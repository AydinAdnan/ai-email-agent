"""Command-line entry point.

``wajo sim run`` replays a fixture as a chat: arrivals stream in on one task while
stdin is read on another, and the run stops only where the safety floor says the
user is needed. ``wajo loop run`` calibrates that way and then walks the same lane
with what the calibration kept.
"""
import argparse
import asyncio
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import IO

from dotenv import load_dotenv

from agent.autonomy.preferences import RememberedProvider
from agent.dataset import (
    DEFAULT_DATASET_PATH,
    Lane,
    Manifest,
    ManifestError,
    SplitViolation,
)
from agent.gateway import (
    ENDPOINTS,
    ProposalError,
    ProposalGateway,
    ProposalProvider,
    build_provider,
)
from agent.graph import GraphError, GraphSession
from agent.loop import run_loop
from agent.memory.claims import ClaimStore
from agent.memory.consent import Capability, Grant, session_grant
from agent.sim.policy import GoldPolicy, ProposalPolicy
from agent.sim.runner import DecisionSource, run_simulation
from agent.trace import TraceError, TraceSink

# The lanes a human may sit in front of. Held-out cases are sealed: reading them
# here would spend the only unbiased measurement Phase 8 has.
SIM_LANES = (Lane.CALIBRATION, Lane.DEVELOPMENT)


def build_parser() -> argparse.ArgumentParser:
    """The CLI's argument grammar."""
    parser = argparse.ArgumentParser(prog="wajo", description="WAJO email autonomy agent")
    commands = parser.add_subparsers(dest="command", required=True)

    sim = commands.add_parser("sim", help="streaming inbox simulator")
    sim_commands = sim.add_subparsers(dest="sim_command", required=True)

    run = sim_commands.add_parser(
        "run",
        help="replay a fixture as a chat, blocking only for ask-first and escalate",
    )
    _replay_flags(run)
    run.add_argument(
        "--no-learn",
        action="store_true",
        help=(
            "calibrate without keeping anything: the session holds the learning "
            "capability and no consent, so a confirmed rule is heard and not stored"
        ),
    )
    run.add_argument(
        "--show-labels",
        action="store_true",
        help="add the dataset's labels to each arrival (debugging only: they are the answer key)",
    )
    run.add_argument(
        "--policy",
        choices=["proposal", "labels"],
        default="proposal",
        help=(
            "where a route comes from: the pipeline (triage plus a proposal) or the "
            "dataset's labels, which is the reference for scoring only"
        ),
    )
    loop = commands.add_parser("loop", help="calibrate a lane, then walk it with what was learned")
    loop_commands = loop.add_subparsers(dest="loop_command", required=True)
    guided = loop_commands.add_parser(
        "run",
        help=(
            "two passes over one lane: a calibration chat, then the graph over the same "
            "mail with the rules that chat produced answering first"
        ),
    )
    _replay_flags(guided)
    guided.add_argument(
        "--say",
        action="append",
        metavar="[CASE=]LINE[;LINE]",
        help=(
            "answer a decision that waits, either naming the case it answers or in the "
            "order the decisions wait; a rule's confirmation is the entry's second line "
            "('WAJO-0008=ignore mail from claire@... ; yes')"
        ),
    )

    graph = commands.add_parser("graph", help="the checkpointed decision graph")
    graph_commands = graph.add_subparsers(dest="graph_command", required=True)
    walk = graph_commands.add_parser(
        "run",
        help="walk a fixture through the graph, one checkpointed decision per arrival",
    )
    _replay_flags(walk)
    walk.add_argument(
        "--no-mask",
        action="store_true",
        help=(
            "hand the provider the raw mail; the default masks subject and body first, "
            "which is what this switch exists to measure against"
        ),
    )
    walk.add_argument(
        "--approve",
        metavar="CASE_ID",
        help=(
            "after the run, answer that arrival's held decision with a yes and report "
            "what it committed (nothing is approved without this flag)"
        ),
    )
    return parser


