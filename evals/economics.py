"""What a run costs, stage by stage (plan Commit 8.4).

Cost is the one number a reviewer cannot check by reading the design, so this runs the
same two lanes the eval runs and prints what that run actually spent: calls and tokens
per stage, an estimated cost at the model's published rate, and the deflection rate -
the arrivals the deterministic layer settled before any provider was asked.

    uv run python -m evals.economics
    uv run python -m evals.economics --provider openrouter
"""
from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from dotenv import load_dotenv

from agent.dataset import DEFAULT_DATASET_PATH, Lane, Manifest
from agent.gateway import ENDPOINTS, ProposalError, build_provider
from agent.usage import LEDGER
from evals.harness import ScoringError
from evals.run_eval import DEFAULT_SCRIPT, run_eval

DEFAULT_OUT = Path("artifacts") / "economics"
# The repository root, named rather than discovered: a search from this file's frame
# finds whatever .env happens to sit beside the caller instead of this project's.
ROOT = Path(__file__).resolve().parents[1]


def main(argv: Sequence[str] | None = None) -> int:
    """Run the lanes, then print what they cost."""
    parser = argparse.ArgumentParser(
        prog="python -m evals.economics",
        description="the per-stage cost of one evaluation run, and how much of it was avoided",
    )
    parser.add_argument("--fixture", default=str(DEFAULT_DATASET_PATH), help="the case set")
    parser.add_argument("--script", default=str(DEFAULT_SCRIPT), help="the teaching transcript")
    parser.add_argument(
        "--out", default=str(DEFAULT_OUT), help="where this run's artifacts go (kept apart from the eval)"
    )
    parser.add_argument("--seed", type=int, default=7, help="seed for both lane runs")
    parser.add_argument(
        "--provider",
        choices=["rules", *ENDPOINTS],
        default="rules",
        help="who proposes: the offline rules cost no tokens, a model endpoint does",
    )
    parser.add_argument("--model", help="model id to use; falls back to WAJO_MODEL")
    args = parser.parse_args(argv)

    # A model endpoint needs its key, and the key lives in .env; without this the file
    # sits there looking authoritative while the provider reports no key at all.
    load_dotenv(ROOT / ".env")
    try:
        manifest = Manifest.load(args.fixture)
        provider = build_provider(args.provider, model=args.model)
    except (ProposalError, ValueError, OSError) as error:
        sys.stderr.write(f"cannot run: {error}\n")
        return 1
    label = str(getattr(provider, "label", None) or getattr(provider, "name", provider))

    try:
        outcome = run_eval(
            manifest.view(Lane.CALIBRATION),
            manifest.view(Lane.HELD_OUT),
            script_path=args.script,
            seed=args.seed,
            provider=provider,
            out=args.out,
        )
    except ScoringError as error:
        sys.stderr.write(f"cannot run: {error}\n")
        return 1

    sys.stdout.write(
        "\n".join(
            [
                f"fixture: {manifest.source}",
                f"proposal source: the {label} proposal",
                f"lanes: calibration {outcome.lanes['calibration']} case(s), "
                f"sealed {outcome.lanes['sealed']} case(s)  seed {outcome.seed}",
                "",
                LEDGER.render(),
                "",
                f"hard gates: {'PASS' if outcome.held_out.gates_ok else 'FAIL'} "
                f"(the counts are in {outcome.report_path.name}; wajo eval all prints them)",
                f"artifacts: {outcome.out}",
            ]
        )
        + "\n"
    )
    # A cost report is still a report on a run: a run whose gates failed is not a pass
    # just because this command is about money.
    return 0 if outcome.held_out.gates_ok else 1


if __name__ == "__main__":  # pragma: no cover - the module's own entry point
    raise SystemExit(main())
