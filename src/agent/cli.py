"""Command-line entry point.

``wajo sim run`` replays a fixture as a chat: arrivals stream in on one task while
stdin is read on another, and the run stops only where the safety floor says the
user is needed. ``wajo loop run`` calibrates that way and then walks the same lane
with what the calibration kept.
"""
import argparse
import asyncio
import os
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import IO

from dotenv import load_dotenv

from agent.autonomy.bandit import Learner
from agent.autonomy.preferences import RememberedProvider
from agent.dataset import (
    DEFAULT_DATASET_PATH,
    Lane,
    Manifest,
    ManifestError,
    SplitViolation,
    validate_cases,
)
from agent.gateway import (
    ENDPOINTS,
    ProposalError,
    ProposalGateway,
    ProposalProvider,
    RuleProvider,
)
from agent.graph import GraphError, GraphSession
from agent.jev import DEFAULT_JEV_MODEL, JEV_RECIPE, proposing_provider
from agent.loop import LoopReport, run_loop
from agent.memory.claims import ClaimError, ClaimStore
from agent.memory.consent import Capability, Grant, session_grant
from agent.sim.policy import GoldPolicy, ProposalPolicy
from agent.sim.runner import DecisionSource, run_simulation
from agent.trace import TraceError, TraceSink
from agent.usage import LEDGER
from evals.harness import BLOCK, ScoringError
from evals.run_eval import DEFAULT_OUT as DEFAULT_EVAL_OUT
from evals.run_eval import DEFAULT_SCRIPT as DEFAULT_EVAL_SCRIPT
from evals.run_eval import render as render_eval
from evals.run_eval import run_eval
from evals.sandbox import (
    DEFAULT_JUDGE,
    DEFAULT_PROPOSER,
    DEFAULT_WRITER,
    SandboxError,
    run_sandbox,
)
from evals.sandbox import render as render_sandbox
from evals.sandbox import write_report as write_sandbox_report

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

    evaluation = commands.add_parser(
        "eval", help="the two-lane evaluation: learn, freeze, then score the sealed lane once"
    )
    eval_commands = evaluation.add_subparsers(dest="eval_command", required=True)
    everything = eval_commands.add_parser(
        "all",
        help=(
            "teach the calibration lane with a scripted transcript, freeze the learner, then "
            "run the sealed lane once and write the report"
        ),
    )
    everything.add_argument(
        "--fixture", default=str(DEFAULT_DATASET_PATH), help="JSONL case set to evaluate"
    )
    everything.add_argument(
        "--script",
        default=str(DEFAULT_EVAL_SCRIPT),
        help="the teaching transcript: which decision gets which lines",
    )
    everything.add_argument(
        "--out",
        default=str(DEFAULT_EVAL_OUT),
        help="where report.json, learner.json and rules.jsonl are written",
    )
    everything.add_argument("--seed", type=int, default=7, help="seed for both lane runs")
    everything.add_argument(
        "--block", type=int, default=BLOCK, help="cases per block in the interruption curve"
    )
    everything.add_argument(
        "--provider",
        choices=PROVIDER_CHOICES,
        default=_default_provider(),
        help=(
            "who proposes during the calibration: the offline rules, a model endpoint, or "
            "an endpoint with Jev routing it ('openrouter+jev'). WAJO_PROVIDER sets the "
            "default"
        ),
    )
    everything.add_argument("--model", help="model id to use; falls back to WAJO_MODEL")
    everything.add_argument(
        "--trace", metavar="PATH", help="append both lanes' decisions to a JSONL trace"
    )

    sandbox = commands.add_parser(
        "sandbox",
        help="a live mailbox: fresh mail every run, through the real pipeline, judged from outside",
    )
    sandbox_commands = sandbox.add_subparsers(dest="sandbox_command", required=True)
    sandbox_run = sandbox_commands.add_parser(
        "run",
        help=(
            "write a fresh mailbox, calibrate on half of it with a model standing in for "
            "the user, then let the agent run the half it has never seen"
        ),
    )
    sandbox_run.add_argument(
        "--count",
        type=int,
        default=12,
        help=(
            "arrivals to write; 28 or more covers every one of the briefs in both halves, "
            "which is what makes the per-class learning table mean anything"
        ),
    )
    sandbox_run.add_argument("--seed", type=int, default=7, help="seed for the run")
    sandbox_run.add_argument(
        "--provider",
        choices=[*ENDPOINTS, *(f"{name}+{JEV_RECIPE}" for name in ENDPOINTS)],
        default=_sandbox_provider(),
        help=(
            "the model endpoint the whole run talks to; '<endpoint>+jev' puts the decision "
            "model in front of the agent, while the writer, the user and the judge keep "
            "talking to the endpoint. WAJO_PROVIDER sets the default here too, unless it "
            "names the offline rules, which cannot write mail"
        ),
    )
    sandbox_run.add_argument(
        "--model", default=DEFAULT_PROPOSER, help="the pipeline's model"
    )
    sandbox_run.add_argument(
        "--writer-model", default=DEFAULT_WRITER, help="the model that writes the mail"
    )
    sandbox_run.add_argument(
        "--user-model", default=DEFAULT_JUDGE, help="the model that answers as the user"
    )
    sandbox_run.add_argument(
        "--judge", default=DEFAULT_JUDGE, help="the model that judges the result"
    )
    sandbox_run.add_argument(
        "--judge-sample", type=int, default=12, help="cases the judge is asked about"
    )
    sandbox_run.add_argument(
        "--proposal-timeout",
        type=float,
        default=120.0,
        help=(
            "seconds to wait for one proposal: a slow model answers in half a minute and "
            "sometimes needs longer, and at the gateway's own 20s every proposal would "
            "time out and fail closed"
        ),
    )
    sandbox_run.add_argument("--no-judge", action="store_true", help="skip the judge")
    sandbox_run.add_argument(
        "--no-control",
        action="store_true",
        help=(
            "skip the second pass over the same mailbox with nothing remembered: without "
            "it the run says how often the agent asked, never how much learning took away"
        ),
    )
    sandbox_run.add_argument(
        "--from-mailbox",
        metavar="PATH",
        help=(
            "walk a mailbox an earlier run already wrote instead of paying a model to write "
            "another one; the proposals and the owner's answers recorded beside it are "
            "replayed too, so the second reading of a run costs nothing on those sides"
        ),
    )
    sandbox_run.add_argument(
        "--out", default="artifacts/sandbox", help="where the run, charts and report go"
    )
    sandbox_run.add_argument(
        "--trace", metavar="PATH", help="append both halves' decisions to a JSONL trace"
    )

    data = commands.add_parser("data", help="the case set: what it holds and whether it holds together")
    data_commands = data.add_subparsers(dest="data_command", required=True)
    validate = data_commands.add_parser(
        "validate",
        help=(
            "check the case set's counts, enums and splits: no scenario in two lanes, "
            "no sealed case carrying feedback"
        ),
    )
    validate.add_argument(
        "path",
        nargs="?",
        default=str(DEFAULT_DATASET_PATH),
        help="JSONL case set to check (default: the committed case set)",
    )
    return parser


