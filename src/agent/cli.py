"""Command-line entry point (Phase 3.4).

``wajo sim run`` replays a fixture as a chat: arrivals stream in on one task while
stdin is read on another, and the run stops only where the safety floor says the
user is needed. Everything else — printing, parsing flags — is stdlib.
"""
import argparse
import asyncio
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import IO

from dotenv import load_dotenv

from agent.dataset import (
    DEFAULT_DATASET_PATH,
    Lane,
    Manifest,
    ManifestError,
    SplitViolation,
)
from agent.gateway import ENDPOINTS, ProposalError, ProposalGateway, build_provider
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
    run.add_argument(
        "--seed",
        type=int,
        default=7,
        help="seed for the deterministic clock and the order inside each arrival window",
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
    run.add_argument(
        "--provider",
        choices=["rules", *ENDPOINTS],
        default="rules",
        help=(
            "who proposes: the offline rule stand-in, or a model endpoint "
            "(its key goes in .env at the repository root)"
        ),
    )
    run.add_argument(
        "--model",
        help="model id to use; falls back to WAJO_MODEL, then the endpoint's default",
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


def _view_note(show_labels: bool) -> str:
    """Say what the reader is looking at, since labels change the calibration."""
    if show_labels:
        return "labels are on: each arrival carries the dataset's answer next to the pipeline's"
    return "each arrival is shown as mail: sender, subject and body only"


def _policy(args: argparse.Namespace) -> tuple[DecisionSource, str]:
    """Pick the decision source and name it. Labels are a reference mode, not the default."""
    if args.policy == "labels":
        return GoldPolicy(), "the dataset's labels (reference)"
    provider = build_provider(args.provider, model=args.model)
    label = str(getattr(provider, "label", None) or getattr(provider, "name", provider))
    return ProposalPolicy(ProposalGateway(provider)), f"the {label} proposal"


def sim_run(args: argparse.Namespace, out: IO[str]) -> int:
    """Replay a fixture or a plain mail stream through the chat loop."""
    manifest = (
        Manifest.load(args.mail, mail_only=True) if args.mail else Manifest.load(args.fixture)
    )
    view = manifest.view(Lane(args.lane))
    cases = view.cases
    policy, source = _policy(args)
    out.write(
        f"fixture: {manifest.source}\n"
        f"lane: {view.lane.value}  cases: {len(cases)}  seed: {args.seed}\n"
        f"digest: {manifest.dataset_digest[:16]}\n"
        f"proposal source: {source}\n"
        "type a line when a decision waits for you; lines already typed are "
        "corrections, bound to the decision they followed\n"
        f"{_view_note(args.show_labels)}\n\n"
    )
    outcome = asyncio.run(
        run_simulation(
            view, seed=args.seed, out=out, policy=policy, show_labels=args.show_labels
        )
    )
    return 0 if outcome.processed == len(cases) else 1


def main(argv: Sequence[str] | None = None) -> int:
    """Entry point for the ``wajo`` console script."""
    # A key in .env is what makes --provider openrouter runnable; without this the file
    # sits there looking authoritative while the provider reports no key. The path is
    # named rather than discovered: this file lives two levels below the repository
    # root, and a search from the caller's frame finds a .env somewhere else or none.
    load_dotenv(Path(__file__).resolve().parents[2] / ".env")
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
