"""The case set's own checks: counts, enums, and nothing in two lanes.

``wajo data validate`` is the first step of the release evidence, so each of its checks
is pinned here against a case set that breaks exactly that one thing. Most error tests
assert the whole code set, so a check that quietly started firing on everything else
would fail here rather than pass over it. The leak test carries a control: the dataset
this case set was promoted from has those two scenarios in both lanes, and the check
has to be able to say so without calling every repeated sender a leak.
"""
import hashlib
import json
from argparse import Namespace
from copy import deepcopy
from io import StringIO
from pathlib import Path

import pytest

from agent.cli import data_validate
from agent.dataset import (
    DEFAULT_DATASET_PATH,
    SCHEMA_VERSION,
    ManifestError,
    validate_cases,
)


def _rows() -> list[dict]:
    """The committed case set, as mutable rows."""
    assert DEFAULT_DATASET_PATH.exists(), f"case set missing at {DEFAULT_DATASET_PATH}"
    with open(DEFAULT_DATASET_PATH, encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def _row(rows: list[dict], split: str, *, case_id: str | None = None) -> dict:
    """One row from a split, optionally a named one."""
    for row in rows:
        if row["split"] == split and (case_id is None or row["case_id"] == case_id):
            return deepcopy(row)
    raise AssertionError(f"no {split} row" + (f" {case_id}" if case_id else ""))


def _extra(row: dict, number: int, *, thread: bool = True) -> dict:
    """Give a copied row its own identity, so only the intended check can complain."""
    row.update({"case_id": f"WAJO-90{number:02d}", "sequence_index": 9000 + number})
    row["incoming_email"]["message_id"] = f"msg-in-wajo-90{number:02d}"
    if thread:
        row["thread"]["thread_id"] = f"th-wajo-90{number:02d}"
    return row


def _written(tmp_path: Path, rows: list[dict]) -> Path:
    """Write rows as a case set and hand back its path."""
    path = tmp_path / "cases.jsonl"
    path.write_text(
        "\n".join(json.dumps(row) for row in rows) + "\n", encoding="utf-8", newline="\n"
    )
    return path


def _codes(report) -> set[str]:
    return {problem.code for problem in report.problems}


def test_the_committed_case_set_validates_and_says_what_it_holds():
    """The plan's check: the two lanes are counted, and the file exits clean."""
    report = validate_cases(DEFAULT_DATASET_PATH)

    assert report.ok, report.render()
    assert report.split_counts["learning_stream"] == 60
    assert report.split_counts["golden_ordinary"] == 38
    assert report.split_counts["golden_adversarial"] == 20
    assert report.split_counts["development"] == 20
    assert (report.learning, report.sealed, report.total) == (60, 58, 138)
    assert report.digest == hashlib.sha256(DEFAULT_DATASET_PATH.read_bytes()).hexdigest()


def test_a_scenario_in_two_lanes_is_a_leak_even_with_a_rewritten_body(tmp_path):
    """The learn-then-test pair has to be gone, not merely reworded.

    Two sealed rows in the source dataset were copies of learning scenarios - the same
    sender and subject with a placeholder body - so the learner was taught the answer to
    a question the held-out run then asked again.
    """
    rows = _rows()
    leak = _extra(_row(rows, "learning_stream", case_id="WAJO-0007"), 1)
    leak.update({"split": "golden_ordinary"})
    leak["observed_user_feedback"].update({"kind": "none", "explicit_for_learning": False})

    report = validate_cases(_written(tmp_path, [*rows, leak]))

    assert _codes(report) == {"SPLIT_LEAK"}
    assert report.problems[0].case_id == "WAJO-9001"


def test_a_different_subject_is_not_a_leak(tmp_path):
    """The control: the check keys on the scenario, so a new subject is a new case."""
    rows = _rows()
    fresh = _extra(_row(rows, "learning_stream", case_id="WAJO-0007"), 2)
    fresh.update({"split": "golden_ordinary"})
    fresh["incoming_email"]["subject"] = "Quarterly capacity review"
    fresh["observed_user_feedback"].update({"kind": "none", "explicit_for_learning": False})

    report = validate_cases(_written(tmp_path, [*rows, fresh]))

    assert report.ok, report.render()
    assert report.sealed == 59


def test_a_thread_in_two_lanes_is_a_leak(tmp_path):
    """A thread carries its own history, so a repeat reveals an earlier lane's mail."""
    rows = _rows()
    copied = _extra(_row(rows, "learning_stream", case_id="WAJO-0007"), 3, thread=False)
    thread_id = copied["thread"]["thread_id"]
    copied.update({"split": "golden_ordinary"})
    copied["incoming_email"]["subject"] = "Nothing to do with the thread above"
    copied["observed_user_feedback"].update({"kind": "none", "explicit_for_learning": False})

    report = validate_cases(_written(tmp_path, [*rows, copied]))

    assert _codes(report) == {"SPLIT_LEAK"}
    assert report.problems[0].case_id == "WAJO-9003"
    assert thread_id in report.problems[0].detail


def test_a_sealed_case_carrying_feedback_is_refused(tmp_path):
    """The held-out run freezes the learner: a sealed row that teaches contradicts it."""
    rows = _rows()
    sealed = _extra(_row(rows, "golden_ordinary"), 4)
    sealed.update({"split": "golden_ordinary"})
    sealed["observed_user_feedback"].update({"kind": "approve", "explicit_for_learning": True})

    report = validate_cases(_written(tmp_path, [*rows, sealed]))

    assert _codes(report) == {"SEALED_FEEDBACK"}
    assert report.problems[0].case_id == "WAJO-9004"


def test_an_unimplemented_action_may_only_be_gold_escalated(tmp_path):
    """A typo in an action id looks exactly like a fence test, so the gold route decides."""
    rows = _rows()
    typo = _extra(_row(rows, "learning_stream"), 5)
    typo["canonical_candidate_action"]["action_id"] = "email.apply_labl"

    report = validate_cases(_written(tmp_path, [*rows, typo]))

    assert _codes(report) == {"UNKNOWN_ACTION"}
    assert "email.apply_labl" in report.problems[0].detail


def test_a_fenced_action_is_fine_when_the_gold_escalates(tmp_path):
    """The control: the case set tests the fence with ids nothing implements, on purpose."""
    rows = _rows()
    fenced = _row(rows, "golden_adversarial")
    assert fenced["canonical_candidate_action"]["action_id"] == "unsupported"

    report = validate_cases(_written(tmp_path, rows))

    assert "UNKNOWN_ACTION" not in _codes(report)


def test_every_enum_is_checked_against_the_code(tmp_path):
    """Splits, routes, ceilings and feedback kinds are the code's own vocabularies."""
    rows = _rows()

    def mutated(path: str, value: str, number: int) -> dict:
        """One development row with a dotted field replaced."""
        row = _extra(_row(rows, "development"), number)
        holders: list[dict] = [row]
        for step in path.split(".")[:-1]:
            holders.append(holders[-1][step])
        holders[-1][path.split(".")[-1]] = value
        return row

    report = validate_cases(
        _written(
            tmp_path,
            [
                *rows,
                mutated("split", "golden_test", 6),
                mutated("gold.autonomy_outcome", "PROCEED", 7),
                mutated("safety_floor.autonomy_ceiling", "SILENT", 8),
                mutated("observed_user_feedback.kind", "sounds_good", 9),
            ],
        )
    )

    assert {"UNKNOWN_SPLIT", "UNKNOWN_ROUTE", "UNKNOWN_CEILING", "UNKNOWN_FEEDBACK"} <= _codes(
        report
    )


def test_another_schema_version_is_refused_rather_than_read(tmp_path):
    """A v2 row read as v1 is a wrong answer, not a parse failure."""
    rows = _rows()
    rows[0]["schema_version"] = "wajo_dataset_v2"

    report = validate_cases(_written(tmp_path, rows))

    assert _codes(report) == {"SCHEMA_VERSION"}
    assert report.problems[0].case_id == rows[0]["case_id"]


def test_duplicate_ids_and_sequence_indices_are_caught(tmp_path):
    """Two cases in one sequence slot sort by luck, and one of them scores the other."""
    rows = _rows()
    twin = deepcopy(rows[0])
    twin["split"] = rows[1]["split"]

    report = validate_cases(_written(tmp_path, [*rows, twin]))

    assert {"DUPLICATE_CASE_ID", "DUPLICATE_SEQUENCE"} <= _codes(report)


def test_a_missing_field_is_named_by_path(tmp_path):
    """A bare KeyError names no case; the report has to name the row and the field."""
    rows = _rows()
    del rows[0]["gold"]

    report = validate_cases(_written(tmp_path, rows))

    assert any(
        problem.code == "MISSING_FIELD"
        and problem.case_id == rows[0]["case_id"]
        and "gold.autonomy_outcome" in problem.detail
        for problem in report.problems
    )


def test_a_case_set_below_the_lane_minimums_is_refused(tmp_path):
    """Both lanes have floors: below them a report is one lucky case, not a measurement."""
    rows = [_row(_rows(), "learning_stream"), _row(_rows(), "golden_ordinary")]
    rows[1]["case_id"] = "WAJO-9100"

    report = validate_cases(_written(tmp_path, rows))

    assert {problem.case_id for problem in report.problems if problem.code == "TOO_FEW_CASES"} == {
        "calibration",
        "held_out",
    }


def test_a_placeholder_body_warns_without_failing(tmp_path):
    """A generator placeholder still scores, but triage sees no text: say so, don't fail."""
    rows = _rows()
    rows[0]["incoming_email"]["body"] = "Detailed email body according to scenario..."

    report = validate_cases(_written(tmp_path, rows))

    assert report.ok, report.render()
    assert any(
        warning.code == "PLACEHOLDER_BODY" and warning.case_id == rows[0]["case_id"]
        for warning in report.warnings
    )


def test_a_broken_line_is_reported_by_its_number(tmp_path):
    """One unparseable line is a typo, not a reason to give up on the other rows."""
    good = DEFAULT_DATASET_PATH.read_text(encoding="utf-8").splitlines()[0]
    path = tmp_path / "cases.jsonl"
    path.write_text(f"{good}\n{{not json}}\n", encoding="utf-8", newline="\n")

    assert "NOT_JSON" in _codes(validate_cases(path))


def test_a_row_that_is_not_an_object_is_reported_rather_than_crashing(tmp_path):
    """A JSONL file is easy to over-edit: a bare list has to be a report, not a traceback."""
    good = DEFAULT_DATASET_PATH.read_text(encoding="utf-8").splitlines()[0]
    path = tmp_path / "cases.jsonl"
    path.write_text(f"{good}\n[1, 2, 3]\n", encoding="utf-8", newline="\n")

    assert "ROW_SHAPE" in _codes(validate_cases(path))


def test_the_command_exits_zero_on_the_case_set_and_nonzero_on_a_broken_one(tmp_path):
    """The plan's exit gate: `wajo data validate <path>` prints and returns a status."""
    clean = StringIO()
    assert data_validate(Namespace(path=str(DEFAULT_DATASET_PATH)), clean) == 0
    assert "learning 60  sealed 58" in clean.getvalue()

    rows = _rows()
    rows[0]["split"] = "golden_test"
    broken = StringIO()
    assert data_validate(Namespace(path=str(_written(tmp_path, rows))), broken) == 1
    assert "failed:" in broken.getvalue()


def test_an_unreadable_path_says_which_path(tmp_path):
    """A missing file is the most likely way this command is used wrong."""
    absent = tmp_path / "absent.jsonl"

    with pytest.raises(ManifestError) as caught:
        validate_cases(absent)

    assert str(absent) in str(caught.value)


def test_the_case_set_declares_the_version_the_loader_reads():
    """One schema version, named once, so an upgrade is a change and not a surprise."""
    assert {row["schema_version"] for row in _rows()} == {SCHEMA_VERSION}
