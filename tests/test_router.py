from __future__ import annotations

import asyncio
import io
import json
from dataclasses import replace
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from agent.autonomy.bandit import Learner
from agent.autonomy.confidence import Bucket
from agent.autonomy.loss import LOSS_V1
from agent.autonomy.preferences import RememberedProvider
from agent.autonomy.router import (
    MIN_NOTIFY,
    MIN_SILENT,
    RELAX,
    TIGHTEN,
    Cutoffs,
    Router,
    RoutingRequest,
    ThresholdStore,
    mail_risk,
)
from agent.dataset import Lane, LaneView, Manifest
from agent.events import FeedbackEvent, FeedbackKind, is_learnable
from agent.gateway import ProposalGateway, ProposalRequest, RuleProvider
from agent.memory.claims import Claim, ClaimScope, ClaimType, ScopeAnchor
from agent.safety.floor import ALL_ROUTES, Route
from agent.sim.policy import ProposalPolicy, floor_verdict_for, named_route
from agent.sim.runner import close_input, run_simulation
from agent.state import routing_fields
from agent.trace import TraceSink

FIXTURE = Path(__file__).parent / "fixtures" / "stream_12.jsonl"
RECRUITER = "WAJO-0008"
RECRUITER_SENDER = "claire@nexustalent.synthetic.example"
WIRE_TRANSFER = "WAJO-0011"
NOW = datetime(2026, 8, 1, 9, 0, tzinfo=UTC)

CONTEXT = Bucket(
    sender=RECRUITER_SENDER, intent="recruiter follow-up", action="email.create_draft"
)

# A mail the user's rules have no opinion about: no missed notification, and the reading is
# sure of itself, so nothing but trust stands between it and acting silently.
PLAIN_RISK = mail_risk(confidence=1.0, addresses_others=False, ignorable=False)
# The mail a rule already covers: the user said it needs no telling, so silence withholds
# nothing and the question is only whether the route is on the ballot.
IGNORABLE_RISK = mail_risk(confidence=1.0, addresses_others=False, ignorable=True)


def view() -> LaneView:
    return Manifest.load(FIXTURE).view(Lane.CALIBRATION)


def case(case_id: str):
    return next(item for item in view().cases if item.case_id == case_id)


def request(
    *,
    allowed: tuple[Route, ...] = ALL_ROUTES,
    bucket: Bucket = CONTEXT,
    named: Route | None = None,
    risk: dict[str, float] | None = None,
) -> RoutingRequest:
    return RoutingRequest(
        case_id=RECRUITER,
        allowed=allowed,
        bucket=bucket,
        risk=risk if risk is not None else PLAIN_RISK,
        named=named,
    )


def feedback(
    kind: FeedbackKind,
    *,
    event_id: str = "WAJO-0008:input:1",
    route: Route | None = None,
    action: str | None = None,
) -> FeedbackEvent:
    """One recorded line, as the simulator writes it."""
    return FeedbackEvent(
        event_id=event_id,
        case_id=RECRUITER,
        kind=kind,
        explicit_for_learning=is_learnable(kind),
        text="ignore mail from claire@nexustalent.synthetic.example",
        chosen_route=route,
        chosen_action_id=action,
        recorded_at=NOW,
    )


def rule(*, route: Route | None, action: str | None) -> Claim:
    """A confirmed rule, the way the parser hands one over."""
    return Claim(
        claim_id="clm-90598ef7a3ac",
        type=ClaimType.PREFERENCE,
        quote="ignore mail from claire@nexustalent.synthetic.example",
        source_message_id="msg-in-wajo-0008",
        source_case_id=RECRUITER,
        recorded_at=NOW,
        scope=ClaimScope(sender=RECRUITER_SENDER),
        scope_anchor=ScopeAnchor.EXPLICIT,
        confidence=1.0,
        action_id=action,
        route=route,
    )