def _replay_flags(target: argparse.ArgumentParser) -> None:
    """The flags both replay paths take: which mail, which lane, who proposes, a trace."""
    target.add_argument(
        "--fixture",
        default=str(DEFAULT_DATASET_PATH),
        help="JSONL dataset or fixture to replay (default: the full dataset)",
    )
    target.add_argument(
        "--mail",
        metavar="PATH",
        help=(
            "replay plain mail instead of a dataset: one JSON object per message with "
            "sender, to, subject and body. Such rows carry no labels, so nothing is scored"
        ),
    )
    target.add_argument(
        "--seed",
        type=int,
        default=7,
        help="seed for the deterministic clock and the order inside each arrival window",
    )
    target.add_argument(
        "--lane",
        choices=[lane.value for lane in SIM_LANES],
        default=Lane.CALIBRATION.value,
        help=(
            "which split to replay (default: the calibration lane); the sealed "
            "held-out lane is not offered, only the eval run may open it"
        ),
    )
    target.add_argument(
        "--provider",
        choices=["rules", *ENDPOINTS],
        default="rules",
        help=(
            "who proposes: the offline rule stand-in, or a model endpoint "
            "(its key goes in .env at the repository root)"
        ),
    )
    target.add_argument(
        "--model",
        help="model id to use; falls back to WAJO_MODEL, then the endpoint's default",
    )
    target.add_argument(
        "--trace",
        metavar="PATH",
        help=(
            "append a JSONL trace of every decision to PATH: ids, hashes and bounded "
            "records, with mail text and secrets replaced by digests"
        ),
    )
    target.add_argument(
        "--store",
        metavar="PATH",
        help=(
            "the rules you confirm, kept in PATH as JSONL: read at the start and written "
            "at the end, so the next run answers from them instead of asking again"
        ),
    )


def _view_note(show_labels: bool) -> str:
    """Say what the reader is looking at, since labels change the calibration."""
    if show_labels:
        return "labels are on: each arrival carries the dataset's answer next to the pipeline's"
    return "each arrival is shown as mail: sender, subject and body only"


def _open_store(args: argparse.Namespace) -> ClaimStore:
    """The run's memory: the rules already kept, and the file they live in."""
    grant = (
        Grant(capability=Capability.LEARN)
        if getattr(args, "no_learn", False)
        else session_grant(purpose="calibration session")
    )
    return ClaimStore(grant=grant, path=args.store)


def _proposing(provider: ProposalProvider, store: ClaimStore) -> ProposalGateway:
    """The pipeline's proposer: a rule already confirmed answers before the provider does."""
    return ProposalGateway(RememberedProvider(store, provider))


def _policy(
    args: argparse.Namespace, store: ClaimStore
) -> tuple[DecisionSource, str]:
    """Pick the decision source and name it. Labels are a reference mode, not the default."""
    if args.policy == "labels":
        return GoldPolicy(), "the dataset's labels (reference)"
    provider = build_provider(args.provider, model=args.model)
    label = str(getattr(provider, "label", None) or getattr(provider, "name", provider))
    return ProposalPolicy(_proposing(provider, store)), f"the {label} proposal"


def _store_note(args: argparse.Namespace, store: ClaimStore, out: IO[str]) -> None:
    """Say what a run starts with, so it is obvious whether earlier rules are in force."""
    if not args.store:
        return
    if store.refusal:
        out.write(f"rules in {args.store}: not read ({store.refusal})\n")
        return
    out.write(f"rules in {args.store}: {store.loaded} loaded\n")


def _keep_rules(args: argparse.Namespace, store: ClaimStore, out: IO[str]) -> None:
    """Write the rules to the run's file, and list what is now in force."""
    if not args.store:
        return
    store.save()
    if store.refusal:
        out.write(f"rules in {args.store}: not written ({store.refusal})\n")
        return
    active = sum(1 for claim in store.claims if claim.active)
    out.write(f"rules in {store.path}: {active} in force\n")
    for claim in store.claims:
        replaced = "" if claim.active else " (replaced)"
        out.write(f"    {claim.claim_id}  {claim.describe()}{replaced}\n")


