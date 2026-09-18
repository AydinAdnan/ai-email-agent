"""The scorer's honesty rules: every rate carries its denominator, and lanes stay apart.

Two claims here are the ones an inflated number would break. Dispositions are mutually
exclusive and sum to the cases processed, so the report cannot quietly drop a case it
handled a third way. And held-out accuracy refuses to exist unless the lane behind it was
sealed: a lane that may teach, or a run that wrote while it was being measured, is not held
out whatever the file is called.
"""
import json
from datetime import UTC, datetime
from types import SimpleNamespace

import pytest

from agent.dataset import DEFAULT_DATASET_PATH, Lane, LaneView, Manifest, SplitViolation
from agent.events import FeedbackEvent, FeedbackKind
from agent.gateway import ProposalGateway, RuleProvider
from agent.graph import GraphOutcome, GraphRuntime
from agent.replay import SeededClock
from agent.safety.floor import Route, SafetyVerdict, VetoLevel
from agent.sim.policy import Decision
from agent.sim.runner import SimOutcome
from agent.tools.email_tools import SimulatedMailbox, build_registry
from agent.tools.registry import Receipt
from evals.harness import (
    BLOCK,
    LaneRecord,
    ScoringError,
    ask_curve,
    calibration_report,
    dispositions,
    held_out_report,
    record_from_chat,
    record_from_graph,
    two_lane_report,
)

NOW = datetime(2026, 9, 1, 12, 0, tzinfo=UTC)
AUTONOMOUS = {Route.PROCEED_SILENTLY.value, Route.PROCEED_AND_NOTIFY.value}


def _rows(split: str, limit: int | None = None) -> list[dict]:
    """Real rows from one split of the committed case set."""
    manifest = Manifest.load(DEFAULT_DATASET_PATH)
    rows = [case.row for case in manifest.cases if case.split == split]
    return rows if limit is None else rows[:limit]


def _view(split: str, lane: Lane, limit: int | None = None) -> LaneView:
    """A lane over real rows, so the routes the tests compare against are the dataset's."""
    manifest = Manifest.load(DEFAULT_DATASET_PATH)
    return Manifest.from_rows(
        _rows(split, limit), source=f"{split} (test)", dataset_digest=manifest.dataset_digest
    ).view(lane)


def _record(view: LaneView, routes: dict[str, str], **overrides) -> LaneRecord:
    """A lane's record, with only the fields the report needs for one claim."""
    settings: dict = {
        "lane": view.lane,
        "processed": len(routes),
        "order": tuple(routes),
        "routes": routes,
    }
    settings.update(overrides)
    return LaneRecord(**settings)


def _gold(view: LaneView) -> dict[str, str]:
    """Every case's gold route, exactly as the dataset states it."""
    return {case.case_id: case.row["gold"]["autonomy_outcome"] for case in view.cases}


def _decision(case_id: str, route: Route, *allowed: Route) -> Decision:
    """A decided case carrying the floor's ballot, which is what violations are read from."""
    return Decision(
        case_id=case_id,
        route=route,
        action_id="email.apply_label",
        tool_name="label",
        params={"label": "Test"},
        sender="someone@synthetic.example",
        reason="test",
        verdict=SafetyVerdict(
            veto=False,
            veto_level=VetoLevel.NONE,
            allowed_routes=allowed or (Route.ESCALATE,),
            reason="test ballot",
        ),
        source="test",
    )


def _receipt(case_id: str, route: Route, action_id: str = "email.apply_label") -> Receipt:
    return Receipt(
        receipt_id=f"rcpt-{case_id}",
        case_id=case_id,
        message_id=f"msg-{case_id}",
        route=route,
        action_id=action_id,
        prepared_digest="digest",
        effects=(),
        committed_at=NOW,
    )


def _feedback(case_id: str, kind: str, *, route: Route = Route.PROCEED_AND_NOTIFY) -> FeedbackEvent:
    return FeedbackEvent(
        event_id=f"{case_id}:{kind}",
        case_id=case_id,
        kind=FeedbackKind(kind),
        explicit_for_learning=kind not in {"none", "reply", "ignore_observed"},
        text="",
        edited_draft=None,
        chosen_action_id="email.apply_label",
        chosen_route=route,
    )


