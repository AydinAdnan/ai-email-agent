"""The cost meter: it has to count what was spent, and admit what it cannot price."""
import asyncio
from types import SimpleNamespace

import pytest

from agent.gateway import (
    ENDPOINTS,
    NO_ACTION_TOOL,
    OpenAICompatibleProvider,
    ProposalGateway,
    ProposalRequest,
    RuleProvider,
)
from agent.safety.floor import Route
from agent.triage import triage
from agent.usage import PRICES, Ledger, Spend
from tests.test_gateway import message, valid


def response(*, content: str, prompt: int, completion: int) -> SimpleNamespace:
    """The slice of an OpenAI response the provider reads, usage included."""
    return SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content=content))],
        usage=SimpleNamespace(prompt_tokens=prompt, completion_tokens=completion),
    )


class MeteredCompletions:
    """A model endpoint that reports usage, so the meter has something to read."""

    def __init__(self, *answers: SimpleNamespace) -> None:
        self.answers = list(answers)

    async def create(self, **kwargs):
        return self.answers.pop(0)


def provider(
    *answers: SimpleNamespace, model: str = "inference-net/schematron-v2-small"
) -> OpenAICompatibleProvider:
    client = SimpleNamespace(
        chat=SimpleNamespace(completions=MeteredCompletions(*answers)),
    )
    return OpenAICompatibleProvider(ENDPOINTS["openrouter"], api_key="test", model=model, client=client)


def test_a_call_is_counted_with_the_tokens_the_response_reported() -> None:
    ledger = Ledger()
    metered = provider(response(content=valid(), prompt=820, completion=64))
    metered.ledger = ledger
    asyncio.run(ProposalGateway(metered).propose(message(), triage(message())))

    (row,) = ledger.rows()
    assert (row.stage, row.calls) == ("proposal", 1)
    assert (row.prompt_tokens, row.completion_tokens) == (820, 64)
    assert ledger.arrivals == 1 and ledger.deflected == 0


def test_the_cost_is_the_published_rate_for_that_sample() -> None:
    row = Spend("proposal", "openrouter", "inference-net/schematron-v2-small", 1, 1_000_000, 1_000_000)
    per_input, per_output = PRICES["inference-net/schematron-v2-small"]
    assert row.cost == pytest.approx(per_input + per_output)


def test_a_model_nobody_prices_is_unpriced_rather_than_free() -> None:
    ledger = Ledger()
    ledger.record(stage="proposal", provider="openrouter", model="vendor/unlisted", prompt_tokens=10, completion_tokens=5)
    assert ledger.rows()[0].cost is None
    assert ledger.unpriced == ledger.rows()
    assert ledger.cost == 0.0, "an unpriced row is excluded from the total, not counted as zero cost"
    assert "unpriced and excluded: vendor/unlisted" in ledger.render()
    assert ledger.render().count("n/a") >= 1


def silent_completions() -> MeteredCompletions:
    """A response with no usage at all, which is what a proxy sometimes returns."""
    answer = SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content=valid()))])
    return MeteredCompletions(answer)


def test_a_response_without_usage_is_a_call_that_reported_no_tokens() -> None:
    ledger = Ledger()
    metered = OpenAICompatibleProvider(
        ENDPOINTS["openrouter"],
        api_key="test",
        ledger=ledger,
        client=SimpleNamespace(chat=SimpleNamespace(completions=silent_completions())),
    )
    asyncio.run(ProposalGateway(metered).propose(message(), triage(message())))
    assert ledger.rows()[0].tokens == 0
    assert ledger.rows()[0].cost == 0.0


def test_the_offline_provider_is_counted_and_costs_nothing() -> None:
    """A table that hid the rules provider would show a run spending nothing and doing nothing."""
    ledger = Ledger()
    metered = RuleProvider(ledger=ledger)
    asyncio.run(ProposalGateway(metered).propose(message(), triage(message())))
    (row,) = ledger.rows()
    assert (row.provider, row.calls, row.cost) == ("rules", 1, 0.0)


