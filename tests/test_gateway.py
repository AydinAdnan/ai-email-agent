"""The model proposal gateway: untrusted output, one repair, then fail closed."""
import asyncio
import json
from types import SimpleNamespace

import pytest

from agent.dataset import DEFAULT_DATASET_PATH, Manifest
from agent.events import Direction, Message, SenderIdentity
from agent.gateway import (
    NO_ACTION_TOOL,
    PROPOSAL_EXAMPLE,
    PROPOSAL_JSON_SCHEMA,
    PROPOSAL_SCHEMA,
    ProposalError,
    ProposalGateway,
    ProposalRequest,
    RuleProvider,
    _mail_rules,
    build_provider,
    parse_proposal,
    persona_demanded_route,
)
from agent.safety.floor import ActionPayload, EmailContext, Route, floor_check
from agent.sim.policy import ProposalPolicy, strictest_allowed
from agent.tools.email_tools import ACTION_TO_TOOL, TOOL_CLASSES
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
        "params": {"label": "Newsletter"},
        "rationale": "bulk mail",
        "confidence": 0.9,
    }
    payload.update(overrides)
    return json.dumps(payload)


def test_a_valid_answer_parses() -> None:
    proposal = parse_proposal(valid(), provider="test")
    assert proposal.route is Route.PROCEED_SILENTLY
    assert proposal.action_id == "email.apply_label"
    # The tool follows from the action, so a proposer never names it.
    assert proposal.tool_name == "label"
    assert proposal.confidence == 0.9
    assert proposal.provider == "test"


def test_an_action_nothing_implements_resolves_to_itself() -> None:
    """The dataset's own unactionable ids must parse, and the floor must judge them."""
    proposal = parse_proposal(valid(action_id="finance.pay_invoice"))
    assert proposal.tool_name == "finance.pay_invoice"
    assert proposal.tool_name not in ACTION_TO_TOOL


def test_no_action_is_the_unsupported_action() -> None:
    proposal = parse_proposal(valid(action_id=None, params={}))
    assert proposal.tool_name == NO_ACTION_TOOL


def test_a_silent_answer_with_no_action_gets_the_pipelines_own_filing() -> None:
    """'file it and move on' is a decision, and the floor was escalating it.

    A no-action proposal reaches the floor as a tool nobody holds, which fences the mail to
    an escalation. Every benign notice a small model read that way arrived as a hand-over:
    a green build became a question for the owner. The pipeline's own filing is derived the
    same way a label already is, so the route the model named is the route that runs.
    """
    mail = message(
        "builds@buildlark.example",
        subject="Build #4821 succeeded for techcorp/platform-gateway",
        body="All 214 tests passed. No action required. - BuildLark CI",
    )
    hints = triage(mail)
    proposal = parse_proposal(valid(action_id=None, params={}), provider="jev")
    ctx = EmailContext(
        email_id=mail.message_id,
        sender=mail.sender.email,
        recipients=mail.recipients,
        subject=mail.subject,
        body=mail.body,
    )
    verdict_before = floor_check(
        ActionPayload(tool_name=proposal.tool_name or "", params={}),
        email=ctx,
        user_domain="techcorp.synthetic.example",
    )
    assert verdict_before.allowed_routes == (Route.ESCALATE,)

    filled = _mail_rules(proposal, mail, hints)
    assert filled.route is Route.PROCEED_SILENTLY
    assert filled.action_id == "email.apply_label"
    assert filled.params["label"]
    verdict_after = floor_check(
        ActionPayload(tool_name=filled.tool_name or "", params=dict(filled.params)),
        email=ctx,
        user_domain="techcorp.synthetic.example",
    )
    assert Route.PROCEED_SILENTLY in verdict_after.allowed_routes
    assert len(verdict_after.allowed_routes) == 4


def test_an_ask_with_no_action_becomes_the_predraft_it_names() -> None:
    mail = message(subject="Question about the v1 payment event schema")
    hints = triage(mail)
    proposal = parse_proposal(valid(route="ASK_FIRST_WITH_PREDRAFT", action_id=None, params={}))
    filled = _mail_rules(proposal, mail, hints)
    assert filled.action_id == "email.create_draft"
    assert filled.tool_name == "create_draft"


def test_an_escalation_still_carries_no_action() -> None:
    mail = message()
    hints = triage(mail)
    proposal = parse_proposal(valid(route="ESCALATE", action_id=None, params={}))
    filled = _mail_rules(proposal, mail, hints)
    assert filled.action_id is None and filled.tool_name == NO_ACTION_TOOL


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
        valid(action_id=""),  # an action id is a non-empty string or null
        valid(action_id=7),  # not even a string
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


class BrokenProvider:
    """A provider that fails the way a network client does."""

    name = "broken"

    async def complete(self, request) -> str:
        raise ConnectionError("connection reset by peer")