# ============================================================================
# Dispositions: mutually exclusive, and summing to what was processed
# ============================================================================

def test_dispositions_cover_every_route_and_sum_to_the_case_count():
    """The plan's rule: three dispositions, one per case, adding up to all of them."""
    counted = dispositions(
        [
            Route.PROCEED_SILENTLY.value,
            Route.PROCEED_AND_NOTIFY.value,
            Route.ASK_FIRST_WITH_PREDRAFT.value,
            Route.ESCALATE.value,
        ]
    )

    assert (counted.automated, counted.user_review, counted.escalate) == (2, 1, 1)
    assert counted.total == 4
    assert "(of 4 case(s))" in counted.describe()


def test_a_route_the_report_does_not_know_is_refused_rather_than_counted():
    """A fifth route is a bug, and an uncounted case is the same bug wearing a number."""
    with pytest.raises(ScoringError):
        dispositions(["PROCEED", "PROCEED_SILENTLY"])


def test_a_record_that_decided_fewer_cases_than_it_processed_is_refused():
    """The denominator is the run's own count, so a partial record cannot be scored."""
    view = _view("learning_stream", Lane.CALIBRATION, limit=2)
    record = _record(
        view,
        {view.cases[0].case_id: Route.PROCEED_SILENTLY.value},
        processed=2,
    )

    with pytest.raises(ScoringError) as caught:
        calibration_report(record)

    assert "denominator" in str(caught.value)


# ============================================================================
# The sealed lane: accuracy here, and nowhere else
# ============================================================================

def test_held_out_accuracy_is_measured_over_the_whole_sealed_lane():
    """Route accuracy's denominator is every graded case, not the ones that matched."""
    view = _view("golden_ordinary", Lane.HELD_OUT, limit=4)
    gold = _gold(view)
    routes = dict(gold)
    missed = next(iter(gold))
    routes[missed] = Route.ESCALATE.value

    report = held_out_report(view, _record(view, routes))

    assert report.total == 4
    assert (report.route_matched, report.route_graded) == (3, 4)
    assert report.disposition.total == report.total
    assert "3/4 (75%)" in report.render()


def test_action_accuracy_is_graded_only_where_gold_carries_an_action():
    """A case whose answer is a handoff has no action to match, so it is not graded as one."""
    view = _view("golden_ordinary", Lane.HELD_OUT, limit=6)
    gold = _gold(view)
    routes = dict(gold)
    receipts = {
        case_id: _receipt(case_id, Route(value))
        for case_id, value in routes.items()
        if value in AUTONOMOUS
    }

    report = held_out_report(view, _record(view, routes, receipts=receipts))

    assert report.action_graded == sum(1 for value in gold.values() if value in AUTONOMOUS)
    assert report.action_matched == report.action_graded


def test_held_out_accuracy_rejects_a_lane_that_could_learn():
    """A lane that may write learner state is not held out, whatever it is called."""
    view = _view("learning_stream", Lane.CALIBRATION, limit=3)
    record = _record(view, {case.case_id: Route.PROCEED_SILENTLY.value for case in view.cases})

    with pytest.raises(SplitViolation) as caught:
        held_out_report(view, record)

    assert "may write learner state" in str(caught.value)


def test_held_out_accuracy_rejects_a_run_that_wrote_learner_state():
    """A sealed pass that taught the learner is grading itself against its own lesson."""
    view = _view("golden_ordinary", Lane.HELD_OUT, limit=3)
    record = _record(view, {case.case_id: Route.PROCEED_SILENTLY.value for case in view.cases})

    with pytest.raises(SplitViolation) as caught:
        held_out_report(view, record, learning_writes=1)

    assert "wrote learner state 1 time(s)" in str(caught.value)


def test_floor_violations_are_counted_against_the_ballot_the_run_was_given():
    """A route outside the floor's surviving set is a violation, not a preference."""
    view = _view("golden_ordinary", Lane.HELD_OUT, limit=2)
    first, second = (case.case_id for case in view.cases)
    record = _record(
        view,
        {first: Route.PROCEED_SILENTLY.value, second: Route.ESCALATE.value},
        decisions={
            # Silence where the floor left only a handoff, and a legal escalation beside it.
            first: _decision(first, Route.PROCEED_SILENTLY, Route.ESCALATE),
            second: _decision(
                second, Route.ESCALATE, Route.ASK_FIRST_WITH_PREDRAFT, Route.ESCALATE
            ),
        },
    )

    report = held_out_report(view, record)

    assert (report.floor_violations, report.floors_graded) == (1, 2)
    assert "1/2 (50%)" in report.render()


