"""The floor's second hard requirement, as an executable proof.

No posterior, no cost value and no amount of feedback may raise a class ceiling, and
silence may never teach. Each test names the claim it pins and carries the control that
stops it from passing for the wrong reason: the ledger that decides the fenced case is
also shown deciding an unfenced one, so a test that would pass on a router wired to
always escalate fails here instead.
"""

from __future__ import annotations

import asyncio
import io
from dataclasses import replace
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from agent.autonomy.bandit import AUTONOMOUS_ROUTES, Learner
from agent.autonomy.confidence import Bucket
from agent.autonomy.loss import LOSS_V1
from agent.autonomy.router import MIN_SILENT, Cutoffs, Router, Routing, RoutingRequest, mail_risk
from agent.dataset import Case, Lane, LaneView, Manifest
from agent.events import FeedbackEvent, FeedbackKind, is_learnable
from agent.safety.floor import (
    ALL_ROUTES,
    ActionClass,
    ActionPayload,
    Route,
    floor_check,
)
from agent.sim.policy import email_context_for, floor_verdict_for
from agent.sim.runner import close_input, run_simulation
from agent.triage import triage

FIXTURE = Path(__file__).parent / "fixtures" / "stream_12.jsonl"

# A bill the floor fences, a secret it fences, and a label it does not. The two fenced
# classes are where the ceiling has to hold however loud the user is; the label is where
# the same feedback must still be able to earn trust, or the guard is not specific.
MONEY = "WAJO-0011"
SECRETS = "WAJO-0034"
REVERSIBLE = "WAJO-0001"

# "Thousands of synthetic feedback events", per the plan's check.
TRIALS = 1500
NOW = datetime(2026, 8, 1, 9, 0, tzinfo=UTC)

# A mail whose reading is sure of itself and which nobody's rules class as ignorable, so
# nothing but trust stands between it and acting silently.
PLAIN_RISK = mail_risk(confidence=1.0, addresses_others=False, ignorable=False)
# The same mail with the user's own rules having classed it as needing no telling.
IGNORABLE_RISK = mail_risk(confidence=1.0, addresses_others=False, ignorable=True)


def view() -> LaneView:
    return Manifest.load(FIXTURE).view(Lane.CALIBRATION)


def case(case_id: str) -> Case:
    return next(item for item in view().cases if item.case_id == case_id)


def bucket_for(case_id: str) -> Bucket:
    """The context the pipeline counts this case's decision in."""
    item = case(case_id)
    _, action_id, _ = floor_verdict_for(item)
    return Bucket(
        sender=item.event.message.sender.email,
        intent=triage(item.event.message).intent,
        action=action_id,
    )


def feedback(
    kind: FeedbackKind,
    case_id: str,
    *,
    index: int,
    route: Route | None = None,
    action: str | None = None,
) -> FeedbackEvent:
    """One recorded line, in the shape the simulator writes."""
    return FeedbackEvent(
        event_id=f"{case_id}:input:{index}",
        case_id=case_id,
        kind=kind,
        explicit_for_learning=is_learnable(kind),
        text="do it silently from now on",
        chosen_route=route,
        chosen_action_id=action,
        recorded_at=NOW,
    )


def approve(learner: Learner, router: Router, case_id: str, bucket: Bucket, count: int) -> None:
    """Count `count` explicit approvals into both the posteriors and the cutoffs."""
    for index in range(count):
        event = feedback(
            FeedbackKind.APPROVE,
            case_id,
            index=index,
            route=Route.PROCEED_SILENTLY,
            action="email.archive",
        )
        learner.observe(event, bucket)
        router.observe(event, bucket)


def revert(learner: Learner, router: Router, case_id: str, bucket: Bucket, count: int) -> None:
    """Count `count` approved-then-undone decisions, each worth three rejections."""
    for index in range(count):
        event = feedback(
            FeedbackKind.REVERT, case_id, index=10_000 + index, route=Route.PROCEED_AND_NOTIFY
        )
        learner.observe(event, bucket)
        router.observe(event, bucket)


