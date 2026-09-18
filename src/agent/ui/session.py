from __future__ import annotations

import asyncio
import re
import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from agent.autonomy.bandit import Learner
from agent.autonomy.preferences import RememberedProvider
from agent.dataset import DEFAULT_DATASET_PATH, Lane, LaneView, Manifest
from agent.gateway import ProposalGateway, ProposalProvider, build_provider
from agent.memory.claims import ClaimStore
from agent.memory.consent import session_grant
from agent.sim.policy import Decision, ProposalPolicy, quietenable
from agent.sim.runner import ChatRunner, SimOutcome, close_input

# The run's own output is the contract here, exactly as it is for the tests: an arrival
# header, a decision waiting for the user, the user's own line, the summary.
MAIL_HEADER = re.compile(r"^\[\s*\d+/\d+\] ")
# The case an arrival block is about, so its route can be recorded beside it.
MAIL_CASE = re.compile(r"^\[\s*\d+/\d+\]\s*(\S+)")
# The preamble a run prints before the first arrival: provenance, not a message, so the page
# can keep it out of the conversation.
RUN_FACTS = ("fixture:", "lane:", "digest:", "proposal source:", "rules loaded:", "schedule:")

_loop_lock = threading.Lock()
_loop: asyncio.AbstractEventLoop | None = None


def _background_loop() -> asyncio.AbstractEventLoop:
    """One event loop for the process, running on its own thread.

    HTTP handlers arrive on request threads, so the run cannot live on the loop the page
    happens to be served from. The loop is a daemon thread: closing the server ends it.
    """
    global _loop
    with _loop_lock:
        if _loop is None:
            _loop = asyncio.new_event_loop()
            threading.Thread(target=_loop.run_forever, daemon=True, name="wajo-ui").start()
        return _loop


@dataclass(frozen=True)
class Block:
    """One chunk of the run's output, as the page shows it."""

    index: int
    kind: str
    text: str

    def as_json(self) -> dict[str, Any]:
        return {"index": self.index, "kind": self.kind, "text": self.text}


def classify(text: str) -> str:
    """What the page should make of one chunk: mail, a wait, a typed line, the summary."""
    if MAIL_HEADER.match(text):
        return "mail"
    if "[waiting]" in text:
        return "wait"
    if text.lstrip().startswith("reply for "):
        return "reply"
    if text.strip() == "run summary":
        return "summary"
    if text.lstrip().startswith(RUN_FACTS):
        return "meta"
    return "note"


class AnswerQueue(asyncio.Queue[str]):
    """The line queue the run reads from, which is also what "waiting" means.

    The run reads a line at an interrupt and again for the confirmation that follows a rule,
    and only the second of those is visible to the interrupt hook. A read blocked on this
    queue is the honest signal for both, so the page hands the input over whenever the run is
    the one waiting rather than whenever a hook happens to fire.
    """

    def __init__(self, session: Session) -> None:
        super().__init__()
        self.session = session

    async def get(self) -> str:
        self.session.waiting = True
        try:
            return await super().get()
        finally:
            self.session.waiting = False


