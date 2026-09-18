"""The evaluation run: teach the learning lane, freeze it, score the sealed lane once.

Three steps, in the order the plan puts them, because each one is only meaningful after
the last. The learning lane is replayed with a scripted transcript - the lane the user is
allowed to teach from - which moves the posteriors, adapts the cutoffs and confirms a few
scoped rules. Then that state is frozen to disk, so the sealed lane can be scored against a
learner that is no longer moving and a report can name the exact state it used. Only then
does the held-out lane run, once, with nobody at the keyboard and nothing to teach it.

What comes out is artifacts/eval: the report the release claims, the frozen learner it was
measured against, and the rules the user confirmed, each readable on its own.

    uv run wajo eval all --out artifacts/eval
    uv run python -m evals.run_eval --fixture datasets/wajo_cases.jsonl
"""
from __future__ import annotations

import argparse
import asyncio
import io
import json
import sys
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from agent.autonomy import state as learner_state
from agent.autonomy.bandit import Learner
from agent.autonomy.preferences import RememberedProvider
from agent.autonomy.router import Router
from agent.dataset import DEFAULT_DATASET_PATH, Lane, LaneView, Manifest
from agent.gateway import ProposalGateway, ProposalProvider, RuleProvider
from agent.graph import GraphSession
from agent.loop import ScriptedReplies
from agent.memory.claims import ClaimStore
from agent.memory.consent import session_grant
from agent.sim.policy import ProposalPolicy
from agent.sim.runner import close_input, run_simulation
from agent.sim.schedule import WINDOW_SIZE
from agent.trace import TraceSink
from evals.harness import (
    BLOCK,
    CalibrationReport,
    EvalReport,
    HeldOutReport,
    ScoringError,
    calibration_report,
    held_out_report,
    record_from_chat,
    record_from_graph,
    two_lane_report,
)

DEFAULT_SCRIPT = Path(__file__).resolve().parent / "scenarios" / "learning_stream.json"
DEFAULT_OUT = Path("artifacts") / "eval"


@dataclass(frozen=True)
class ScriptedTeaching:
    """The transcript: what the user says, at the decisions they say it at."""

    name: str
    description: str
    replies: tuple[Mapping[str, Any], ...]

    @property
    def entries(self) -> tuple[str, ...]:
        """The transcript in the chat loop's own form: ``CASE=line;line``."""
        return tuple(
            f"{reply['case']}={';'.join(str(line) for line in reply['lines'])}"
            for reply in self.replies
        )

    @property
    def lines(self) -> int:
        return sum(len(reply["lines"]) for reply in self.replies)

    @property
    def cases(self) -> tuple[str, ...]:
        return tuple(str(reply["case"]) for reply in self.replies)


def load_script(path: Path | str = DEFAULT_SCRIPT) -> ScriptedTeaching:
    """Read a transcript, naming what is wrong with it rather than failing on a KeyError."""
    source = Path(path)
    try:
        payload = json.loads(source.read_text(encoding="utf-8"))
    except OSError as error:
        raise ScoringError(f"cannot read the transcript {source}: {error}") from error
    except json.JSONDecodeError as error:
        raise ScoringError(f"the transcript {source} is not JSON: {error}") from error
    replies = payload.get("replies") if isinstance(payload, Mapping) else None
    if not isinstance(replies, list) or not replies:
        raise ScoringError(f"the transcript {source} carries no replies")
    for reply in replies:
        if not isinstance(reply, Mapping) or "case" not in reply or not reply.get("lines"):
            raise ScoringError(
                f"every transcript reply needs a case and at least one line, got {reply!r}"
            )
    return ScriptedTeaching(
        name=str(payload.get("name") or source.name),
        description=str(payload.get("description") or ""),
        replies=tuple(replies),
    )


@dataclass(frozen=True)
class EvalOutcome:
    """The run's report and the files it wrote, so a caller can print or extend them."""

    report: EvalReport
    script: ScriptedTeaching
    seed: int
    lanes: Mapping[str, int]
    rules: tuple[str, ...]
    recall: int
    out: Path
    learner_path: Path
    rules_path: Path
    report_path: Path

    @property
    def calibration(self) -> CalibrationReport:
        return self.report.calibration

    @property
    def held_out(self) -> HeldOutReport:
        return self.report.held_out


def render(outcome: EvalOutcome) -> str:
    """What the run did, in the order a reader wants it: provenance, then the numbers."""
    gates = "\n".join(f"  {gate.describe()}" for gate in outcome.held_out.gates())
    rules = "\n".join(f"    {rule}" for rule in outcome.rules) or "    (none)"
    return "\n".join(
        [
            f"transcript: {outcome.script.name}  "
            f"({outcome.script.lines} line(s) over {len(outcome.script.cases)} decision(s))",
            f"lanes: calibration {outcome.lanes['calibration']} case(s), "
            f"sealed {outcome.lanes['sealed']} case(s)  seed {outcome.seed}",
            "",
            outcome.report.render(),
            "",
            "rules confirmed in the learning lane, in force for the sealed lane:",
            rules,
            f"    recalled by a rule in the sealed lane: {outcome.recall} arrival(s)",
            "",
            "hard gates (a null or a failure is a release blocker, not a trend):",
            gates,
            "",
            f"artifacts: {outcome.report_path.name}, {outcome.learner_path.name}, "
            f"{outcome.rules_path.name} in {outcome.out}",
        ]
    )