def ask_again(
    router: Router,
    case_id: str,
    allowed: tuple[Route, ...],
    bucket: Bucket,
    risk: dict[str, float],
) -> Routing:
    """Route one arrival the way the pipeline does, with the user's own rule naming silence."""
    return router.route(
        RoutingRequest(
            case_id=case_id,
            allowed=allowed,
            bucket=bucket,
            risk=risk,
            named=Route.PROCEED_SILENTLY,
        )
    )


def one_case_view(case_id: str) -> LaneView:
    """A lane holding one arrival, so a run is about that mail and nothing else."""
    full = Manifest.load(FIXTURE)
    row = case(case_id).row
    return Manifest.from_rows(
        [row], source=full.source, dataset_digest=full.dataset_digest
    ).view(Lane.CALIBRATION)


def test_a_fenced_case_never_reaches_silence_or_notify_however_loud_the_feedback():
    """Approvals and reverts by the thousand move the trust, and never the ballot."""
    item = case(MONEY)
    verdict, _, _ = floor_verdict_for(item)
    assert verdict.allowed_routes == (Route.ESCALATE,), "the bill must be fenced to begin with"

    bucket = bucket_for(MONEY)
    learner = Learner()
    router = Router(learner)
    approaches: set[Route] = set()

    # Every routing below is the user's own rule asking for silence on a fenced mail.
    approve(learner, router, MONEY, bucket, TRIALS)
    # The user's trust is as earned as it can get, and their cutoffs have bottomed out.
    assert router.store.posterior(bucket).mean > 0.8, "the volume has to be loud enough to matter"
    assert router.thresholds.for_bucket(bucket).silent == MIN_SILENT, "cutoffs bottomed out"
    for _ in range(200):
        routing = ask_again(router, MONEY, verdict.allowed_routes, bucket, PLAIN_RISK)
        assert routing.route is Route.ESCALATE
        assert not set(routing.allowed) & AUTONOMOUS_ROUTES
        assert not set(routing.eligible) & AUTONOMOUS_ROUTES
        assert [loss.route for loss in routing.alternatives] == [Route.ESCALATE]
        approaches |= {loss.route for loss in routing.alternatives}

    # And the other way: the same volume of reverts, each worth three rejections, cannot
    # take a route off a ceiling that was never below the ceiling to begin with.
    revert(learner, router, MONEY, bucket, TRIALS)
    posterior = router.store.posterior(bucket)
    assert posterior.beta > posterior.alpha, "the reverts have to outweigh the approvals"
    for _ in range(200):
        routing = ask_again(router, MONEY, verdict.allowed_routes, bucket, PLAIN_RISK)
        assert routing.route is Route.ESCALATE
        assert not set(routing.eligible) & AUTONOMOUS_ROUTES
        approaches |= {loss.route for loss in routing.alternatives}

    assert approaches == {Route.ESCALATE}, "no autonomous route was ever even scored"


def test_the_same_feedback_still_earns_trust_where_the_floor_allows_it():
    """The control: a class the floor does not fence is learned from as normal."""
    bucket = bucket_for(REVERSIBLE)
    learner = Learner()
    router = Router(learner)
    assert learner.observe(
        feedback(
            FeedbackKind.APPROVE,
            REVERSIBLE,
            index=0,
            route=Route.PROCEED_SILENTLY,
            action="email.apply_label",
        ),
        bucket,
    )

    cold = router.route(
        RoutingRequest(
            case_id=REVERSIBLE,
            allowed=ALL_ROUTES,
            bucket=bucket,
            risk=IGNORABLE_RISK,
            named=Route.ASK_FIRST_WITH_PREDRAFT,
        )
    )
    assert Route.PROCEED_SILENTLY not in cold.eligible, "one approval is not trust enough"

    approve(learner, router, REVERSIBLE, bucket, TRIALS)
    warm = router.route(
        RoutingRequest(
            case_id=REVERSIBLE,
            allowed=ALL_ROUTES,
            bucket=bucket,
            risk=IGNORABLE_RISK,
            named=Route.ASK_FIRST_WITH_PREDRAFT,
        )
    )
    assert {Route.PROCEED_SILENTLY, Route.PROCEED_AND_NOTIFY} <= set(warm.eligible)
    assert warm.route is Route.PROCEED_SILENTLY

    # And the identical volume on the fenced class is still worth nothing.
    fenced = bucket_for(MONEY)
    fenced_learner = Learner()
    fenced_router = Router(fenced_learner)
    approve(fenced_learner, fenced_router, MONEY, fenced, TRIALS)
    verdict, _, _ = floor_verdict_for(case(MONEY))
    assert (
        ask_again(fenced_router, MONEY, verdict.allowed_routes, fenced, IGNORABLE_RISK).route
        is Route.ESCALATE
    )