class ScriptedProvider:
    """A model in the shape of the provider protocol, answering from a script."""

    name = "scripted"

    def __init__(self, *answers: str) -> None:
        self.answers = list(answers)

    async def complete(self, request: ProposalRequest) -> str:
        return self.answers.pop(0) if self.answers else "{"


def test_a_payment_preference_still_escalates_a_fenced_bill():
    """The plan's check: the floor is not weighed against a preference, it is applied first."""
    verdict, _, _ = floor_verdict_for(case(WIRE_TRANSFER))
    assert verdict.allowed_routes == (Route.ESCALATE,)

    routing = Router().route(
        request(allowed=tuple(verdict.allowed_routes), named=Route.PROCEED_SILENTLY)
    )
    assert routing.route is Route.ESCALATE
    # Only one route was ever scored, so no cost and no preference could have reached past it.
    assert [loss.route for loss in routing.alternatives] == [Route.ESCALATE]


def test_a_confirmed_preference_enables_a_later_archive_before_trust_is_earned():
    """A rule the user confirmed is on the ballot on their word, not on the posterior's."""
    learner = Learner()
    learner.observe(
        feedback(FeedbackKind.ALWAYS_DO_THIS, route=Route.PROCEED_SILENTLY, action="email.archive"),
        Bucket(sender=RECRUITER_SENDER, intent="recruiter follow-up", action="email.archive"),
        claim=rule(route=Route.PROCEED_SILENTLY, action="email.archive"),
    )
    router = Router(learner)
    routing = router.route(
        request(
            bucket=Bucket(
                sender=RECRUITER_SENDER, intent="recruiter follow-up", action="email.archive"
            ),
            named=Route.PROCEED_SILENTLY,
            risk=IGNORABLE_RISK,
        )
    )
    assert routing.posterior.mean < 0.6, "one approval is not trust enough by itself"
    assert routing.route is Route.PROCEED_SILENTLY
    assert routing.named is Route.PROCEED_SILENTLY


def test_trust_admits_the_quieter_routes_only_when_it_is_earned():
    router = Router()
    cold = router.route(request(named=Route.ASK_FIRST_WITH_PREDRAFT))
    assert cold.eligible == (Route.ASK_FIRST_WITH_PREDRAFT, Route.ESCALATE)

    # Four approvals: Beta(5, 3), a mean of 0.625, over the notify cutoff of 0.6.
    for _ in range(4):
        router.store.record(CONTEXT, approved=True)
    warmed = router.route(request(named=Route.ASK_FIRST_WITH_PREDRAFT))
    assert Route.PROCEED_AND_NOTIFY in warmed.eligible
    assert Route.PROCEED_SILENTLY not in warmed.eligible, "0.625 is short of 0.8"
    assert warmed.route is Route.PROCEED_AND_NOTIFY

    # Eight more: Beta(13, 3), a mean of 0.8125, and silence is on the ballot.
    for _ in range(8):
        router.store.record(CONTEXT, approved=True)
    trusted = router.route(request(named=Route.ASK_FIRST_WITH_PREDRAFT))
    assert trusted.posterior.mean >= 0.8
    assert Route.PROCEED_SILENTLY in trusted.eligible
    # Eligible is not the same as chosen: on a mail whose awareness has value, telling the
    # user costs a tenth of a handoff and withholding it costs more than one.
    assert trusted.route is Route.PROCEED_AND_NOTIFY
    assert router.route(
        request(named=Route.ASK_FIRST_WITH_PREDRAFT, risk=IGNORABLE_RISK)
    ).route is Route.PROCEED_SILENTLY


def test_an_answer_nobody_vouched_for_buys_no_autonomy():
    """A model's own route is not a preference: it has to wait for the posterior."""
    routing = Router().route(request(named=None))
    assert routing.eligible == (Route.ASK_FIRST_WITH_PREDRAFT, Route.ESCALATE)
    assert routing.route is Route.ASK_FIRST_WITH_PREDRAFT