class Transcript:
    """The runner's output, collected as blocks instead of printed."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def write(self, text: str) -> int:
        if text.strip():
            self.session.add(text.rstrip("\n"))
        return len(text)

    def flush(self) -> None:
        return None


class Session:
    """One calibration run, driven a line at a time.

    The run is the one the CLI drives - same gateway, store, floor and learner - so the page
    cannot disagree with the terminal about what the agent did. Typed lines are handed to the
    run through the same queue the scripted transcript uses, and every rule kept lands in the
    same store file.
    """

    def __init__(
        self,
        *,
        fixture: Path | str | None = None,
        lane: str = Lane.CALIBRATION.value,
        seed: int = 7,
        store_path: Path | str | None = None,
        provider: str = "rules",
        model: str | None = None,
    ) -> None:
        self.fixture = Path(fixture) if fixture is not None else DEFAULT_DATASET_PATH
        self.lane = lane
        self.seed = seed
        self.provider = provider
        self.model = model
        self.blocks: list[Block] = []
        self.waiting = False
        self.done = False
        self.case_id = ""
        self.error = ""
        # What each arrival was routed to, and whether a rule could take the waiting one
        # off the screen. The page colours a card by the first and offers the right
        # choices with the second.
        self.routes: dict[str, str] = {}
        self.quietenable = True
        self.confirming = False
        self.view: LaneView | None = None
        # The run itself, held so the page can read what it has done so far rather than
        # only what it did once the whole lane is over.
        self.runner: ChatRunner | None = None
        self.outcome: SimOutcome | None = None
        self.store = ClaimStore(
            grant=session_grant(purpose="page session"),
            path=Path(store_path) if store_path else None,
        )
        self.learner = Learner()
        self._queue: asyncio.Queue[str] | None = None
        self._lock = threading.Lock()
        # The summary is written a line at a time, and it is one thing on screen.
        self._in_summary = False

    def start(self) -> None:
        """Load the lane and begin the run. A failure here is the caller's to report."""
        manifest = Manifest.load(self.fixture)
        view = manifest.view(Lane(self.lane))
        proposal: ProposalProvider = build_provider(self.provider, model=self.model)
        label = str(getattr(proposal, "label", None) or proposal.name)
        self.add(f"fixture: {manifest.source}")
        self.add(f"lane: {view.lane.value}  cases: {len(view.cases)}  seed: {self.seed}")
        self.add(f"digest: {manifest.dataset_digest[:16]}")
        self.add(f"proposal source: the {label} proposal")
        self.add(f"rules loaded: {self.store.loaded}")
        asyncio.run_coroutine_threadsafe(
            self._run(view, ProposalPolicy(ProposalGateway(RememberedProvider(self.store, proposal)))),
            _background_loop(),
        )

    async def _run(self, view: LaneView, policy: ProposalPolicy) -> None:
        queue: asyncio.Queue[str] = AnswerQueue(self)
        self._queue = queue
        self.view = view
        runner = ChatRunner(
            view,
            seed=self.seed,
            out=Transcript(self),
            input_queue=queue,
            on_interrupt=self._waited,
            policy=policy,
            store=self.store,
            learner=self.learner,
        )
        self.runner = runner
        try:
            self.outcome = await runner.run()
        # Any failure ends the session with the reason on screen; a page cannot print a
        # traceback, and a run that dies silently looks like a page that is stuck.
        except Exception as error:  # noqa: BLE001
            self.error = f"{type(error).__name__}: {error}"
        finally:
            self.waiting = False
            self.done = True
            self.add(f"session ended: {self.store.save()} rule(s) in force")

    async def _waited(self, index: int, decision: Decision) -> None:
        """Called while a decision is on screen and before its line is read."""
        self.case_id = decision.case_id
        # The run already answered this at the prompt; asking it the same way keeps the two
        # from ever disagreeing about which decisions a rule can take off the screen.
        case = self.view.open(decision.case_id) if self.view is not None else None
        self.quietenable = quietenable(case) if case is not None else True

    def add(self, text: str) -> None:
        """Append one block, with the number the page polls from."""
        # The summary is one thing written a line at a time, so it stays open until a line
        # that is not indented under it arrives.
        self._in_summary = text.strip() == "run summary" or (
            self._in_summary and text.startswith("    ")
        )
        with self._lock:
            self.blocks.append(
                Block(index=len(self.blocks), kind="summary" if self._in_summary else classify(text), text=text)
            )
        # The route is read off the decision the run just made: the arrival block for a case
        # is emitted in the same step that decided it, so this is that case's route.
        arrival = MAIL_CASE.match(text)
        decision = self.runner.last_decision if self.runner is not None else None
        if arrival and decision is not None and decision.case_id == arrival[1]:
            self.routes[arrival[1]] = decision.route.value
        # A question with a parenthesised hint is the run about to read one more line about
        # the rule it just echoed, which is the only other thing a line can be.
        self.confirming = text.rstrip().endswith(")") and "?" in text

    def reply(self, text: str) -> None:
        """Hand a typed line to the run that is waiting for one."""
        queue = self._queue
        if not self.waiting or queue is None:
            raise RuntimeError("nothing is waiting for a line")
        self.waiting = False
        _background_loop().call_soon_threadsafe(queue.put_nowait, text)

    def stop(self) -> None:
        """End the run the way end of input does: nothing else is approved."""
        queue = self._queue
        if queue is None or self.done:
            return
        self.waiting = False
        asyncio.run_coroutine_threadsafe(close_input(queue), _background_loop())

    def since(self, index: int) -> list[Block]:
        """Every block the page has not seen yet."""
        with self._lock:
            return [block for block in self.blocks if block.index >= index]

    def state(self) -> dict[str, Any]:
        """What the page's side panel shows: what the run did and what it now knows."""
        store = self.store
        # Read from the runner, not from a finished result: the panel is meant to be watched.
        outcome = self.runner.outcome if self.runner is not None else None
        return {
            "waiting": self.waiting,
            "done": self.done,
            "case": self.case_id,
            "error": self.error,
            "count": len(self.blocks),
            # Counted from the routes rather than from the finished run, so the panel moves
            # as the lane is walked instead of only at the end.
            "seen": len(outcome.route_counts) if outcome else 0,
            "interrupts": outcome.interrupts if outcome else 0,
            "receipts": len(outcome.receipts) if outcome else 0,
            "routes": dict(outcome.route_counts) if outcome else {},
            "routes_by_case": dict(self.routes),
            "quietenable": self.quietenable,
            "confirming": self.confirming,
            "claims": [claim.describe() for claim in store.claims if claim.active],
            "posteriors": [
                f"{bucket.describe()} - {self.learner.store.posterior(bucket).describe()}"
                for bucket in self.learner.store.contexts()
            ],
            "learner": {
                "updates": self.learner.updates,
                "ignored": self.learner.ignored,
                "refused_arms": self.learner.refusals,
            },
            "rules_file": str(store.path) if store.path is not None else "",
            "rules_refusal": store.refusal,
        }


__all__ = ["AnswerQueue", "Block", "Session", "Transcript", "classify"]