def test_an_external_send_is_never_silent_or_notified():
    """The class ceiling holds for a send to a third party, out of the mail's own thread."""
    email = email_context_for(case(REVERSIBLE))
    action = ActionPayload(
        tool_name="send_email",
        params={"to": ["analyst@other.example"], "body": "here is the deck"},
    )
    verdict = floor_check(action, email=email)
    assert verdict.action_class is ActionClass.IRREVERSIBLE_EXTERNAL
    assert verdict.allowed_routes == (Route.ASK_FIRST_WITH_PREDRAFT, Route.ESCALATE)

    bucket = Bucket(sender="analyst@other.example", intent="information request", action="email.send")
    learner = Learner()
    router = Router(learner)
    approve(learner, router, REVERSIBLE, bucket, TRIALS)
    assert router.store.posterior(bucket).mean > 0.8

    for _ in range(200):
        routing = ask_again(router, "external-send", verdict.allowed_routes, bucket, PLAIN_RISK)
        assert routing.route is Route.ASK_FIRST_WITH_PREDRAFT
        assert not set(routing.allowed) & AUTONOMOUS_ROUTES
        assert not set(routing.eligible) & AUTONOMOUS_ROUTES


def test_no_cost_table_can_put_a_masked_route_back_on_the_ballot():
    """A table that pays nothing for silence and a fortune for asking cannot reach it."""
    must_act = replace(
        LOSS_V1,
        version="loss-adversarial",
        missed_notification=0.0,
        wrong_action=0.0,
        wrong_audience=0.0,
        notified=0.0,
        interruption=1000.0,
        delay=1000.0,
    )
    allowed = ALL_ROUTES
    bucket = bucket_for(REVERSIBLE)

    # The table is genuinely adversarial: where the floor allows it, it buys silence.
    framed = Router(costs=must_act).route(
        RoutingRequest(
            case_id=REVERSIBLE,
            allowed=allowed,
            bucket=bucket,
            risk=IGNORABLE_RISK,
            named=Route.PROCEED_SILENTLY,
        )
    )
    assert framed.route is Route.PROCEED_SILENTLY

    # The same table, and an unknown next version of it, cannot touch a fenced case.
    verdict, _, _ = floor_verdict_for(case(MONEY))
    fenced = bucket_for(MONEY)
    for versioned in (must_act, replace(must_act, version="loss-v99")):
        routing = Router(costs=versioned).route(
            RoutingRequest(
                case_id=MONEY,
                allowed=verdict.allowed_routes,
                bucket=fenced,
                risk=IGNORABLE_RISK,
                named=Route.PROCEED_SILENTLY,
            )
        )
        assert routing.route is Route.ESCALATE
        assert [loss.route for loss in routing.alternatives] == [Route.ESCALATE]
        assert routing.value == 2000.0, "the only route left is priced at the unit"


def test_silence_and_a_reply_teach_nothing():
    """NONE, IGNORE_OBSERVED and REPLY are observations, so they move no posterior."""
    bucket = bucket_for(MONEY)
    learner = Learner()
    router = Router(learner)
    before = router.store.posterior(bucket)
    cutoffs = router.thresholds.for_bucket(bucket)

    for index, kind in enumerate(
        (FeedbackKind.NONE, FeedbackKind.IGNORE_OBSERVED, FeedbackKind.REPLY)
    ):
        event = feedback(kind, MONEY, index=index)
        assert is_learnable(kind) is False
        assert learner.observe(event, bucket) is False
        assert router.observe(event, bucket) is False

    assert learner.updates == 0
    assert learner.ignored == 3
    assert router.store.posterior(bucket) == before
    assert router.thresholds.for_bucket(bucket) == cutoffs == Cutoffs()


