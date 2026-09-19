"""The Jev hybrid: Jev decides the route, the model does the work, the floor still rules."""
import asyncio
import json
from pathlib import Path

import pytest

from agent.dataset import Lane, Manifest
from agent.events import Direction, Message, SenderIdentity
from agent.gateway import ProposalError, ProposalGateway, ProposalRequest
from agent.jev import Jev, JevError, JevRouted, route_by_jev
from agent.safety.floor import Route
from agent.sim.policy import ProposalPolicy
from agent.triage import triage
from agent.usage import Ledger

FIXTURE = Path(__file__).parent / "fixtures" / "stream_12.jsonl"
# The wire-transfer invoice: unknown vendor, unverified sender, asking for money.
WIRE_CASE = "WAJO-0011"

ROUTES = ("PROCEED_SILENTLY", "PROCEED_AND_NOTIFY", "ASK_FIRST_WITH_PREDRAFT", "ESCALATE")


def message(*, verified: bool = True) -> Message:
    return Message(
        message_id="m-1",
        thread_id="th-1",
        sender=SenderIdentity(
            email="elena@techcorp.synthetic.example",
            display_name="Elena Rostova",
            verified_identity=verified,
        ),
        recipients=("aydin@techcorp.synthetic.example",),
        direction=Direction.INBOUND,
        subject="Quick catchup this week?",
        body="Would you have time for a quick sync on Thursday?",
    )


class ScriptedModel:
    """The text model, answering from a script so nothing reaches a network."""

    name = "scripted"
    label = "scripted:v1"

    def __init__(self, *answers: str) -> None:
        self.answers = list(answers)
        self.asked = 0

    async def complete(self, request) -> str:
        self.asked += 1
        return self.answers.pop(0) if self.answers else "{"


def work(route: str = "PROCEED_AND_NOTIFY", action: str = "email.apply_label") -> str:
    """What the text model answers: an action and its arguments, no route of its own."""
    return json.dumps(
        {
            "route": route,
            "action_id": action,
            "params": {"label": "Newsletter"},
            "rationale": "bulk mail, filed",
            "confidence": 0.8,
        }
    )


def reply(choice: str, *, cost: float = 0.00002) -> dict:
    """One Jev response, in the shape the endpoint actually returns."""
    probabilities = {name: 0.05 for name in ROUTES}
    probabilities[choice] = 0.85
    return {
        "model": "typesafe/jev-1.13-test",
        "answers": {
            "route": {
                "type": "choice",
                "choice": choice,
                "probabilities": probabilities,
                "confidence": 0.7,
            }
        },
        "usage": {"input_tokens": 442, "output_tokens": 64, "cost": cost},
    }


class FakeJev:
    """A transport standing in for the endpoint: one answer, or one named failure."""

    def __init__(self, choice: str = "PROCEED_SILENTLY", *, error: Exception | None = None) -> None:
        self.choice = choice
        self.error = error
        self.bodies: list[dict] = []

    def __call__(self, body: dict) -> dict:
        self.bodies.append(body)
        if self.error is not None:
            raise self.error
        return reply(self.choice)


def hybrid(choice: str, *answers: str, **kwargs) -> tuple[JevRouted, ScriptedModel, Ledger]:
    """A wrapped model, the model's own script, and the ledger both of them write into."""
    ledger = Ledger()
    transport = kwargs.pop("transport", None) or FakeJev(choice)
    jev = Jev(api_key="test-key", transport=transport, ledger=ledger)
    model = ScriptedModel(*answers)
    return JevRouted(jev, model), model, ledger


def answer(provider: JevRouted) -> dict:
    """Drive the wrapper the way the gateway does, and hand back what it answered."""
    mail = message()
    request = ProposalRequest(message=mail, hints=triage(mail))
    return json.loads(asyncio.run(provider.complete(request)))


