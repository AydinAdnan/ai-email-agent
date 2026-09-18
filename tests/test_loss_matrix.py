from __future__ import annotations

from dataclasses import fields, replace
from itertools import chain

import pytest

from agent.autonomy.loss import LOSS_V1, ROUTE_OUTCOMES, Costs, Loss, pick, score
from agent.safety.floor import ALL_ROUTES, Route

# The plan's section 4.4 walkthrough as a mail's risk profile: a verified AWS billing
# sender, an invoice, and a persona rule that already fixes the action - label
# Finance/Cloud, never pay, never reply. So the action is not in doubt and only the
# awareness is, which is why nothing here carries a wrong-action or wrong-audience risk
# and the three numbers that decide the route are the costs of telling.
AWS_BILL = {"missed_notification": 1.0, "interruption": 1.0, "delay": 1.0, "notified": 1.0}

# "Can you handle the refund?" with no amount. A missing required field makes a wrong
# commitment both likely and expensive, so every route that acts is dear and the one
# bounded question is cheap.
AMBIGUOUS_REFUND = {
    "wrong_action": 1.0,
    "wrong_audience": 1.0,
    "missed_notification": 1.0,
    "interruption": 1.0,
    "delay": 1.0,
    "notified": 1.0,
}


def test_the_aws_bill_reproduces_the_plans_three_losses_and_picks_notify():
    values = {loss.route: loss.value for loss in score(ALL_ROUTES, AWS_BILL)}
    assert values[Route.PROCEED_SILENTLY] == pytest.approx(1.4)
    assert values[Route.PROCEED_AND_NOTIFY] == pytest.approx(0.1)
    assert values[Route.ASK_FIRST_WITH_PREDRAFT] == pytest.approx(0.5)
    assert pick(score(ALL_ROUTES, AWS_BILL)).route is Route.PROCEED_AND_NOTIFY


def test_silence_is_the_costliest_route_there_because_it_reports_nothing():
    values = {loss.route: loss.value for loss in score(ALL_ROUTES, AWS_BILL)}
    assert (
        values[Route.PROCEED_AND_NOTIFY]
        < values[Route.ASK_FIRST_WITH_PREDRAFT]
        < values[Route.ESCALATE]
        < values[Route.PROCEED_SILENTLY]
    )


def test_an_ambiguous_refund_is_asked_about_rather_than_acted_on():
    assert pick(score(ALL_ROUTES, AMBIGUOUS_REFUND)).route is Route.ASK_FIRST_WITH_PREDRAFT


def test_the_table_holds_the_documented_outcome_costs_and_a_version():
    assert {field.name for field in fields(Costs)} == {
        "version",
        "wrong_action",
        "wrong_audience",
        "missed_notification",
        "interruption",
        "delay",
        "notified",
    }
    assert LOSS_V1.version == "loss-v1"


def test_every_outcome_a_route_can_produce_is_a_cost_on_the_table():
    # The lookup is by name, so a route naming an outcome the table does not price would
    # fail while a mail was being routed rather than here.
    priced = {field.name for field in fields(Costs)}
    assert set(chain.from_iterable(ROUTE_OUTCOMES.values())) <= priced


def test_the_matrix_carries_no_safety_term():
    # Safety is masked before this table is consulted, so no cost here can promote a
    # fenced action: an outcome named after money, credentials or sends would be exactly
    # the wrong place to put that decision.
    vocabulary = " ".join(
        sorted(
            {field.name for field in fields(Costs)}
            | set(chain.from_iterable(ROUTE_OUTCOMES.values()))
        )
    )
    for word in ("money", "payment", "credential", "password", "secret", "token", "send", "delete"):
        assert word not in vocabulary


def test_only_the_routes_the_floor_left_are_scored():
    # A fenced action arrives as ESCALATE alone, so the other three are never priced.
    assert [loss.route for loss in score((Route.ESCALATE,), AWS_BILL)] == [Route.ESCALATE]


def test_a_tie_goes_to_the_more_cautious_route_whichever_order_it_arrives_in():
    tied = [
        Loss(route=route, value=0.5, terms=())
        for route in (Route.PROCEED_SILENTLY, Route.PROCEED_AND_NOTIFY, Route.ASK_FIRST_WITH_PREDRAFT)
    ]
    tied.append(Loss(route=Route.ESCALATE, value=0.5, terms=()))
    assert pick(tied).route is Route.ESCALATE
    assert pick(list(reversed(tied))).route is Route.ESCALATE


def test_an_empty_choice_is_an_error_rather_than_a_default():
    with pytest.raises(ValueError):
        pick(())


def test_the_receipt_keeps_the_workings_behind_the_chosen_route():
    loss = pick(score(ALL_ROUTES, AWS_BILL))
    assert loss.terms == (
        ("wrong_action", 0.0, 0.6),
        ("wrong_audience", 0.0, 2.0),
        ("notified", 1.0, 0.1),
    )
    assert "notified 1.00x0.1" in loss.describe()


def test_a_cost_change_is_a_new_version_and_it_moves_the_route():
    # The numbers are load-bearing, which is why the table is versioned and why safety
    # lives elsewhere: no edit here can reach past the floor, and no vote can change it.
    cheaper_awareness = replace(LOSS_V1, version="loss-v2", missed_notification=0.05)
    assert pick(score(ALL_ROUTES, AWS_BILL, cheaper_awareness)).route is Route.PROCEED_SILENTLY
    assert pick(score(ALL_ROUTES, AWS_BILL)).route is Route.PROCEED_AND_NOTIFY
