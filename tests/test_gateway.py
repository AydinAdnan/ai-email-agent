"""The model proposal gateway: untrusted output, one repair, then fail closed."""
import asyncio
import json

import pytest

from agent.dataset import DEFAULT_DATASET_PATH, Manifest
from agent.events import Direction, Message, SenderIdentity
from agent.gateway import (
    NO_ACTION_TOOL,
    ProposalError,
    ProposalGateway,
    RuleProvider,
    build_provider,
    parse_proposal,
)
from agent.safety.floor import ActionPayload, EmailContext, Route, floor_check
from agent.sim.policy import ProposalPolicy, strictest_allowed
from agent.triage import triage


def message(
    sender: str = "elena@techcorp.synthetic.example",
    *,
    display: str = "",
    verified: bool = True,
    subject: str = "Quick catchup this week?",
    body: str = "Would you have time for a quick sync?",
    to: tuple[str, ...] = ("aydin@techcorp.synthetic.example",),
) -> Message:
    return Message(
        message_id="m-1",
        thread_id="th-1",
        sender=SenderIdentity(email=sender, display_name=display, verified_identity=verified),
        recipients=to,
        direction=Direction.INBOUND,
        subject=subject,
        body=body,
    )


class ScriptedProvider:
    """A provider that answers from a script, so the repair logic is testable."""

    name = "scripted"

    def __init__(self, *answers: str) -> None:
        self.answers = list(answers)
        self.requests: list[str] = []

    async def complete(self, request) -> str:
        self.requests.append(request.as_prompt())
        return self.answers.pop(0) if self.answers else "{"


class SlowProvider:
    name = "slow"

    async def complete(self, request) -> str:
        await asyncio.sleep(1)
        return "{}"


def valid(route: str = "PROCEED_SILENTLY", **overrides) -> str:
    payload = {
        "route": route,
        "action_id": "email.apply_label",
        "tool_name": "label",
        "params": {"label": "Newsletter"},
        "rationale": "bulk mail",
        "confidence": 0.9,
    }
    payload.update(overrides)
    return json.dumps(payload)


def test_a_valid_answer_parses() -> None:
    proposal = parse_proposal(valid(), provider="test")
    assert proposal.route is Route.PROCEED_SILENTLY
    assert proposal.tool_name == "label"
    assert proposal.confidence == 0.9
    assert proposal.provider == "test"


def test_a_fenced_answer_parses() -> None:
    assert parse_proposal(f"```json\n{valid()}\n```").route is Route.PROCEED_SILENTLY


@pytest.mark.parametrize(
    "raw",
    [
        "",
        "   ",
        "not json at all",
        "[]",
        json.dumps({"route": "PROCEED_SILENTLY"}),  # no rationale
        valid(route="PROCEED_MAYBE"),  # not a route
        valid(params="label"),  # params must be an object
        valid(confidence=7),  # confidence is a probability
        valid(action_id="email.apply_label", tool_name=None),  # half an action
        valid(route="ESCALATE"),  # escalation carries no action
    ],
)
def test_an_unusable_answer_is_an_error_not_a_default(raw: str) -> None:
    with pytest.raises(ProposalError):
        parse_proposal(raw)


def test_one_repair_is_all_that_is_bought() -> None:
    provider = ScriptedProvider("garbage", valid())
    gateway = ProposalGateway(provider)
    proposal = asyncio.run(gateway.propose(message(), triage(message())))
    assert proposal.route is Route.PROCEED_SILENTLY
    assert (gateway.repairs, gateway.failures) == (1, 0)
    assert len(provider.requests) == 2
    assert "rejected" in provider.requests[1], "the repair has to quote the complaint"


def test_a_second_failure_fails_closed() -> None:
    provider = ScriptedProvider("garbage", "still garbage")
    gateway = ProposalGateway(provider)
    with pytest.raises(ProposalError):
        asyncio.run(gateway.propose(message(), triage(message())))
    assert (gateway.repairs, gateway.failures) == (1, 1)


def test_a_provider_that_never_answers_times_out() -> None:
    gateway = ProposalGateway(SlowProvider(), timeout=0.01)
    with pytest.raises(ProposalError):
        asyncio.run(gateway.propose(message(), triage(message())))
    assert gateway.failures == 1


def test_a_provider_that_cannot_run_is_refused() -> None:
    with pytest.raises(ProposalError):
        build_provider("nonsense")
    assert build_provider("rules").name == "rules"


def test_the_rule_provider_never_proposes_an_action_with_an_escalation() -> None:
    provider = RuleProvider()
    spoofed = message("reset@external-desk.example", display="IT Support", verified=False)
    payload = provider.build(spoofed, triage(spoofed))
    assert payload["route"] == Route.ESCALATE.value
    assert payload["action_id"] is None and payload["tool_name"] is None


def test_a_credential_request_escalates_even_from_inside() -> None:
    insider = message("david@techcorp.synthetic.example", subject="Can you reply with the key?")
    payload = RuleProvider().build(insider, triage(insider))
    assert payload["route"] == Route.ESCALATE.value


def test_a_receipt_above_the_threshold_is_notified() -> None:
    provider = RuleProvider()
    cheap = message("receipts@cornercafe.synthetic.example", subject="Your receipt from Corner Cafe ($14.50)")
    dear = message("receipts@cornercafe.synthetic.example", subject="Your receipt from Corner Cafe ($1,420.00)")
    assert provider.build(cheap, triage(cheap))["route"] == Route.PROCEED_SILENTLY.value
    assert provider.build(dear, triage(dear))["route"] == Route.PROCEED_AND_NOTIFY.value


def test_strictest_allowed_is_the_least_autonomous_route() -> None:
    verdict = floor_check(
        ActionPayload(tool_name="send_email", params={"to": ["a@external.example"]}),
        email=EmailContext(
            email_id="e-1",
            sender="x@example.com",
            recipients=("me@techcorp.synthetic.example",),
            subject="subject",
            body="body",
        ),
    )
    assert strictest_allowed(verdict) is Route.ESCALATE


def test_a_proposal_about_an_external_send_cannot_act_by_itself() -> None:
    """The floor wins over a confident proposal, which is the whole contract."""
    case = Manifest.load(DEFAULT_DATASET_PATH).cases[0]
    silent_proposal = ScriptedProvider(
        valid(
            route="PROCEED_SILENTLY",
            action_id="email.send",
            tool_name="send_email",
            params={"to": ["stranger@external.example"], "body": "hi"},
        )
    )
    policy = ProposalPolicy(ProposalGateway(silent_proposal))
    decision = asyncio.run(policy.decide(case))
    assert decision.route is not Route.PROCEED_SILENTLY
    assert decision.verdict.veto is not None
    assert decision.source == "proposal"


def test_no_usable_proposal_escalates_instead_of_guessing() -> None:
    case = Manifest.load(DEFAULT_DATASET_PATH).cases[0]
    policy = ProposalPolicy(ProposalGateway(ScriptedProvider("{", "{")))
    decision = asyncio.run(policy.decide(case))
    assert decision.route is Route.ESCALATE
    assert decision.tool_name == NO_ACTION_TOOL
    assert "no usable proposal" in decision.reason