def test_a_refused_arm_leaves_the_ballot_and_is_named_on_the_receipt():
    learner = Learner()
    learner.observe(
        feedback(FeedbackKind.NEVER_DO_THIS, action="email.archive"),
        CONTEXT,
        claim=rule(route=None, action="email.archive"),
    )
    routing = Router(learner).route(
        request(bucket=Bucket(sender=RECRUITER_SENDER, action="email.archive"), named=Route.PROCEED_SILENTLY)
    )
    assert routing.refused_by == "clm-90598ef7a3ac"
    assert Route.PROCEED_SILENTLY not in routing.eligible
    assert Route.PROCEED_AND_NOTIFY not in routing.eligible
    assert routing.route is Route.ASK_FIRST_WITH_PREDRAFT
    assert "refused" in routing.basis


def test_the_router_scores_nothing_the_floor_masked():
    routing = Router().route(
        request(allowed=(Route.ASK_FIRST_WITH_PREDRAFT, Route.ESCALATE), named=Route.PROCEED_SILENTLY)
    )
    assert {loss.route for loss in routing.alternatives} <= set(routing.allowed)
    assert routing.allowed == (Route.ASK_FIRST_WITH_PREDRAFT, Route.ESCALATE)


def test_a_tie_goes_to_the_more_cautious_route():
    # A handoff that costs nothing to defer is exactly what asking costs, which is the one
    # way the arithmetic can tie; the tie then breaks toward the route the user can see.
    free_delay = replace(LOSS_V1, version="loss-v1-tie", delay=0.0)
    routing = Router(costs=free_delay).route(request(named=Route.ASK_FIRST_WITH_PREDRAFT))
    assert {loss.value for loss in routing.alternatives} == {0.5}
    assert routing.route is Route.ESCALATE


def test_the_receipt_carries_the_posterior_the_claim_and_the_workings():
    routing = Router().route(request(named=Route.PROCEED_AND_NOTIFY))
    fields = routing_fields(routing)

    assert fields["route"] == routing.route.value
    assert fields["named"] == Route.PROCEED_AND_NOTIFY.value
    assert fields["posterior"] == {"mean": 0.25, "alpha": 1.0, "beta": 3.0, "level": ""}
    assert [item["route"] for item in fields["alternatives"]] == [
        loss.route.value for loss in routing.alternatives
    ]
    assert fields["alternatives"][0]["terms"] == [
        "wrong_action 0.00x0.6",
        "wrong_audience 0.00x2",
        "notified 1.00x0.1",
    ]


def test_the_thresholds_move_with_feedback_and_stop_at_the_calibration_floor():
    thresholds = ThresholdStore()
    assert thresholds.for_bucket(CONTEXT) == Cutoffs()

    relaxed = thresholds.adapt(CONTEXT, approved=True)
    assert relaxed.silent == 0.8 * RELAX
    assert thresholds.for_bucket(CONTEXT).notify == 0.6 * RELAX

    tightened = thresholds.adapt(CONTEXT, approved=False)
    assert tightened.silent == 0.8 * RELAX + TIGHTEN
    assert tightened.notify == 0.6 * RELAX + TIGHTEN

    for _ in range(200):
        thresholds.adapt(CONTEXT, approved=True)
    assert thresholds.for_bucket(CONTEXT).silent == MIN_SILENT
    assert thresholds.for_bucket(CONTEXT).notify == MIN_NOTIFY
    for _ in range(200):
        thresholds.adapt(CONTEXT, approved=False)
    # A cap of 1.0 is the most a burst of reverts can demand, and it never exceeds certainty.
    assert thresholds.for_bucket(CONTEXT).silent <= 1.0

    # Cutoffs are read through the same chain the posteriors use, so a bucket nobody has
    # adapted itself inherits whatever a coarser context earned.
    archive = Bucket(action="email.archive")
    thresholds.adapt(archive, approved=True)
    assert thresholds.for_bucket(archive).silent == 0.8 * RELAX
    assert thresholds.for_bucket(Bucket(sender=RECRUITER_SENDER, action="email.archive")).silent == (
        0.8 * RELAX
    )
    # A sender on its own cannot read a context-level cutoff: that level is keyed on the
    # whole context, so it falls through to the defaults rather than a stranger's history.
    assert thresholds.for_bucket(Bucket(sender=RECRUITER_SENDER)).silent == Cutoffs().silent


