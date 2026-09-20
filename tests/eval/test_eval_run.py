"""The eval run: teach the learning lane, freeze it, then score the sealed lane once.

What these pin is the order and the firewall rather than the numbers - the numbers are the
report's business and they move with the case set. The sealed lane has to be handed a
learner that is no longer moving, has to teach it nothing, and has to decide the same way
twice, or the report it produces is a measurement of itself.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from agent.autonomy import state as learner_state
from agent.dataset import DEFAULT_DATASET_PATH, Lane, Manifest
from evals.harness import ScoringError
from evals.run_eval import ScriptedTeaching, load_script, run_eval

# An approval of the work the agent prepared, which is what most teaching looks like.
TAUGHT_LINE = "yes"


def _rows(split: str, count: int) -> list[dict]:
    """The first few committed rows of one split, so the test runs on the real case set."""
    chosen = []
    for line in DEFAULT_DATASET_PATH.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if row.get("split") == split:
            chosen.append(row)
        if len(chosen) == count:
            break
    assert chosen, f"the case set carries no {split} rows"
    return chosen


def mini_manifest(*, calibration: int = 12, sealed: int = 3, adversarial: int = 2) -> Manifest:
    """A tiny two-lane manifest built from the committed rows.

    The adversarial rows are in it on purpose: the escalation gate fails on an empty
    adversarial set, so a mini lane without them would fail a gate for having no data.
    """
    return Manifest.from_rows(
        _rows("learning_stream", calibration)
        + _rows("golden_ordinary", sealed)
        + _rows("golden_adversarial", adversarial),
        source="<mini case set>",
    )


def mini_script(manifest: Manifest) -> ScriptedTeaching:
    """One approval, typed at the mail the case set says deserves a question.

    A line is released only while its decision is on screen, so the case has to be one the
    agent actually asks about - which is what a gold ask-first row is for.
    """
    case = next(
        case
        for case in manifest.view(Lane.CALIBRATION).cases
        if case.row["gold"]["autonomy_outcome"] == "ASK_FIRST_WITH_PREDRAFT"
    )
    return ScriptedTeaching(
        name="one approval, typed where it is asked for",
        description="a single reply at the first mail the agent asks about",
        replies=({"case": case.case_id, "lines": [TAUGHT_LINE]},),
    )


def evaluate(tmp_path: Path, manifest: Manifest | None = None):
    built = manifest if manifest is not None else mini_manifest()
    return run_eval(
        built.view(Lane.CALIBRATION),
        built.view(Lane.HELD_OUT),
        script=mini_script(built),
        seed=7,
        out=tmp_path / "eval",
    )


def test_the_sealed_lane_is_scored_after_the_freeze_and_teaches_nothing(tmp_path: Path):
    outcome = evaluate(tmp_path)

    assert outcome.held_out.learning_writes == 0
    assert outcome.held_out.total == len(outcome.held_out.order)
    assert outcome.held_out.gates_ok, outcome.held_out.render()
    # The freeze happened before the sealed lane ran, and it holds what teaching taught.
    frozen = json.loads(outcome.learner_path.read_text(encoding="utf-8"))
    assert frozen["version"] == learner_state.FREEZE_VERSION
    assert frozen["learner"]["counts"], "the calibration lane taught the learner nothing"


def test_the_artifacts_are_the_report_the_run_returned(tmp_path: Path):
    outcome = evaluate(tmp_path)
    written = json.loads(outcome.report_path.read_text(encoding="utf-8"))
    assert {key: value for key, value in written.items() if key != "provenance"} == (
        outcome.report.as_dict()
    )
    assert written["provenance"]["floor_version"], "a report has to name its policy versions"
    assert outcome.rules_path.exists(), "the run has to keep the rules it confirmed"


def test_the_same_seed_decides_the_same_way_twice(tmp_path: Path):
    first = evaluate(tmp_path / "first")
    second = evaluate(tmp_path / "second")
    assert first.report.as_dict() == second.report.as_dict()
    assert first.learner_path.read_bytes() == second.learner_path.read_bytes()


def test_the_gates_are_in_the_report_as_data(tmp_path: Path):
    """A build fails on the report, so the pass marks have to be machine-readable."""
    outcome = evaluate(tmp_path)
    written = json.loads(outcome.report_path.read_text(encoding="utf-8"))
    assert written["gates_ok"] is True
    assert {gate["name"] for gate in written["gates"]} == {
        "learning writes in the sealed lane",
        "floor violations",
        "adversarial escalation",
    }
    assert all(isinstance(gate["ok"], bool) for gate in written["gates"])


def test_a_transcript_with_no_replies_is_refused(tmp_path: Path):
    empty = tmp_path / "empty.json"
    empty.write_text(json.dumps({"replies": []}), encoding="utf-8")
    with pytest.raises(ScoringError, match="no replies"):
        load_script(empty)


def test_a_transcript_reply_with_no_lines_is_refused(tmp_path: Path):
    thin = tmp_path / "thin.json"
    thin.write_text(json.dumps({"replies": [{"case": "WAJO-0001"}]}), encoding="utf-8")
    with pytest.raises(ScoringError, match="at least one line"):
        load_script(thin)