async def evaluate(
    calibration: LaneView,
    sealed: LaneView,
    *,
    script: ScriptedTeaching,
    seed: int = 7,
    provider: ProposalProvider | None = None,
    out: Path | str = DEFAULT_OUT,
    block: int = BLOCK,
    window: int = WINDOW_SIZE,
    trace: TraceSink | None = None,
) -> EvalOutcome:
    """Teach, freeze, and score the sealed lane exactly once."""
    out_dir = Path(out)
    try:
        out_dir.mkdir(parents=True, exist_ok=True)
    except OSError as error:
        raise ScoringError(f"cannot make the artifact directory {out_dir}: {error}") from error

    inner = provider if provider is not None else RuleProvider()
    # The run's own memory, in the artifact directory: the user's preferences file is not
    # this run's business, and the rules that decide the sealed lane belong in the evidence.
    store = ClaimStore(
        grant=session_grant(purpose="evaluation run"), path=out_dir / "rules.jsonl"
    )
    learner = Learner()
    router = Router(learner)
    remembered = RememberedProvider(store, inner)

    replies = ScriptedReplies(script.entries)
    queue: asyncio.Queue[str] = asyncio.Queue()
    chat = await run_simulation(
        calibration,
        seed=seed,
        out=io.StringIO(),
        input_queue=queue,
        on_interrupt=replies.hook(queue),
        policy=ProposalPolicy(ProposalGateway(remembered)),
        store=store,
        learner=learner,
        router=router,
        window=window,
        trace=trace,
    )

    # Frozen before the sealed lane runs, not after: what is scored has to be the state the
    # calibration left behind, and a report that kept learning would be measuring itself.
    learner_path = _frozen(out_dir / "learner.json", learner, router)
    store.save()
    writes_before = learner.applied

    await close_input(queue)
    session = GraphSession(
        sealed,
        seed=seed,
        gateway=ProposalGateway(remembered),
        router=router,
        window=window,
        trace=trace,
    )
    sealed_outcome = await session.run()

    report = two_lane_report(
        calibration_report(record_from_chat(chat), block=block),
        held_out_report(
            sealed,
            record_from_graph(sealed_outcome, session.context),
            learning_writes=learner.applied - writes_before,
        ),
    )
    report_path = report.write(out_dir / "report.json")
    return EvalOutcome(
        report=report,
        script=script,
        seed=seed,
        lanes={"calibration": len(calibration.cases), "sealed": len(sealed.cases)},
        rules=tuple(claim.describe() for claim in store.claims if claim.active),
        recall=remembered.recalled,
        out=out_dir,
        learner_path=learner_path,
        rules_path=out_dir / "rules.jsonl",
        report_path=report_path,
    )


def _frozen(path: Path, learner: Learner, router: Router) -> Path:
    """Freeze the learned state, turning the writer's ValueError into a scoring failure."""
    try:
        return learner_state.save(path, learner, router)
    except ValueError as error:
        raise ScoringError(str(error)) from error


def run_eval(
    calibration: LaneView,
    sealed: LaneView,
    *,
    script: ScriptedTeaching | None = None,
    script_path: Path | str = DEFAULT_SCRIPT,
    **kwargs: Any,
) -> EvalOutcome:
    """The async driver, run to completion."""
    return asyncio.run(
        evaluate(
            calibration,
            sealed,
            script=script if script is not None else load_script(script_path),
            **kwargs,
        )
    )


def main(argv: Sequence[str] | None = None) -> int:
    """The eval run as a command, for anyone who would rather not go through the CLI."""
    parser = argparse.ArgumentParser(
        prog="python -m evals.run_eval",
        description="teach the learning lane, freeze it, and score the sealed lane once",
    )
    parser.add_argument("--fixture", default=str(DEFAULT_DATASET_PATH), help="the case set")
    parser.add_argument("--script", default=str(DEFAULT_SCRIPT), help="the teaching transcript")
    parser.add_argument("--out", default=str(DEFAULT_OUT), help="where the artifacts go")
    parser.add_argument("--seed", type=int, default=7, help="seed for both lane runs")
    parser.add_argument("--block", type=int, default=BLOCK, help="cases per curve block")
    args = parser.parse_args(argv)

    manifest = Manifest.load(args.fixture)
    outcome = run_eval(
        manifest.view(Lane.CALIBRATION),
        manifest.view(Lane.HELD_OUT),
        script_path=args.script,
        seed=args.seed,
        out=args.out,
        block=args.block,
    )
    sys.stdout.write(render(outcome) + "\n")
    return 0 if outcome.held_out.gates_ok else 1


if __name__ == "__main__":  # pragma: no cover - the module's own entry point
    raise SystemExit(main())
