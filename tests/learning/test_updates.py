from __future__ import annotations

import asyncio
import io
from dataclasses import replace
from datetime import UTC, datetime
from pathlib import Path

from agent.autonomy.bandit import Learner
from agent.autonomy.confidence import REVERT_WEIGHT, Bucket
from agent.dataset import Lane, LaneView, Manifest
from agent.events import FeedbackEvent, FeedbackKind, is_learnable
from agent.memory.claims import Claim, ClaimScope, ClaimType, ScopeAnchor
from agent.safety.floor import Route
from agent.sim.runner import close_input, run_simulation

FIXTURE = Path(__file__).parent.parent / "fixtures" / "stream_12.jsonl"
RECRUITER = "WAJO-0008"
RECRUITER_SENDER = "claire@nexustalent.synthetic.example"

CONTEXT = Bucket(
    sender=RECRUITER_SENDER, intent="recruiter follow-up", action="email.create_draft"
)
NOW = datetime(2026, 8, 1, 9, 0, tzinfo=UTC)


def view() -> LaneView:
    return Manifest.load(FIXTURE).view(Lane.CALIBRATION)


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


def test_duplicate_feedback_is_counted_once():
    learner = Learner()
    event = feedback(FeedbackKind.APPROVE)

    assert learner.observe(event, CONTEXT) is True
    once = learner.store.posterior(CONTEXT)
    assert learner.observe(event, CONTEXT) is False
    assert learner.store.posterior(CONTEXT) == once
    assert learner.updates == 1
    assert learner.ignored == 1


def test_silence_is_never_counted():
    """A decision nobody answered is not an approval, and not evidence of any kind."""
    learner = Learner()
    for kind in (
        FeedbackKind.NONE,
        FeedbackKind.IGNORE_OBSERVED,
        FeedbackKind.REPLY,
    ):
        assert learner.observe(feedback(kind), CONTEXT) is False
    assert learner.store.posterior(CONTEXT).mean == 0.25
    assert learner.updates == 0


def test_a_revert_outweighs_several_approvals():
    """One undo says more than a run of silences, so it counts as three rejections."""
    approvals = Learner()
    for index in range(3):
        approvals.observe(
            feedback(FeedbackKind.APPROVE, event_id=f"c:approve:{index}"), CONTEXT
        )

    reverted = Learner()
    reverted.observe(feedback(FeedbackKind.APPROVE, event_id="c:1"), CONTEXT)
    reverted.observe(feedback(FeedbackKind.REVERT, event_id="c:2"), CONTEXT)

    assert reverted.store.posterior(CONTEXT).beta == 3 + REVERT_WEIGHT
    assert reverted.store.posterior(CONTEXT).mean < approvals.store.posterior(CONTEXT).mean


def test_a_confirmed_rule_counts_the_route_it_chose_not_the_words_that_chose_it():
    """"Never tell me about these" is a never in the user's words and a yes in effect."""
    learner = Learner()
    learner.observe(
        feedback(FeedbackKind.NEVER_DO_THIS, route=Route.PROCEED_SILENTLY, action="email.archive"),
        CONTEXT,
        claim=rule(route=Route.PROCEED_SILENTLY, action="email.archive"),
    )
    assert learner.store.posterior(CONTEXT).mean > 0.25
    assert learner.refusals == 0


def test_a_rule_that_keeps_the_user_in_it_counts_against_autonomy():
    learner = Learner()
    for index, route in enumerate((Route.ASK_FIRST_WITH_PREDRAFT, Route.ESCALATE)):
        learner.observe(
            feedback(FeedbackKind.ALWAYS_DO_THIS, event_id=f"c:{index}", route=route, action=None),
            CONTEXT,
            claim=rule(route=route, action=None),
        )
    assert learner.store.posterior(CONTEXT).mean < 0.25


def test_a_never_claim_masks_the_matching_arm():
    learner = Learner()
    learner.observe(
        feedback(FeedbackKind.NEVER_DO_THIS, action="email.archive"),
        CONTEXT,
        claim=rule(route=None, action="email.archive"),
    )

    assert learner.refuses(Bucket(sender=RECRUITER_SENDER, action="email.archive")) == (
        "clm-90598ef7a3ac"
    )
    assert learner.refuses(Bucket(sender=RECRUITER_SENDER, action="email.create_draft")) == ""
    assert learner.refuses(Bucket(sender="someone@else.example", action="email.archive")) == ""
    assert learner.refusals == 1


def test_a_refusal_scoped_to_an_intent_covers_every_sender_of_that_intent():
    learner = Learner()
    claim = replace(
        rule(route=None, action="email.archive"),
        scope=ClaimScope(intent="newsletter"),
        scope_anchor=ScopeAnchor.INTENT,
    )
    learner.observe(
        feedback(FeedbackKind.NEVER_DO_THIS, action="email.archive"), CONTEXT, claim=claim
    )
    assert learner.refuses(Bucket(sender="news@anywhere.example", intent="newsletter", action="email.archive"))
    assert learner.refuses(Bucket(sender="news@anywhere.example", intent="receipt", action="email.archive")) == ""


def test_a_calibration_run_counts_what_the_user_said():
    """The wiring, not just the rule: a line confirmed at a prompt moves a posterior."""
    queue: asyncio.Queue[str] = asyncio.Queue()
    learner = Learner()
    out = io.StringIO()

    async def hook(index: int, decision) -> None:
        if decision.case_id == RECRUITER:
            queue.put_nowait(f"ignore mail from {RECRUITER_SENDER}")
            queue.put_nowait("yes")
            await close_input(queue)
            return
        # A line that teaches nothing, so the run reaches the decision it is meant to reach.
        queue.put_nowait("nothing for now")

    outcome = asyncio.run(
        run_simulation(
            view(),
            seed=7,
            out=out,
            input_queue=queue,
            on_interrupt=hook,
            learner=learner,
        )
    )

    text = out.getvalue()
    assert [claim.action_id for claim in outcome.claims] == ["email.archive"]
    assert learner.updates == 1
    assert learner.ignored >= 1, "the lines that decided nothing were not counted"
    assert learner.store.contexts(), text
    assert learner.store.posterior(CONTEXT).mean > 0.25
    assert "posteriors:" in text and "recruiter follow-up" in text