def sandbox_run_command(args: argparse.Namespace, out: IO[str]) -> int:
    """Write a fresh mailbox and run the pipeline over it, with nobody at the keyboard."""
    sink = TraceSink(args.trace) if args.trace else None
    try:
        outcome = asyncio.run(
            run_sandbox(
                count=args.count,
                seed=args.seed,
                provider=args.provider,
                model=args.model,
                writer_model=args.writer_model,
                user_model=args.user_model,
                judge_model=args.judge,
                out=args.out,
                judge_sample=args.judge_sample,
                proposal_timeout=args.proposal_timeout,
                from_mailbox=args.from_mailbox,
                no_judge=args.no_judge,
                control=not args.no_control,
                trace=sink,
                notes=sys.stderr,
            )
        )
    finally:
        if sink is not None:
            sink.close()
    report, markdown, written = write_sandbox_report(outcome, notes=sys.stderr)
    out.write(render_sandbox(outcome) + "\n")
    out.write(f"\nartifacts: {report.name}, {markdown.name} in {outcome.out}\n")
    out.write(f"charts: {', '.join(path.name for path in written)}\n")
    if sink is not None:
        out.write(f"trace: {sink.lines} line(s) in {sink.path}\n")
    # A sandbox run measures, it does not gate: the mail is new every time and no two
    # runs compare, so it reports and exits zero unless it could not run at all.
    return 0


# One name chooses the whole proposer: an endpoint, and ``+jev`` for the decision model in
# front of it. So the hybrid is ``--provider openrouter+jev`` rather than an endpoint, a
# model, a routing flag and a second model id - and no flag at all when .env says which
# provider a run defaults to.
PROVIDER_NAMES = (RuleProvider.name, *ENDPOINTS)
PROVIDER_CHOICES = [*PROVIDER_NAMES, *(f"{name}+{JEV_RECIPE}" for name in PROVIDER_NAMES)]


