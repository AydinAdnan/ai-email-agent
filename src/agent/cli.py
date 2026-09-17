"""Command-line entry point (Phase 3.4).

``wajo sim run`` replays a fixture as a chat: arrivals stream in on one task while
stdin is read on another, and the run stops only where the safety floor says the
user is needed. Everything else — printing, parsing flags — is stdlib.
"""
import argparse
import asyncio
import sys
from collections.abc import Sequence
from typing import IO

from agent.dataset import (
    DEFAULT_DATASET_PATH,
    Lane,
    Manifest,
    ManifestError,
    SplitViolation,
)
from agent.gateway import ProposalError, ProposalGateway, build_provider
from agent.sim.policy import GoldPolicy, ProposalPolicy
from agent.sim.runner import DecisionSource, run_simulation

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
    run.add_argument(
        "--fixture",
        default=str(DEFAULT_DATASET_PATH),
        help="JSONL dataset or fixture to replay (default: the full dataset)",
    )
    run.add_argument(
        "--mail",
        metavar="PATH",
        help=(
            "replay plain mail instead of a dataset: one JSON object per message with "
            "sender, to, subject and body. Such rows carry no labels, so nothing is scored"
        ),
    )
    run.add_argument("--seed", type=int, default=7, help="seed for the deterministic clock")
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
    run.add_argument(
        "--provider",
        choices=["rules", "openai"],
        default="rules",
        help="who proposes: the offline rule stand-in, or a model when OPENAI_API_KEY is set",
    )
    run.add_argument(
        "--lane",
        choices=[lane.value for lane in SIM_LANES],
        default=Lane.CALIBRATION.value,
        help=(
            "which split to replay (default: the calibration lane); the sealed "
            "held-out lane is not offered, only the eval run may open it"
        ),
    )
    return parser


def _view_note(show_labels: bool, policy: str, provider: str) -> str:
    """Say what the reader is looking at, since labels change the calibration."""
    if show_labels:
        return "labels are on: each arrival carries the dataset's answer next to the pipeline's"
    source = (
        "the dataset's labels (reference)" if policy == "labels" else f"the {provider} proposal"
    )
    return f"each arrival is shown as mail, with routes from {source}"


def _policy(args: argparse.Namespace) -> DecisionSource:
    """Pick the decision source. Reading labels is a reference mode, not the default."""
    if args.policy == "labels":
        return GoldPolicy()
    return ProposalPolicy(ProposalGateway(build_provider(args.provider)))


def sim_run(args: argparse.Namespace, out: IO[str]) -> int:
    """Replay a fixture or a plain mail stream through the chat loop."""
    manifest = (
        Manifest.load(args.mail, mail_only=True) if args.mail else Manifest.load(args.fixture)
    )
    view = manifest.view(Lane(args.lane))
    cases = view.cases
    out.write(
        f"fixture: {manifest.source}\n"
        f"lane: {view.lane.value}  cases: {len(cases)}  seed: {args.seed}\n"
        f"digest: {manifest.dataset_digest[:16]}\n"
        "type a line when a decision waits for you; lines already typed are "
        "corrections, bound to the decision they followed\n"
        f"{_view_note(args.show_labels, args.policy, args.provider)}\n\n"
    )
    policy = _policy(args)
    outcome = asyncio.run(
        run_simulation(
            view, seed=args.seed, out=out, policy=policy, show_labels=args.show_labels
        )
    )
    return 0 if outcome.processed == len(cases) else 1


def main(argv: Sequence[str] | None = None) -> int:
    """Entry point for the ``wajo`` console script."""
    args = build_parser().parse_args(argv)
    out = sys.stdout
    if (args.command, getattr(args, "sim_command", None)) == ("sim", "run"):
        try:
            return sim_run(args, out)
        except KeyboardInterrupt:
            out.write("\nstopped before the run finished\n")
            return 130
        except (ProposalError, ManifestError, SplitViolation, OSError) as error:
            # Foreseeable operational failures get one readable line, not a traceback.
            out.write(f"cannot run: {error}\n")
            return 2
    return 2


__all__ = ["build_parser", "main", "sim_run"]