def sim_run(args: argparse.Namespace, out: IO[str]) -> int:
    """Replay a fixture or a plain mail stream through the chat loop."""
    manifest = (
        Manifest.load(args.mail, mail_only=True) if args.mail else Manifest.load(args.fixture)
    )
    view = manifest.view(Lane(args.lane))
    cases = view.cases
    store = _open_store(args)
    policy, source = _policy(args, store)
    out.write(
        f"fixture: {manifest.source}\n"
        f"lane: {view.lane.value}  cases: {len(cases)}  seed: {args.seed}\n"
        f"digest: {manifest.dataset_digest[:16]}\n"
        f"proposal source: {source}\n"
    )
    _store_note(args, store, out)
    out.write(
        "type a line when a decision waits for you; lines already typed are "
        "corrections, bound to the decision they followed\n"
        f"{_view_note(args.show_labels)}\n\n"
    )
    sink = TraceSink(args.trace) if args.trace else None
    try:
        outcome = asyncio.run(
            run_simulation(
                view,
                seed=args.seed,
                out=out,
                policy=policy,
                show_labels=args.show_labels,
                trace=sink,
                store=store,
            )
        )
    finally:
        # A run that dies mid-lane still leaves the lines it wrote.
        if sink is not None:
            sink.close()
    _keep_rules(args, store, out)
    if sink is not None:
        out.write(f"trace: {sink.lines} line(s) in {sink.path}\n")
    return 0 if outcome.processed == len(cases) else 1


def loop_run(args: argparse.Namespace, out: IO[str]) -> int:
    """Calibrate on a lane and then walk it again with what that pass kept."""
    manifest = (
        Manifest.load(args.mail, mail_only=True) if args.mail else Manifest.load(args.fixture)
    )
    view = manifest.view(Lane(args.lane))
    provider = build_provider(args.provider, model=args.model)
    label = str(getattr(provider, "label", None) or getattr(provider, "name", provider))
    store = _open_store(args)
    out.write(
        f"fixture: {manifest.source}\n"
        f"lane: {view.lane.value}  cases: {len(view.cases)}  seed: {args.seed}\n"
        f"digest: {manifest.dataset_digest[:16]}\n"
        f"proposal source: the {label} proposal\n"
    )
    _store_note(args, store, out)
    out.write(
        "\n[pass 1] calibration: the mail arrives, and only a decision that waits asks "
        "you for a line\n"
    )
    sink = TraceSink(args.trace) if args.trace else None
    try:
        report = asyncio.run(
            run_loop(
                view,
                seed=args.seed,
                out=out,
                script=args.say or (),
                provider=provider,
                store=store,
                trace=sink,
            )
        )
    finally:
        if sink is not None:
            sink.close()

    recalled = set(report.recalled)
    out.write(
        f"\n[pass 2] autonomous: the same lane and seed, with {len(report.claims)} kept "
        "rule(s) answering before the provider\n"
    )
    for index, case_id in enumerate(report.autonomous.order, start=1):
        message = view.open(case_id).event.message
        committed = case_id in {item.case_id for item in report.autonomous.receipts}
        ended = "committed" if committed else report.autonomous.interrupts.get(case_id, "")
        mark = "  <- from a rule" if message.message_id in recalled else ""
        out.write(
            f"[{index:>3}/{len(report.autonomous.order)}] {case_id}  "
            f"{report.autonomous.routes.get(case_id, ''):<24} {ended}{mark}\n"
        )
    out.write(
        f"\nasked for a line: {report.asked_before} in pass 1, {report.asked_after} in pass 2"
        f"  ({report.quietened} decided by a rule)\n"
        f"receipts: {len(report.calibration.receipts)} in pass 1, "
        f"{len(report.autonomous.receipts)} in pass 2\n"
    )
    if not report.claims:
        out.write("no rule was confirmed, so pass 2 decides exactly as pass 1\n")
    elif not args.store:
        out.write("kept after this run:\n")
        for claim in report.claims:
            out.write(f"    {claim.claim_id}  {claim.describe()}\n")
    _keep_rules(args, store, out)
    if sink is not None:
        out.write(f"trace: {sink.lines} line(s) in {sink.path}\n")
    return 0 if report.autonomous.processed == len(view.cases) else 1