def test_a_commit_the_route_did_not_license_is_unauthorized_without_an_approval():
    """An ASK that committed with nobody behind it is the bypass this gate exists for."""
    view = _view("golden_ordinary", Lane.HELD_OUT, limit=2)
    first, second = (case.case_id for case in view.cases)
    routes = {first: Route.ASK_FIRST_WITH_PREDRAFT.value, second: Route.PROCEED_SILENTLY.value}
    receipts = {
        first: _receipt(first, Route.ASK_FIRST_WITH_PREDRAFT),
        second: _receipt(second, Route.PROCEED_SILENTLY),
    }

    assert held_out_report(view, _record(view, routes, receipts=receipts)).unauthorised_commits == 1

    approved = _record(view, routes, receipts=receipts, approvals={first: "user"})
    assert held_out_report(view, approved).unauthorised_commits == 0


def test_adversarial_escalation_counts_only_the_adversarial_subset():
    """The gate is 100% on the adversarial split, so its denominator is that split."""
    view = _view("golden_adversarial", Lane.HELD_OUT, limit=3)
    ids = [case.case_id for case in view.cases]
    escalated = {case_id: Route.ESCALATE.value for case_id in ids}
    asked = {**escalated, ids[0]: Route.ASK_FIRST_WITH_PREDRAFT.value}

    assert held_out_report(view, _record(view, escalated)).adversarial_escalated == 3

    report = held_out_report(view, _record(view, asked))
    assert (report.adversarial_escalated, report.adversarial_total) == (2, 3)
    assert "2/3 (67%)" in report.render()


# ============================================================================
# The calibration lane: what the user typed, and the curve
# ============================================================================

def test_the_curve_blocks_the_lane_in_delivery_order_and_the_last_block_may_be_short():
    """Blocks are the stream's own order, and four cases at block 12 is one block of four."""
    order = tuple(f"case-{index:02d}" for index in range(1, 26))

    curve = ask_curve(order, {"case-01", "case-13"}, block=BLOCK)

    assert [block.cases for block in curve] == [12, 12, 1]
    assert [block.asked for block in curve] == [1, 1, 0]
    assert curve[0].share == "1/12 (8%)"
    assert curve[-1].last == 25


def test_the_chat_adapter_reads_routes_and_asks_per_case_in_delivery_order():
    """The simulator records per case, so the curve comes from the run rather than a guess."""
    view = _view("learning_stream", Lane.CALIBRATION, limit=3)
    ids = [case.case_id for case in view.cases]
    outcome = SimOutcome(
        processed=3,
        replies=2,
        corrections=1,
        routes={
            ids[0]: Route.ESCALATE.value,
            ids[1]: Route.PROCEED_SILENTLY.value,
            ids[2]: Route.PROCEED_SILENTLY.value,
        },
        asked={ids[0]: "AUTHORIZATION_REFUSED"},
        receipts=[_receipt(ids[1], Route.PROCEED_SILENTLY)],
    )

    record = record_from_chat(outcome)
    report = calibration_report(record)

    assert record.order == tuple(ids)
    assert report.typings == 3
    assert (report.asked, report.autonomous) == (1, 1)
    assert report.disposition.describe() == "automated 2  user review 0  escalate 1  (of 3 case(s))"


def test_reverts_are_rated_against_the_agent_s_own_commits():
    """A revert rate needs both halves: what the user undid, and what the agent did."""
    view = _view("learning_stream", Lane.CALIBRATION, limit=2)
    first, second = (case.case_id for case in view.cases)
    outcome = SimOutcome(
        processed=2,
        routes={first: Route.PROCEED_AND_NOTIFY.value, second: Route.PROCEED_SILENTLY.value},
        receipts=[
            _receipt(first, Route.PROCEED_AND_NOTIFY),
            _receipt(second, Route.PROCEED_SILENTLY),
        ],
        feedback=[
            _feedback(first, "revert"),
            _feedback(second, "approve"),
            _feedback(second, "none"),
        ],
    )

    report = calibration_report(record_from_chat(outcome))

    assert (report.reverts, report.autonomous) == (1, 2)
    assert "1/2 (50%) of the agent's own commits" in report.render()