def _default_provider() -> str:
    """The provider a run proposes with when the flag is absent.

    Read here rather than at module import, because .env is loaded by ``main`` and this
    runs after it. A value that names no known provider is ignored instead of breaking
    every command: a typo in a dotfile should not take the CLI with it.
    """
    named = os.environ.get("WAJO_PROVIDER", "")
    return named if named in PROVIDER_CHOICES else RuleProvider.name


def _sandbox_provider() -> str:
    """The provider the sandbox proposes with when the flag is absent.

    The sandbox writes mail with a model, so the offline rules are not a default it can
    honour - they would fail at the first arrival - and neither is a recipe built on them.
    """
    named = os.environ.get("WAJO_PROVIDER", "")
    if named in PROVIDER_CHOICES and not named.startswith(RuleProvider.name):
        return named
    return "openrouter" if "openrouter" in ENDPOINTS else next(iter(ENDPOINTS), "openrouter")


def _provider_for(args: argparse.Namespace, *, model: str | None = None) -> ProposalProvider:
    """The proposer one name asks for: an endpoint, or an endpoint with Jev routing it."""
    return proposing_provider(args.provider, model=model or getattr(args, "model", None))


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
        choices=PROVIDER_CHOICES,
        default=_default_provider(),
        help=(
            "who proposes: the offline rule stand-in, a model endpoint, or an endpoint "
            "with a decision model in front of it ('openrouter+jev' asks Jev for the "
            "four-way route and the model for the work, with the decision model named by "
            f"WAJO_JEV_MODEL, default {DEFAULT_JEV_MODEL}). Keys go in .env, and "
            "WAJO_PROVIDER sets the default for every command"
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
    target.add_argument(
        "--rule-ttl-days",
        type=float,
        default=0.0,
        metavar="DAYS",
        help=(
            "retire rules nobody has restated in DAYS days, and say how many went; "
            "0 (the default) keeps every rule in force, because retiring the user's own "
            "words is a decision a run has to ask for"
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
    ttl = float(getattr(args, "rule_ttl_days", 0.0) or 0.0)
    store = ClaimStore(grant=grant, path=args.store, ttl_days=ttl)
    if ttl:
        store.retire(store.expired(), reason="expired")
    return store


def _proposing(provider: ProposalProvider, store: ClaimStore) -> ProposalGateway:
    """The pipeline's proposer: a rule already confirmed answers before the provider does."""
    return ProposalGateway(RememberedProvider(store, provider))


def data_validate(args: argparse.Namespace, out: IO[str]) -> int:
    """Print what a case set holds and everything wrong with it."""
    report = validate_cases(args.path)
    out.write(report.render() + "\n")
    return 0 if report.ok else 1


def eval_all(args: argparse.Namespace, out: IO[str]) -> int:
    """Teach the calibration lane, freeze it, and score the sealed lane once."""
    manifest = Manifest.load(args.fixture)
    provider = _provider_for(args)
    label = str(getattr(provider, "label", None) or getattr(provider, "name", provider))
    sink = TraceSink(args.trace) if args.trace else None
    try:
        outcome = run_eval(
            manifest.view(Lane.CALIBRATION),
            manifest.view(Lane.HELD_OUT),
            script_path=args.script,
            seed=args.seed,
            provider=provider,
            out=args.out,
            block=args.block,
            trace=sink,
        )
    finally:
        if sink is not None:
            sink.close()
    out.write(
        f"fixture: {manifest.source}\n"
        f"digest: {manifest.dataset_digest[:16]}\n"
        f"proposal source: the {label} proposal\n"
        f"{render_eval(outcome)}\n"
        # The third report the exit gate asks for: what the run spent getting there.
        f"\ncost:\n{LEDGER.render()}\n"
    )
    if sink is not None:
        out.write(f"trace: {sink.lines} line(s) in {sink.path}\n")
    return 0 if outcome.held_out.gates_ok else 1


def _policy(
    args: argparse.Namespace, store: ClaimStore
) -> tuple[DecisionSource, str]:
    """Pick the decision source and name it. Labels are a reference mode, not the default."""
    if args.policy == "labels":
        return GoldPolicy(), "the dataset's labels (reference)"
    provider = _provider_for(args)
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
    if store.retired:
        out.write(
            f"    {store.retired} retired: nobody has restated them in "
            f"{args.rule_ttl_days:g} day(s)\n"
        )


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
    learner = None if args.no_learn else Learner()
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
                learner=learner,
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
    provider = _provider_for(args)
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
    baseline = report.without_rules
    out.write(
        f"\n[pass 2] autonomous: the same lane and seed, with {len(report.claims)} kept "
        "rule(s) answering before the provider\n"
    )
    for index, case_id in enumerate(report.autonomous.order, start=1):
        message = view.open(case_id).event.message
        committed = case_id in {item.case_id for item in report.autonomous.receipts}
        ended = "committed" if committed else report.autonomous.interrupts.get(case_id, "")
        was = None if baseline is None else baseline.routes.get(case_id)
        mark = "  <- from a rule" if message.message_id in recalled else ""
        if mark and was is not None and was != report.autonomous.routes.get(case_id):
            mark = f"{mark} (was {was})"
        out.write(
            f"[{index:>3}/{len(report.autonomous.order)}] {case_id}  "
            f"{report.autonomous.routes.get(case_id, ''):<24} {ended}{mark}\n"
        )
    out.write(
        f"\nasked for a line: {report.asked_before} in pass 1, {report.asked_after} in pass 2\n"
        f"receipts: {len(report.calibration.receipts)} in pass 1, "
        f"{len(report.autonomous.receipts)} in pass 2\n"
    )
    _rule_effect(report, out)
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


def _rule_effect(report: LoopReport, out: IO[str]) -> None:
    """What the rules answered, and what the same lane would have done without them."""
    if not report.answered:
        return
    taught = sum(1 for case_id, source in report.answered.items() if case_id == source)
    out.write(
        f"\nthe rules answered {len(report.answered)} arrival(s): {taught} the mail they were "
        f"taught on, {len(report.answered) - taught} that came later\n"
    )
    if report.without_rules is None:
        return
    out.write(
        f"with the same lane run with no rules at all: {report.asked_without_rules} arrival(s) "
        f"would have waited, so the rules saved {report.saved} ask(s) and moved "
        f"{len(report.changed)} route(s), {len(report.changed_later)} of them after the mail "
        "that taught them\n"
    )
    changed = "\n".join(
        f"    {case_id}  {report.without_rules.routes.get(case_id, '')} -> "
        f"{report.autonomous.routes.get(case_id, '')}"
        for case_id in report.changed
    )
    if changed:
        out.write(f"the rules moved:\n{changed}\n")


def graph_run(args: argparse.Namespace, out: IO[str]) -> int:
    """Walk a fixture through the decision graph and say what each arrival ended in."""
    manifest = (
        Manifest.load(args.mail, mail_only=True) if args.mail else Manifest.load(args.fixture)
    )
    view = manifest.view(Lane(args.lane))
    cases = view.cases
    provider = _provider_for(args)
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
        # The draft the ask carries, printed where the wait is: reading the run should show
        # what is being asked about, not only that something is.
        decided = session.context.decisions.get(item.case_id)
        draft = decided.predraft if decided is not None else None
        if draft is not None:
            out.write("\n".join(f"    {line}" if line else "" for line in draft.lines()) + "\n")
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
    if (args.command, getattr(args, "eval_command", None)) == ("eval", "all"):
        try:
            return eval_all(args, out)
        except KeyboardInterrupt:
            out.write("\nstopped before the evaluation finished\n")
            return 130
        except (
            ProposalError,
            ManifestError,
            SplitViolation,
            TraceError,
            ClaimError,
            ScoringError,
            OSError,
        ) as error:
            # Foreseeable operational failures get one readable line, not a traceback.
            out.write(f"cannot evaluate: {error}\n")
            return 2
    if (args.command, getattr(args, "data_command", None)) == ("data", "validate"):
        try:
            return data_validate(args, out)
        except (ManifestError, OSError) as error:
            out.write(f"cannot validate: {error}\n")
            return 2
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
    if (args.command, getattr(args, "sandbox_command", None)) == ("sandbox", "run"):
        try:
            return sandbox_run_command(args, out)
        except KeyboardInterrupt:
            out.write("\nstopped before the mailbox finished\n")
            return 130
        except (
            SandboxError,
            ProposalError,
            ManifestError,
            SplitViolation,
            TraceError,
            ClaimError,
            ScoringError,
            OSError,
        ) as error:
            # Foreseeable operational failures get one readable line, not a traceback.
            out.write(f"cannot run the sandbox: {error}\n")
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


__all__ = ["build_parser", "main", "sandbox_run_command", "sim_run"]