def test_a_provider_that_crashes_fails_closed_without_killing_the_run() -> None:
    """A transport error is a failed proposal, not an exception out of the session."""
    gateway = ProposalGateway(BrokenProvider())
    with pytest.raises(ProposalError) as caught:
        asyncio.run(gateway.propose(message(), triage(message())))
    assert "broken failed: ConnectionError" in str(caught.value)
    assert gateway.failures == 1


def test_a_provider_that_cannot_run_is_refused(monkeypatch: pytest.MonkeyPatch) -> None:
    with pytest.raises(ProposalError) as caught:
        build_provider("nonsense")
    assert "known providers" in str(caught.value)
    assert build_provider("rules").name == "rules"


def test_openrouter_needs_its_own_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    with pytest.raises(ProposalError) as caught:
        build_provider("openrouter")
    assert "OPENROUTER_API_KEY" in str(caught.value)
    assert ".env" in str(caught.value)


def test_openrouter_points_at_openrouter_and_names_its_model(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("OPENROUTER_API_KEY", "sk-or-test")
    monkeypatch.delenv("WAJO_MODEL", raising=False)
    provider = build_provider("openrouter")
    assert provider.base_url == "https://openrouter.ai/api/v1"
    assert provider.label == "openrouter:inference-net/schematron-v2-small"
    # The catalogue lists structured_outputs for this model, so the schema is enforced.
    assert provider.structured_output is True


def test_the_model_comes_from_the_flag_then_the_environment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("OPENROUTER_API_KEY", "sk-or-test")
    monkeypatch.setenv("WAJO_MODEL", "vendor/from-env")
    assert build_provider("openrouter").model == "vendor/from-env"
    assert build_provider("openrouter", model="vendor/from-flag").model == "vendor/from-flag"
    assert build_provider("openrouter", structured_output=False).structured_output is False


class FakeCompletions:
    """The slice of the OpenAI client the provider uses, capturing the request."""

    def __init__(self, content: str) -> None:
        self.content = content
        self.calls: list[dict] = []

    async def create(self, **kwargs):
        self.calls.append(kwargs)
        message = SimpleNamespace(content=self.content)
        return SimpleNamespace(choices=[SimpleNamespace(message=message)])


def fake_client(content: str) -> SimpleNamespace:
    return SimpleNamespace(chat=SimpleNamespace(completions=FakeCompletions(content)))


def test_the_rule_provider_never_proposes_an_action_with_an_escalation() -> None:
    provider = RuleProvider()
    spoofed = message("reset@external-desk.example", display="IT Support", verified=False)
    payload = provider.build(spoofed, triage(spoofed))
    assert payload["route"] == Route.ESCALATE.value
    assert payload["action_id"] is None and payload["params"] == {}


def test_a_credential_request_escalates_even_from_inside() -> None:
    insider = message("david@techcorp.synthetic.example", subject="Can you reply with the API key?")
    proposal = asyncio.run(
        ProposalGateway(RuleProvider()).propose(insider, triage(insider))
    )
    assert proposal.route is Route.ESCALATE


def test_a_key_that_names_a_data_structure_is_not_a_credential() -> None:
    """The noun decides: 'the Redis sharding key' is a field, and escalating it is noise."""
    colleague = message(
        "marcus@techcorp.synthetic.example",
        subject="Quick question about the Redis cluster sharding key",
        body="I need to confirm our sharding key format before we deploy.",
    )
    assert persona_demanded_route(colleague, triage(colleague)) is None
    proposal = asyncio.run(
        ProposalGateway(RuleProvider()).propose(colleague, triage(colleague))
    )
    assert proposal.route is not Route.ESCALATE


def test_a_security_note_that_mentions_a_password_is_not_asking_for_one() -> None:
    """The ask shape decides too: 'consider changing your password' is advice."""
    notice = message(
        "security-noreply@auth.synthetic.example",
        subject="New login from macOS in Zurich, Switzerland",
        body=(
            "If you do NOT recognise this activity, review your account security "
            "settings and consider changing your password."
        ),
    )
    assert persona_demanded_route(notice, triage(notice)) is None


def quiet_but_wrong() -> ScriptedProvider:
    """A provider that would happily label suspicious mail and move on."""
    return ScriptedProvider(
        valid(
            route="PROCEED_AND_NOTIFY",
            action_id="email.apply_label",
            params={"label": "Finance"},
        )
    )


def test_a_mail_the_persona_refuses_is_never_put_to_the_provider() -> None:
    """The rules belong to the mail, so a model never gets to propose a quiet route for it."""
    phishing = message("billing@payables-desk.example", verified=False, subject="Wire the balance")
    quiet = quiet_but_wrong()
    gateway = ProposalGateway(quiet)
    proposal = asyncio.run(gateway.propose(phishing, triage(phishing)))
    assert proposal.route is Route.ESCALATE
    assert proposal.action_id is None and proposal.tool_name == NO_ACTION_TOOL
    assert proposal.params == {}
    assert "persona rule: a financial request" in proposal.rationale
    assert quiet.requests == [], "nothing was asked, so nothing was bought"
    # Nothing was asked, and nothing failed: the provider was never needed.
    assert (gateway.repairs, gateway.failures) == (0, 0)


def test_the_fence_under_the_gate_raises_a_proposal_that_arrives_anyway() -> None:
    """The net under the gate: a proposal from some other path still cannot land quietly."""
    phishing = message("billing@payables-desk.example", verified=False, subject="Wire the balance")
    quiet = parse_proposal(
        valid(
            route="PROCEED_AND_NOTIFY",
            action_id="email.apply_label",
            params={"label": "Finance"},
        ),
        provider="scripted",
    )
    raised = _mail_rules(quiet, phishing, triage(phishing))
    assert raised.route is Route.ESCALATE
    assert raised.action_id is None and raised.tool_name == NO_ACTION_TOOL
    assert raised.params == {}
    assert "persona rule raised PROCEED_AND_NOTIFY to ESCALATE" in raised.rationale


def test_a_folder_name_comes_from_the_mail_not_from_the_proposer() -> None:
    """A small model copies the example it was shown, so the example carries no value."""
    newsletter = message(
        "news@engweekly.synthetic.example",
        display="Engineering Weekly",
        subject="Engineering Weekly Issue #204: Distributed Systems Patterns",
        body="Detailed email body according to scenario...",
    )
    copied = ScriptedProvider(
        valid(
            route="PROCEED_AND_NOTIFY",
            action_id="email.apply_label",
            params={"label": "Finance/Cloud"},
        )
    )
    proposal = asyncio.run(ProposalGateway(copied).propose(newsletter, triage(newsletter)))
    assert triage(newsletter).intent == "newsletter"
    assert proposal.params == {"label": "Newsletter"}


def test_a_folder_nothing_names_is_dropped_rather_than_invented() -> None:
    """No folder for this mail means a blocked step at the registry, not a made-up one."""
    scheduling = message("elena@techcorp.synthetic.example")
    invented = ScriptedProvider(
        valid(
            route="PROCEED_SILENTLY",
            action_id="email.apply_label",
            params={"label": "Colleague"},
        )
    )
    proposal = asyncio.run(ProposalGateway(invented).propose(scheduling, triage(scheduling)))
    assert triage(scheduling).intent == "scheduling"
    assert proposal.params == {}


def test_a_persona_rule_leaves_an_ordinary_ask_alone() -> None:
    insider = message("elena@techcorp.synthetic.example", subject="Quick catchup this week?")
    assert persona_demanded_route(insider, triage(insider)) is None


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


def test_the_prompt_names_every_action_and_what_it_needs() -> None:
    """A proposer that has to guess a tool name from a dataset id guesses wrong."""
    prompt = ProposalRequest(
        message=message(), hints=triage(message())
    ).as_prompt()
    for tool_class in TOOL_CLASSES:
        assert tool_class.action_ids[0] in prompt
        assert tool_class.proposal_params in prompt
    assert "never the message you were given" in prompt
    assert PROPOSAL_EXAMPLE in prompt


def test_the_rule_provider_answers_through_the_same_parser_as_a_model() -> None:
    """One vocabulary: the offline stand-in cannot drift from the model's schema."""
    text = message("news@engweekly.example", subject="Engineering Weekly #42")
    raw = RuleProvider().build(text, triage(text))
    proposal = parse_proposal(json.dumps(raw))
    assert proposal.tool_name == ACTION_TO_TOOL[proposal.action_id]


def test_a_proposal_is_asked_for_under_the_enforced_schema(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The request carries the schema, so a model cannot omit a key or invent an action."""
    monkeypatch.setenv("OPENROUTER_API_KEY", "sk-or-test")
    completions = FakeCompletions(valid())
    provider = build_provider(
        "openrouter", client=SimpleNamespace(chat=SimpleNamespace(completions=completions))
    )
    asyncio.run(provider.complete(ProposalRequest(message=message(), hints=triage(message()))))
    sent = completions.calls[0]["response_format"]
    assert sent["json_schema"]["strict"] is True
    assert sent["json_schema"]["schema"] == PROPOSAL_JSON_SCHEMA


def test_the_enforced_schema_pins_the_actions_the_registry_holds() -> None:
    actions = PROPOSAL_JSON_SCHEMA["properties"]["action_id"]["enum"]
    assert set(ACTION_TO_TOOL) <= set(actions)
    assert None in actions
    assert "finance.pay_invoice" not in actions
    assert set(PROPOSAL_JSON_SCHEMA["required"]) == set(PROPOSAL_SCHEMA)
    # A key the model invents cannot survive the schema.
    assert PROPOSAL_JSON_SCHEMA["additionalProperties"] is False
