from __future__ import annotations

import asyncio
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import IO

from agent.autonomy.bandit import Learner
from agent.autonomy.preferences import RememberedProvider
from agent.autonomy.router import Router
from agent.dataset import LaneView
from agent.gateway import ProposalGateway, ProposalProvider, RuleProvider
from agent.graph import GraphOutcome, GraphSession
from agent.memory.claims import Claim, ClaimStore
from agent.memory.consent import session_grant
from agent.sim.policy import Decision, ProposalPolicy
from agent.sim.runner import InterruptHook, SimOutcome, close_input, run_simulation
from agent.sim.schedule import WINDOW_SIZE
from agent.trace import TraceSink

# A scripted entry holds the lines that belong to one decision, in the order a prompt
# reads them: the line itself, then the confirmation a rule needs before it is stored.
SCRIPT_SEPARATOR = ";"

# What a decision the script does not answer is told, so the run carries on instead of
# waiting for input nobody is going to give. It reads as neither a rule nor a decision:
# the line is recorded and changes nothing.
SKIP_LINE = "nothing for now"


class ScriptedReplies:
    """Types scripted lines at the decisions that wait for a human.

    A line handed over before its prompt exists is read as a correction to the previous
    decision, so a decision's lines are released only while it is on screen. An entry
    may name the case it answers; the rest answer the decisions in the order they wait.
    """

    def __init__(self, entries: Sequence[str]) -> None:
        self.named: dict[str, list[str]] = {}
        self.in_order: list[list[str]] = []
        for entry in entries:
            case_id, separator, line = entry.partition("=")
            if separator:
                self.named.setdefault(case_id.strip(), []).extend(line.split(SCRIPT_SEPARATOR))
            else:
                self.in_order.append(case_id.split(SCRIPT_SEPARATOR))

    @property
    def remaining(self) -> int:
        return len(self.named) + len(self.in_order)

    def hook(self, queue: asyncio.Queue[str]) -> InterruptHook:
        """A hook that hands the waiting decision its lines, and closes input at the end."""

        async def feed(index: int, decision: Decision) -> None:
            lines = self.named.pop(decision.case_id, None)
            if lines is None and self.in_order:
                lines = self.in_order.pop(0)
            for line in lines if lines is not None else [SKIP_LINE]:
                queue.put_nowait(line.strip())
            if self.remaining == 0:
                await close_input(queue)

        return feed


@dataclass
class LoopReport:
    """One lane, walked with a baseline pipeline and with what the user said during it."""

    source: str
    total: int
    calibration: SimOutcome
    autonomous: GraphOutcome
    claims: tuple[Claim, ...]
    # The messages a confirmed rule answered in the second pass.
    recalled: tuple[str, ...]
    # Each arrival a rule answered, and the arrival whose mail taught that rule.
    answered: Mapping[str, str]
    # The same lane, same seed and same learner, with no rules in front of the provider:
    # what the second pass would have decided had the first pass taught nothing. None when
    # no rule answered anything, because then there is nothing to compare against.
    without_rules: GraphOutcome | None
    # What the calibration counted: the posteriors the router will read.
    learner: Learner

    @property
    def asked_before(self) -> int:
        """Decisions the chat pass waited on.

        Not a baseline: a rule takes effect from the next arrival, so the chat pass is
        already quieter than no rules at all from the mail it was taught on. The honest
        baseline is ``without_rules``, and ``saved`` is the difference it measures.
        """
        return self.calibration.interrupts

    @property
    def asked_after(self) -> int:
        """Decisions that would still wait for a human, with the rules in front."""
        return len(self.autonomous.interrupts)

    @property
    def asked_without_rules(self) -> int:
        """Decisions the same lane waits on with nothing remembered, or 0 with no control."""
        return 0 if self.without_rules is None else len(self.without_rules.interrupts)

    @property
    def changed(self) -> tuple[str, ...]:
        """Arrivals a rule sent somewhere else than the lane would have gone on its own."""
        if self.without_rules is None:
            return ()
        return tuple(
            case_id
            for case_id in self.autonomous.order
            if self.without_rules.routes.get(case_id) != self.autonomous.routes.get(case_id)
        )

    @property
    def changed_later(self) -> tuple[str, ...]:
        """Of those, the arrivals that came after the mail their rule was taught on.

        This is the number that says the agent learned something rather than echoed back
        the decision it was just handed: a rule answering its own teaching mail changes
        nothing for any other arrival.
        """
        return tuple(
            case_id for case_id in self.changed if self.answered.get(case_id) != case_id
        )

    @property
    def saved(self) -> int:
        """Asking the rules took off the user, measured against the lane with no rules.

        Counted per arrival rather than from the ask totals: a lane where a rule silences
        four asks and the learner's own drift adds one would report saving one, which is
        not what the rules did.
        """
        if self.without_rules is None:
            return 0
        return sum(
            1
            for case_id in self.answered
            if case_id in self.without_rules.interrupts
            and case_id not in self.autonomous.interrupts
        )