def test_a_repair_is_a_second_call_in_its_own_stage() -> None:
    ledger = Ledger()
    metered = provider(
        response(content="garbage", prompt=810, completion=20),
        response(content=valid(), prompt=900, completion=64),
    )
    gateway = ProposalGateway(metered, ledger=ledger)
    asyncio.run(gateway.propose(message(), triage(message())))
    stages = {row.stage: row for row in ledger.rows()}
    assert set(stages) == {"proposal", "proposal (repair)"}
    assert stages["proposal (repair)"].calls == 1
    assert ledger.arrivals == 1 and ledger.calls == 2


def test_mail_the_persona_refuses_is_settled_without_asking_the_provider() -> None:
    """No call, no tokens, and the deflection is what makes the saving countable."""
    ledger = Ledger()
    metered = provider()
    phishing = message("billing@payables-desk.example", verified=False, subject="Wire the balance")
    proposal = asyncio.run(ProposalGateway(metered, ledger=ledger).propose(phishing, triage(phishing)))

    assert proposal.route is Route.ESCALATE
    assert proposal.tool_name == NO_ACTION_TOOL and proposal.action_id is None
    assert ledger.calls == 0 and ledger.rows() == ()
    assert (ledger.arrivals, ledger.deflected) == (1, 1)
    assert ledger.deflection_rate == 1.0
    assert "persona rule: a financial request" in proposal.rationale


def test_the_gateway_and_its_provider_share_one_meter() -> None:
    """Two tables for one run is how a cost report starts under-reporting.

    The meter is this test's own: reading the process-wide one made the count depend on
    which tests ran before it, so the check passed or failed by running order.
    """
    metered = provider(response(content=valid(), prompt=10, completion=10))
    metered.ledger = Ledger()
    gateway = ProposalGateway(metered)
    asyncio.run(gateway.propose(message(), triage(message())))
    assert gateway.ledger is metered.ledger
    assert gateway.ledger.calls == 1


def test_a_wrapper_that_hides_the_provider_does_not_split_the_meter() -> None:
    """The remembered provider sits between the gateway and the model, and holds no ledger."""
    ledger = Ledger()
    inner = provider(response(content=valid(), prompt=10, completion=10))
    inner.ledger = ledger

    class Wrapper:
        name = "remembered"

        def __init__(self, inner) -> None:
            self.inner = inner

        async def complete(self, request: ProposalRequest) -> str:
            return await self.inner.complete(request)

        def __getattr__(self, item):  # exposes the inner provider's ledger when asked for one
            return getattr(self.inner, item)

    asyncio.run(ProposalGateway(Wrapper(inner)).propose(message(), triage(message())))
    assert ledger.calls == 1
    assert ledger.arrivals == 1


def test_the_deflection_rate_counts_arrivals_not_calls() -> None:
    ledger = Ledger()
    ledger.arrival()
    ledger.arrival(deflected=True)
    ledger.arrival(deflected=True)
    assert ledger.deflection_rate == pytest.approx(2 / 3)


def test_the_table_names_the_stage_the_model_and_the_price() -> None:
    ledger = Ledger()
    ledger.record(
        stage="proposal",
        provider="openrouter",
        model="inference-net/schematron-v2-small",
        prompt_tokens=1_000,
        completion_tokens=100,
    )
    ledger.arrival()
    table = ledger.render()
    assert "proposal" in table and "inference-net/schematron-v2-small" in table
    assert "$0.0001" in table, "the priced row shows a figure, not a placeholder"
    assert "deflection rate: 0/1" in table


def test_an_empty_run_reports_zero_rather_than_dividing_by_it() -> None:
    assert Ledger().deflection_rate == 0.0
    assert "over 0 arrival(s)" in Ledger().render()


def test_a_usage_object_that_arrives_as_a_mapping_reads_the_same() -> None:
    """A proxy that hands back plain JSON must price the same as the SDK's own object."""
    ledger = Ledger()
    mapped = SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content=valid()))],
        usage={"prompt_tokens": 7, "completion_tokens": 3},
    )
    metered = OpenAICompatibleProvider(
        ENDPOINTS["openrouter"],
        api_key="test",
        ledger=ledger,
        client=SimpleNamespace(chat=SimpleNamespace(completions=MeteredCompletions(mapped))),
    )
    asyncio.run(metered.complete(ProposalRequest(message=message(), hints=triage(message()))))
    assert (ledger.rows()[0].prompt_tokens, ledger.rows()[0].completion_tokens) == (7, 3)