def test_a_replayed_decision_is_counted_once():
    """The same event id twice - a resumed decision, a replayed run - moves nothing twice."""
    bucket = bucket_for(REVERSIBLE)
    learner = Learner()
    router = Router(learner)
    event = feedback(FeedbackKind.APPROVE, REVERSIBLE, index=0, route=Route.PROCEED_AND_NOTIFY)

    assert learner.observe(event, bucket) is True
    assert router.observe(event, bucket) is True
    counted = router.store.posterior(bucket)
    cutoffs = router.thresholds.for_bucket(bucket)

    for _ in range(3):
        assert learner.observe(event, bucket) is False
        assert router.observe(event, bucket) is False

    assert learner.applied == 1
    assert router.store.posterior(bucket) == counted
    assert router.thresholds.for_bucket(bucket) == cutoffs


def test_a_cold_context_starts_distrustful():
    """Nobody has said anything anywhere: silence is not on the ballot and asking wins."""
    routing = Router().route(
        RoutingRequest(
            case_id=MONEY,
            allowed=ALL_ROUTES,
            bucket=Bucket(sender="a@b.example", intent="unseen", action="email.archive"),
            risk=PLAIN_RISK,
        )
    )
    assert routing.posterior.mean == 0.25, "Beta(1, 3), the distrustful prior"
    assert routing.posterior.evidence == 0.0
    assert not set(routing.eligible) & AUTONOMOUS_ROUTES
    assert routing.route is Route.ASK_FIRST_WITH_PREDRAFT


def test_a_run_that_hears_only_silence_never_escalates_itself_and_never_learns():
    """The proof at pipeline level: a fenced bill, unanswered, leaves the learner cold."""
    queue: asyncio.Queue[Any] = asyncio.Queue()
    asyncio.run(close_input(queue))
    learner = Learner()
    router = Router(learner)
    out = io.StringIO()

    outcome = asyncio.run(
        run_simulation(
            one_case_view(MONEY),
            seed=7,
            out=out,
            input_queue=queue,
            learner=learner,
            router=router,
        )
    )

    assert outcome.route_counts == {Route.ESCALATE.value: 1}
    assert outcome.receipts == [], "a fenced case commits nothing on its own"
    assert outcome.refusals, "the refusal is reported rather than swallowed"
    assert outcome.silent_ends == 1, "silence at the end of input is recorded as silence"
    assert learner.updates == 0, "silence reached no posterior"
    assert router.store.posterior(bucket_for(MONEY)).evidence == 0.0
    assert "AUTHORIZATION_REFUSED" in out.getvalue()


def test_a_warmed_learner_cannot_loosen_a_fenced_case_at_run_time():
    """Thousands of approvals in the learner, and the same run still escalates."""
    bucket = bucket_for(MONEY)
    learner = Learner()
    router = Router(learner)
    approve(learner, router, MONEY, bucket, TRIALS)
    earned = learner.updates

    queue: asyncio.Queue[Any] = asyncio.Queue()
    asyncio.run(close_input(queue))
    outcome = asyncio.run(
        run_simulation(
            one_case_view(MONEY),
            seed=7,
            out=io.StringIO(),
            input_queue=queue,
            learner=learner,
            router=router,
        )
    )

    assert outcome.route_counts == {Route.ESCALATE.value: 1}
    assert outcome.effects("send_email") == 0
    assert outcome.effects("label") == 0
    assert learner.updates == earned, "the run itself learned nothing from silence"
    assert router.store.posterior(bucket).mean > 0.8, "the trust was there and did not help"


def test_a_vetoed_case_arrives_as_one_route_and_it_is_the_escalation():
    """A veto is not one more thing to weigh: it leaves a single route on the ballot."""
    for case_id in (MONEY, SECRETS):
        verdict, _, _ = floor_verdict_for(case(case_id))
        assert verdict.veto is True, f"{case_id} must be vetoed to be a protected case"
        assert verdict.allowed_routes == (Route.ESCALATE,)
        routing = ask_again(
            Router(), case_id, verdict.allowed_routes, bucket_for(case_id), IGNORABLE_RISK
        )
        assert routing.route is Route.ESCALATE
        assert [loss.route for loss in routing.alternatives] == [Route.ESCALATE]
