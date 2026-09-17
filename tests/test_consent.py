import asyncio
import io
from collections.abc import Sequence
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from agent.dataset import Lane, Manifest
from agent.memory.claims import Claim, ClaimScope, ClaimStore, ClaimType, ScopeAnchor
from agent.memory.consent import (
    Capability,
    ConsentRequired,
    Grant,
    LearningConsent,
    Retention,
    session_grant,
)
from agent.sim.runner import close_input, run_simulation

FIXTURE = Path(__file__).parent / "fixtures" / "stream_12.jsonl"
NOW = datetime(2026, 8, 1, 9, 0, tzinfo=UTC)


def view() -> object:
    return Manifest.load(FIXTURE).view(Lane.CALIBRATION)


def claim(recorded_at: datetime = NOW) -> Claim:
    return Claim(
        claim_id="clm-000000000001",
        type=ClaimType.BOUNDARY,
        quote="ignore future cron emails from status@acme.example",
        source_message_id="msg-in-wajo-0052",
        source_case_id="WAJO-0052",
        recorded_at=recorded_at,
        scope=ClaimScope(sender="status@acme.example"),
        scope_anchor=ScopeAnchor.EXPLICIT,
        confidence=0.9,
    )


def test_a_capability_is_not_consent():
    grant = Grant(capability=Capability.LEARN)
    assert grant.may_learn(at=NOW) is False
    assert "no consent" in grant.why_not(at=NOW)


def test_capability_without_consent_stores_zero_claims():
    memory = ClaimStore(grant=Grant(capability=Capability.LEARN))
    with pytest.raises(ConsentRequired, match="no consent"):
        memory.store(claim())
    assert memory.stored_claims == 0


def test_consent_without_the_learning_capability_stores_nothing():
    grant = Grant(
        capability=Capability.READ,
        consent=LearningConsent(purpose="calibration", retention=Retention.SESSION),
    )
    memory = ClaimStore(grant=grant)
    assert memory.may_learn(at=NOW) is False
    with pytest.raises(ConsentRequired, match="not learning"):
        memory.store(claim())
    assert memory.stored_claims == 0


def test_expired_consent_stores_nothing():
    grant = Grant(
        capability=Capability.LEARN,
        consent=LearningConsent(
            purpose="calibration",
            retention=Retention.THIRTY_DAYS,
            expiry=NOW - timedelta(days=1),
        ),
    )
    memory = ClaimStore(grant=grant)
    with pytest.raises(ConsentRequired, match="expired"):
        memory.store(claim())
    assert memory.stored_claims == 0


def test_consent_has_to_name_a_purpose_and_who_granted_it():
    with pytest.raises(ValueError, match="purpose"):
        LearningConsent(purpose="   ", retention=Retention.SESSION)
    with pytest.raises(ValueError, match="who granted"):
        LearningConsent(purpose="calibration", retention=Retention.SESSION, granted_by="")


def test_a_store_is_closed_by_default():
    """Nobody gets learning by forgetting to ask for it."""
    assert ClaimStore().may_learn(at=NOW) is False
    with pytest.raises(ConsentRequired):
        ClaimStore().store(claim())


def test_a_session_grant_keeps_a_confirmed_claim():
    memory = ClaimStore(grant=session_grant(purpose="calibration session"))
    stored = memory.store(claim())
    assert stored.claim_id == "clm-000000000001"
    assert memory.stored_claims == 1


def test_a_run_with_capability_and_no_consent_stores_zero_claims():
    """The plan's check after 4.1, on a real chat run.

    The same lines are heard and confirmed; the session holds the learning capability and
    no consent for it, so the transcript says so and memory stays empty.
    """
    outcome, transcript = asyncio.run(
        run_session(
            ClaimStore(grant=Grant(capability=Capability.LEARN)),
            ["ignore future cron emails from status@acme.example", "yes"],
        )
    )
    assert "reply for WAJO-0026: 'ignore future cron emails from status@acme.example'" in transcript
    # The line was understood and echoed, and then not kept: consent is what is missing.
    assert "Storing that as a rule - is it right?" in transcript
    assert "not stored: nothing was stored: no consent to learn was given" in transcript
    assert outcome.claims == []
    assert outcome.replies == 1


def test_a_run_with_a_session_grant_keeps_the_rule():
    grant = session_grant(purpose="calibration session")
    outcome, transcript = asyncio.run(
        run_session(
            ClaimStore(grant=grant),
            ["ignore future cron emails from status@acme.example", "yes"],
        )
    )
    assert "stored clm-" in transcript
    assert len(outcome.claims) == 1
    stored = outcome.claims[0]
    assert stored.source_message_id == "msg-in-wajo-0026"
    assert stored.quote == "ignore future cron emails from status@acme.example"


async def run_session(store: ClaimStore, lines: Sequence[str]):
    """Replay the fixture, typing ``lines`` at the first decision that waits."""
    queue: asyncio.Queue = asyncio.Queue()
    seen = 0

    async def hook(index: int, decision) -> None:
        nonlocal seen
        seen += 1
        if seen > 1:
            await close_input(queue)
            return
        for line in lines:
            queue.put_nowait(line)
        await close_input(queue)

    out = io.StringIO()
    outcome = await run_simulation(
        view(),
        seed=7,
        out=out,
        input_queue=queue,
        on_interrupt=hook,
        store=store,
    )
    return outcome, out.getvalue()