def graph_run(args: argparse.Namespace, out: IO[str]) -> int:
    """Walk a fixture through the decision graph and say what each arrival ended in."""
    manifest = (
        Manifest.load(args.mail, mail_only=True) if args.mail else Manifest.load(args.fixture)
    )
    view = manifest.view(Lane(args.lane))
    cases = view.cases
    provider = build_provider(args.provider, model=args.model)
    label = str(getattr(provider, "label", None) or getattr(provider, "name", provider))
    mask = not args.no_mask
    store = _open_store(args)
    out.write(
        f"fixture: {manifest.source}\n"
        f"lane: {view.lane.value}  cases: {len(cases)}  seed: {args.seed}\n"
        f"digest: {manifest.dataset_digest[:16]}\n"
        f"proposal source: the {label} proposal\n"
        f"provider view: {'masked subject and body' if mask else 'the raw mail'}\n"
    )
    _store_note(args, store, out)
    out.write("\n")
    sink = TraceSink(args.trace) if args.trace else None
    session = GraphSession(
        view,
        seed=args.seed,
        gateway=_proposing(provider, store),
        mask=mask,
        trace=sink,
    )
    note = ""
    try:
        outcome = asyncio.run(session.run())
        if args.approve:
            note = _resume_note(session, args.approve)
    finally:
        if sink is not None:
            sink.close()

    for index, case_id in enumerate(outcome.order, start=1):
        ended = outcome.interrupts.get(case_id, "")
        done = "committed" if case_id in {item.case_id for item in outcome.receipts} else ended
        out.write(
            f"[{index:>3}/{len(outcome.order)}] {case_id}  "
            f"{outcome.routes.get(case_id, ''):<24} {done}\n"
        )
    out.write(
        f"\nprocessed={outcome.processed} committed={len(outcome.receipts)} "
        f"held={len(outcome.held)} refused={len(outcome.refusals)}\n"
    )
    for item in outcome.held:
        out.write(f"    waiting on you: {item.case_id} {item.digest[:12]} {item.summary()}\n")
    for route, count in sorted(outcome.route_counts.items()):
        out.write(f"    {route:<24} {count}\n")
    if note:
        out.write(note)
    _keep_rules(args, store, out)
    if sink is not None:
        out.write(f"trace: {sink.lines} line(s) in {sink.path}\n")
    return 0 if outcome.processed == len(cases) else 1


def _resume_note(session: GraphSession, case_id: str) -> str:
    """Answer one held decision with a yes and say what that committed."""
    approved = {item.case_id: item for item in session.outcome.held}
    if case_id not in approved:
        return f"\napprove: {case_id} is not waiting for an answer\n"
    result = asyncio.run(
        session.resume(
            case_id,
            {"approved_by": "user", "prepared_digest": approved[case_id].digest},
        )
    )
    detail = result.receipt.summary() if result.receipt is not None else result.reason
    return f"\napprove: {case_id} -> {result.status} ({detail})\n"


def main(argv: Sequence[str] | None = None) -> int:
    """Entry point for the ``wajo`` console script."""
    # A key in .env is what makes --provider openrouter runnable; without this the file
    # sits there looking authoritative while the provider reports no key. The path is
    # named rather than discovered: this file lives two levels below the repository
    # root, and a search from the caller's frame finds a .env somewhere else or none.
    load_dotenv(Path(__file__).resolve().parents[2] / ".env")
    args = build_parser().parse_args(argv)
    out = sys.stdout
    if (args.command, getattr(args, "graph_command", None)) == ("graph", "run"):
        try:
            return graph_run(args, out)
        except KeyboardInterrupt:
            out.write("\nstopped before the lane finished\n")
            return 130
        except (GraphError, ManifestError, SplitViolation, TraceError, OSError) as error:
            # Foreseeable operational failures get one readable line, not a traceback.
            out.write(f"cannot run: {error}\n")
            return 2
    if (args.command, getattr(args, "loop_command", None)) == ("loop", "run"):
        try:
            return loop_run(args, out)
        except KeyboardInterrupt:
            out.write("\nstopped before the second pass finished\n")
            return 130
        except (ProposalError, ManifestError, SplitViolation, TraceError, OSError) as error:
            # Foreseeable operational failures get one readable line, not a traceback.
            out.write(f"cannot run: {error}\n")
            return 2
    if (args.command, getattr(args, "sim_command", None)) == ("sim", "run"):
        try:
            return sim_run(args, out)
        except KeyboardInterrupt:
            out.write("\nstopped before the run finished\n")
            return 130
        except (ProposalError, ManifestError, SplitViolation, TraceError, OSError) as error:
            # Foreseeable operational failures get one readable line, not a traceback.
            out.write(f"cannot run: {error}\n")
            return 2
    return 2


__all__ = ["build_parser", "main", "sim_run"]