def test_the_graph_adapter_reads_the_ballot_and_who_authorised_each_commit():
    """A graph run keeps the verdict and the authorization, which both gates read."""
    view = _view("golden_ordinary", Lane.HELD_OUT, limit=1)
    case = view.cases[0]
    runtime = GraphRuntime(
        cases={case.case_id: case},
        gateway=ProposalGateway(RuleProvider()),
        registry=build_registry(SimulatedMailbox()),
        clock=SeededClock(seed=7),
    )
    runtime.decisions[case.case_id] = _decision(
        case.case_id, Route.PROCEED_SILENTLY, Route.PROCEED_SILENTLY
    )  # one legal route on the ballot, and it took it
    runtime.authorizations[case.case_id] = SimpleNamespace(approved_by="auto")
    outcome = GraphOutcome(
        processed=1,
        order=[case.case_id],
        routes={case.case_id: Route.PROCEED_SILENTLY.value},
        receipts=[_receipt(case.case_id, Route.PROCEED_SILENTLY)],
    )

    record = record_from_graph(outcome, runtime)
    report = held_out_report(view, record)

    assert (report.floor_violations, report.floors_graded) == (0, 1)
    assert report.unauthorised_commits == 0
    assert report.route_matched == 1


# ============================================================================
# The report itself
# ============================================================================

def test_the_report_keeps_the_lanes_apart_and_writes_both_sections(tmp_path):
    """One disposition count over everything; accuracy only ever from the sealed lane."""
    calibration_view = _view("learning_stream", Lane.CALIBRATION, limit=2)
    sealed_view = _view("golden_ordinary", Lane.HELD_OUT, limit=3)
    sealed_gold = _gold(sealed_view)
    calibration = calibration_report(
        record_from_chat(
            SimOutcome(
                processed=2,
                replies=1,
                routes={
                    case.case_id: Route.PROCEED_AND_NOTIFY.value
                    for case in calibration_view.cases
                },
                receipts=[
                    _receipt(case.case_id, Route.PROCEED_AND_NOTIFY)
                    for case in calibration_view.cases
                ],
                asked={calibration_view.cases[0].case_id: "APPROVAL_REQUIRED"},
            )
        )
    )
    held_out = held_out_report(
        sealed_view,
        _record(
            sealed_view,
            dict(sealed_gold),
            receipts={
                case_id: _receipt(case_id, Route(value))
                for case_id, value in sealed_gold.items()
                if value in AUTONOMOUS
            },
        ),
    )

    report = two_lane_report(calibration, held_out)

    assert report.overall.total == calibration.total + held_out.total
    assert report.overall.describe().endswith("(of 5 case(s))")
    text = report.render()
    assert "calibration lane: 2 case(s)" in text
    assert "held-out lane: 3 case(s)" in text
    assert "never blended" in text

    written = report.write(tmp_path / "report.json")
    payload = json.loads(written.read_text(encoding="utf-8"))
    assert payload["overall"]["cases"] == 5
    assert "route_accuracy" in payload["held_out"]
    assert "route_accuracy" not in payload["calibration"]
    assert payload["held_out"]["learning_writes"] == 0


def test_a_report_cannot_be_written_where_it_cannot_be_read(tmp_path):
    """The failure names the path, because a report nobody can write is nobody's data."""
    calibration_view = _view("learning_stream", Lane.CALIBRATION, limit=1)
    sealed_view = _view("golden_adversarial", Lane.HELD_OUT, limit=1)
    report = two_lane_report(
        calibration_report(
            record_from_chat(
                SimOutcome(
                    processed=1,
                    routes={calibration_view.cases[0].case_id: Route.PROCEED_SILENTLY.value},
                )
            )
        ),
        held_out_report(
            sealed_view,
            _record(
                sealed_view,
                {sealed_view.cases[0].case_id: Route.ESCALATE.value},
            ),
        ),
    )

    with pytest.raises(ScoringError) as caught:
        report.write(tmp_path / "no-such-dir" / "report.json")

    assert "no-such-dir" in str(caught.value)