def test_one_feedback_event_moves_the_posterior_and_the_cutoffs_once():
    thresholds = ThresholdStore()
    router = Router(Learner(), thresholds=thresholds)
    event = feedback(FeedbackKind.APPROVE)

    assert router.observe(event, CONTEXT) is True
    once = thresholds.for_bucket(CONTEXT)
    # Silence and the user's own reply are not decisions, so they move nothing at all.
    assert router.observe(feedback(FeedbackKind.REPLY, event_id="c:2"), CONTEXT) is False
    assert thresholds.for_bucket(CONTEXT) == once


def test_the_router_is_deterministic():
    first = Router().route(request(named=Route.PROCEED_AND_NOTIFY))
    second = Router().route(request(named=Route.PROCEED_AND_NOTIFY))
    assert first.describe() == second.describe()
    assert [(loss.route, loss.value) for loss in first.alternatives] == [
        (loss.route, loss.value) for loss in second.alternatives
    ]


def test_the_persona_names_the_route_a_model_may_not_exceed():
    """An untrusted proposal is the thing the router tests, so it cannot buy silence."""
    silent_archive = json.dumps(
        {
            "route": "PROCEED_SILENTLY",
            "action_id": "email.archive",
            "params": {},
            "rationale": "reads like a recruiter mail",
            "confidence": 0.95,
        }
    )
    recruiter = case(RECRUITER)
    provider = ScriptedProvider(silent_archive)
    assert named_route(provider, recruiter.event.message, _hints(recruiter)) is (
        Route.ASK_FIRST_WITH_PREDRAFT
    )

    policy = ProposalPolicy(ProposalGateway(provider), router=Router())
    decision = asyncio.run(policy.decide(recruiter))
    assert decision.routing is not None
    assert decision.routing.named is Route.ASK_FIRST_WITH_PREDRAFT
    assert decision.route is Route.ASK_FIRST_WITH_PREDRAFT


def test_a_run_routes_every_arrival_and_keeps_the_receipts(tmp_path: Path):
    queue: asyncio.Queue[Any] = asyncio.Queue()
    for _ in range(len(view().cases)):
        queue.put_nowait("nothing for now")
    asyncio.run(close_input(queue))

    learner = Learner()
    router = Router(learner)
    trace_path = tmp_path / "router.jsonl"
    outcome = asyncio.run(
        run_simulation(
            view(),
            seed=7,
            out=io.StringIO(),
            input_queue=queue,
            learner=learner,
            router=router,
            trace=TraceSink(trace_path),
        )
    )

    assert outcome.processed == len(view().cases)
    assert router.routings == outcome.processed
    decisions = [
        json.loads(line)
        for line in trace_path.read_text(encoding="utf-8").splitlines()
        if '"decision"' in line
    ]
    assert len(decisions) == outcome.processed
    for line in decisions:
        routing = line["routing"]
        assert routing["route"] == line["route"]
        assert routing["alternatives"], "every alternative is scored and kept"
        assert set(routing["eligible"]) <= set(routing["allowed"])


def _hints(item):
    from agent.triage import triage

    return triage(item.event.message)


def test_the_remembered_provider_names_the_users_own_route():
    """The memory layer answers from a claim, and that is a preference like the rules are."""
    from agent.memory.claims import ClaimStore
    from agent.memory.consent import session_grant

    store = ClaimStore(grant=session_grant(purpose="router test"))
    store.store(rule(route=Route.PROCEED_SILENTLY, action="email.archive"))
    provider = RememberedProvider(store, RuleProvider())
    recruiter = case(RECRUITER)
    assert named_route(provider, recruiter.event.message, _hints(recruiter)) is (
        Route.PROCEED_SILENTLY
    )
