from __future__ import annotations

import asyncio
import io
import json
import re
from collections.abc import Sequence
from pathlib import Path

from agent.cli import build_parser, graph_run, loop_run, sim_run
from agent.dataset import DEFAULT_DATASET_PATH, Lane, LaneView, Manifest
from agent.loop import LoopReport, ScriptedReplies, run_loop
from agent.memory.claims import ClaimStore
from agent.memory.consent import session_grant
from agent.sim.policy import route_decision
from agent.triage import triage

FIXTURE = Path(__file__).parent / "fixtures" / "stream_12.jsonl"

# The recruiter follow-up: an ask-first case, which is where a rule can be heard.
RECRUITER_CASE = "WAJO-0008"
RECRUITER_SENDER = "claire@nexustalent.synthetic.example"

# The wire-transfer invoice: an unknown vendor asking for money. Nothing the user says
# about that sender may make the agent handle it on its own.
WIRE_CASE = "WAJO-0011"
WIRE_SENDER = "billing@officesupply.synthetic.example"


def view() -> LaneView:
    return Manifest.load(FIXTURE).view(Lane.CALIBRATION)


def loop(script: Sequence[str] = ()) -> tuple[LoopReport, str]:
    out = io.StringIO()
    report = asyncio.run(
        run_loop(
            view(),
            seed=7,
            out=out,
            script=script,
            store=ClaimStore(grant=session_grant(purpose="test session")),
        )
    )
    return report, out.getvalue()


def recruiter_lane() -> LaneView:
    """The whole class of recruiter arrivals, in order, and nothing else beside it."""
    full = Manifest.load(DEFAULT_DATASET_PATH)
    rows = [
        case.row
        for case in full.cases
        if (case.row.get("incoming_email") or {}).get("intent") == "recruiter follow-up"
    ]
    return Manifest.from_rows(
        rows, source="recruiter arrivals", dataset_digest=full.dataset_digest
    ).view(Lane.CALIBRATION)


def test_a_rule_taught_on_one_arrival_decides_the_ones_that_come_later():
    """The learning claim, measured: one correction about a class, four quieter arrivals.

    The teaching mail is not evidence - a rule answering its own case changed nothing for
    anybody else. The four recruiter arrivals after it are, and they are counted against
    the same lane run with no rules at all rather than assumed from the ask totals.
    """
    view = recruiter_lane()
    report = asyncio.run(
        run_loop(
            view,
            seed=7,
            out=io.StringIO(),
            script=[f"{RECRUITER_CASE}=always file recruiter follow-ups silently; yes"],
            store=ClaimStore(grant=session_grant(purpose="test session")),
        )
    )

    later = {case.case_id for case in view.cases if case.case_id != RECRUITER_CASE}
    assert len(later) == 4, later
    assert set(report.answered) == later | {RECRUITER_CASE}
    assert set(report.answered.values()) == {RECRUITER_CASE}
    assert set(report.changed_later) == later
    assert report.without_rules is not None
    for case_id in later:
        assert report.without_rules.routes[case_id] == "ASK_FIRST_WITH_PREDRAFT"
        assert report.autonomous.routes[case_id] == "PROCEED_SILENTLY"
        assert case_id not in report.autonomous.interrupts
    # Five arrivals a rule answered, five asks the lane would have waited on without it.
    assert report.saved == 5


def asked(text: str) -> tuple[int, int]:
    found = re.search(r"asked for a line: (\d+) in pass 1, (\d+) in pass 2", text)
    assert found is not None, text[-400:]
    return int(found.group(1)), int(found.group(2))


def test_a_rule_stated_in_the_first_pass_answers_the_second():
    report, text = loop([f"{RECRUITER_CASE}=ignore mail from {RECRUITER_SENDER}; yes"])

    assert [claim.describe() for claim in report.claims], text
    assert report.recalled, text
    assert report.autonomous.routes[RECRUITER_CASE] == "PROCEED_SILENTLY"
    assert RECRUITER_CASE not in report.autonomous.interrupts
    assert report.asked_after == report.asked_before - 1


def test_a_rule_cannot_open_a_route_the_floor_closed():
    report, text = loop([f"{WIRE_CASE}=ignore mail from {WIRE_SENDER}; yes"])

    # The rule was heard and kept, which is what makes the assertion worth having:
    # memory is consulted, and the floor still refuses what the mail compels.
    assert [claim.scope.sender for claim in report.claims] == [WIRE_SENDER], text
    assert report.autonomous.routes[WIRE_CASE] == "ESCALATE"
    assert WIRE_CASE in report.autonomous.interrupts
    assert report.asked_after == report.asked_before


def test_without_a_rule_the_second_pass_asks_exactly_as_much():
    report, text = loop()
    assert report.claims == ()
    assert report.recalled == ()
    assert report.asked_before == 7
    assert report.asked_after == report.asked_before
    assert len(report.autonomous.order) == report.total
    assert "nothing for now" in text