async def run_loop(
    view: LaneView,
    *,
    seed: int = 7,
    out: IO[str] | None = None,
    script: Sequence[str] = (),
    provider: ProposalProvider | None = None,
    store: ClaimStore | None = None,
    mask: bool = True,
    window: int = WINDOW_SIZE,
    trace: TraceSink | None = None,
) -> LoopReport:
    """Calibrate on a lane, then walk the same lane with the rules it produced.

    Two passes over one lane and one seed, so the mail arrives in the same order both
    times. The first is the chat loop: every decision that waits is answered, and a
    confirmed answer is kept as a claim. The second is the graph over that same mail,
    with the kept claims consulted before the provider.

    Both passes decide through the same safety floor, which is what makes the second one
    safe to trust: it can only be quieter where the floor leaves it that room.

    A third pass walks the lane with no rules in front of the provider, so the report can
    say what the rules changed rather than assume every arrival a rule answered would
    otherwise have waited. It is skipped when nothing was kept, and it is one more pass
    over the lane, so a run against a model pays for it.
    """
    inner = provider if provider is not None else RuleProvider()
    store = store if store is not None else ClaimStore(
        grant=session_grant(purpose="calibration session")
    )
    replies = ScriptedReplies(script)
    queue: asyncio.Queue[str] = asyncio.Queue()
    learner = Learner()
    # One router for both passes: what the calibration earns is what the autonomous pass
    # then spends, which is the whole point of running them in that order.
    router = Router(learner)
    # One memory for both passes as well. A rule takes effect from the next arrival - the
    # plan's own wording for the scope echo - so the chat pass consults the claims it is
    # confirming rather than asking again for what the user just answered.
    remembered = RememberedProvider(store, inner)

    calibration = await run_simulation(
        view,
        seed=seed,
        out=out,
        input_queue=queue,
        on_interrupt=replies.hook(queue),
        policy=ProposalPolicy(ProposalGateway(remembered)),
        store=store,
        learner=learner,
        router=router,
        window=window,
        trace=trace,
    )

    session = GraphSession(
        view,
        seed=seed,
        gateway=ProposalGateway(remembered),
        mask=mask,
        router=router,
        window=window,
        trace=trace,
    )
    autonomous = await session.run()
    answered = _answered_cases(view, store, remembered)
    without_rules = None
    if answered:
        # Same seed, same lane, same learner, same floor - only the memory in front of the
        # provider is gone, so a route that differs is a route a rule moved.
        without_rules = await GraphSession(
            view,
            seed=seed,
            gateway=ProposalGateway(inner),
            mask=mask,
            router=router,
            window=window,
        ).run()
    return LoopReport(
        source=remembered.label,
        total=len(view.cases),
        calibration=calibration,
        autonomous=autonomous,
        claims=tuple(store.claims),
        recalled=tuple(sorted(remembered.answered)),
        answered=answered,
        without_rules=without_rules,
        learner=learner,
    )


def _answered_cases(
    view: LaneView, store: ClaimStore, remembered: RememberedProvider
) -> dict[str, str]:
    """Each arrival a rule answered, mapped to the arrival whose mail taught that rule."""
    by_message = {case.event.message.message_id: case.case_id for case in view.cases}
    by_claim = {claim.claim_id: claim for claim in store.claims}
    answered: dict[str, str] = {}
    for message_id, claim_id in remembered.answered.items():
        case_id = by_message.get(message_id)
        claim = by_claim.get(claim_id)
        if case_id is not None and claim is not None:
            answered[case_id] = claim.source_case_id or case_id
    return answered


__all__ = ["LoopReport", "ScriptedReplies", "run_loop"]