def test_jev_answers_the_route_and_the_model_answers_the_work() -> None:
    provider, model, _ = hybrid("PROCEED_AND_NOTIFY", work())

    proposal = answer(provider)

    assert proposal["route"] == "PROCEED_AND_NOTIFY"
    assert proposal["action_id"] == "email.apply_label"
    assert proposal["params"] == {"label": "Newsletter"}
    # The calibrated mass on the chosen route is the confidence the schema carries.
    assert proposal["confidence"] == pytest.approx(0.85)
    assert "jev: PROCEED_AND_NOTIFY" in proposal["rationale"]
    assert model.asked == 1


def test_an_escalation_never_pays_for_the_work() -> None:
    """No work to prepare, so the text model is not called at all."""
    provider, model, _ = hybrid("ESCALATE")

    proposal = answer(provider)

    assert proposal["route"] == "ESCALATE"
    assert proposal["action_id"] is None
    assert model.asked == 0


def test_an_ask_with_no_draft_in_it_gets_one_to_ask_with() -> None:
    provider, _, _ = hybrid("ASK_FIRST_WITH_PREDRAFT", work(action="email.apply_label"))

    proposal = answer(provider)

    assert proposal["route"] == "ASK_FIRST_WITH_PREDRAFT"
    assert proposal["action_id"] == "email.create_draft"
    assert proposal["params"] == {}


def test_a_routing_opinion_that_never_arrives_falls_back_to_the_model() -> None:
    provider, _, _ = hybrid(
        "PROCEED_SILENTLY", work(route="PROCEED_AND_NOTIFY"), transport=FakeJev(error=JevError("504"))
    )

    proposal = answer(provider)

    assert proposal["route"] == "PROCEED_AND_NOTIFY"
    assert "jev unavailable" in proposal["rationale"]
    assert provider.fallbacks == 1


def test_an_answer_outside_the_four_routes_is_refused_not_guessed() -> None:
    provider, _, _ = hybrid("MAYBE", work(route="PROCEED_AND_NOTIFY"))

    proposal = answer(provider)

    # The wrapper never guesses: the model's own route stands, and the reason is on the record.
    assert proposal["route"] == "PROCEED_AND_NOTIFY"
    assert "jev unavailable" in proposal["rationale"]
    assert provider.fallbacks == 1


def test_the_floor_still_rules_a_route_jev_chose() -> None:
    """The safety property: a decision model saying silence cannot silence a wire request."""
    view = Manifest.load(FIXTURE).view(Lane.CALIBRATION)
    provider, _, _ = hybrid(
        "PROCEED_SILENTLY", work(route="PROCEED_SILENTLY", action="email.archive")
    )

    decision = asyncio.run(ProposalPolicy(ProposalGateway(provider)).decide(view.open(WIRE_CASE)))

    assert decision.route is Route.ESCALATE
    assert "floor" in decision.reason or "ESCALATE" in decision.reason


def test_the_decision_is_metered_under_its_own_stage_with_the_price_it_reported() -> None:
    provider, _, ledger = hybrid("PROCEED_SILENTLY", work())

    answer(provider)

    rows = {row.stage: row for row in ledger.rows()}
    assert "jev/route" in rows
    row = rows["jev/route"]
    assert row.calls == 1
    assert row.model == "typesafe/jev-1.13-test"
    assert row.tokens == 442 + 64
    # The endpoint priced its own call, so the rate table is not consulted for it.
    assert row.cost == pytest.approx(0.00002)


def test_the_hybrid_needs_a_key_to_route(monkeypatch) -> None:
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    with pytest.raises(ProposalError, match="OPENROUTER_API_KEY"):
        route_by_jev(ScriptedModel(work()))


def test_the_state_jev_reads_is_the_mail_and_the_hints() -> None:
    transport = FakeJev("PROCEED_SILENTLY")
    provider, _, _ = hybrid("PROCEED_SILENTLY", work(), transport=transport)

    answer(provider)

    body = transport.bodies[0]
    assert body["model"] == "~typesafe/jev-latest"
    assert "elena@techcorp.synthetic.example" in body["state"]
    assert "intent=" in body["state"]
    question = body["questions"]["route"]
    assert question["type"] == "choice"
    assert set(question["criteria"]) == set(ROUTES)