def test_a_rule_needs_its_confirmation_at_the_prompt():
    """A named case still waits for the second line, so an unanswered echo stores nothing."""
    report, text = loop([f"{RECRUITER_CASE}=ignore mail from {RECRUITER_SENDER}"])

    assert report.claims == ()
    assert f"reply for {RECRUITER_CASE}:" in text
    assert report.asked_after == report.asked_before


def test_the_second_pass_never_sends_anything():
    report, _ = loop([f"{RECRUITER_CASE}=ignore mail from {RECRUITER_SENDER}; yes"])
    assert report.autonomous.effects("email.send") == 0
    assert report.calibration.effects("email.send") == 0


def test_a_decision_the_script_does_not_answer_is_passed_on():
    """Nothing hangs on a prompt the script never feeds: it is told a line that does nothing."""
    queue: asyncio.Queue[str] = asyncio.Queue()
    case = view().cases[0]
    asyncio.run(
        ScriptedReplies([]).hook(queue)(
            1, route_decision(case, triage(case.event.message), None, "test", source="test")
        )
    )
    assert _drained(queue) == ["nothing for now"]


def test_a_named_entry_is_typed_at_the_case_it_names():
    queue: asyncio.Queue[str] = asyncio.Queue()
    replies = ScriptedReplies(["WAJO-0003=later", f"{RECRUITER_CASE}=ignore this sender; yes"])
    case = view().open(RECRUITER_CASE)
    asyncio.run(
        replies.hook(queue)(
            1, route_decision(case, triage(case.event.message), None, "test", source="test")
        )
    )
    assert _drained(queue) == ["ignore this sender", "yes"]
    assert replies.remaining == 1


def test_the_cli_reports_both_passes_and_what_was_kept(capsys):
    args = build_parser().parse_args(
        [
            "loop",
            "run",
            "--fixture",
            str(FIXTURE),
            "--seed",
            "7",
            "--say",
            f"{RECRUITER_CASE}=ignore mail from {RECRUITER_SENDER}; yes",
        ]
    )
    out = io.StringIO()
    assert loop_run(args, out) == 0
    text = out.getvalue()
    assert "[pass 1] calibration" in text and "[pass 2] autonomous" in text
    assert f"{RECRUITER_CASE}  PROCEED_SILENTLY         committed  <- from a rule" in text
    before, after = asked(text)
    assert after == before - 1
    assert "kept after this run:" in text
    capsys.readouterr()


def test_a_rule_kept_by_calibration_is_in_force_in_the_next_run(tmp_path, capsys):
    """The deliverable flow: calibrate once, then run autonomously in a later process."""
    store = tmp_path / "prefs.jsonl"
    calibrate = build_parser().parse_args(
        [
            "loop",
            "run",
            "--fixture",
            str(FIXTURE),
            "--seed",
            "7",
            "--store",
            str(store),
            "--say",
            f"{RECRUITER_CASE}=ignore mail from {RECRUITER_SENDER}; yes",
        ]
    )
    first = io.StringIO()
    assert loop_run(calibrate, first) == 0
    assert "1 in force" in first.getvalue()
    assert store.exists()

    autonomous = build_parser().parse_args(
        ["graph", "run", "--fixture", str(FIXTURE), "--seed", "7", "--store", str(store)]
    )
    second = io.StringIO()
    assert graph_run(autonomous, second) == 0
    text = second.getvalue()
    assert "1 loaded" in text
    assert f"{RECRUITER_CASE}  PROCEED_SILENTLY         committed" in text
    capsys.readouterr()


def test_the_simulator_answers_from_a_saved_rule_without_asking(tmp_path, capsys):
    """Calibrating on the same mail twice asks once: the rule answers the second time."""
    store = tmp_path / "prefs.jsonl"
    store.write_text(
        json.dumps(
            {
                "action_id": "email.archive",
                "claim_id": "clm-90598ef7a3ac",
                "confidence": 1.0,
                "params": {},
                "quote": f"ignore mail from {RECRUITER_SENDER}",
                "recorded_at": "2026-08-01T08:20:07+00:00",
                "route": "PROCEED_SILENTLY",
                "scope": {"domain": None, "intent": None, "sender": RECRUITER_SENDER},
                "scope_anchor": "explicit",
                "source_case_id": RECRUITER_CASE,
                "source_message_id": "msg-in-wajo-0008",
                "starts_after_case_id": RECRUITER_CASE,
                "superseded_by": None,
                "type": "boundary",
            }
        )
        + "\n",
        encoding="utf-8",
    )
    args = build_parser().parse_args(
        ["sim", "run", "--fixture", str(FIXTURE), "--seed", "7", "--store", str(store)]
    )
    out = io.StringIO()
    assert sim_run(args, out) == 0
    text = out.getvalue()
    assert "1 loaded" in text
    assert "interrupts=6" in text
    assert "archives=1" in text
    capsys.readouterr()


def _drained(queue: asyncio.Queue[str]) -> list[str]:
    lines: list[str] = []
    while not queue.empty():
        item = queue.get_nowait()
        if isinstance(item, str):
            lines.append(item)
    return lines
