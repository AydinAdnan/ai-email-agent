from dataclasses import replace
from datetime import UTC, datetime

import pytest

from agent.memory.claims import (
    SENSITIVE_ATTRIBUTES,
    Claim,
    ClaimError,
    ClaimScope,
    ClaimStore,
    ClaimType,
    ScopeAnchor,
)
from agent.memory.consent import Capability, Grant, session_grant
from agent.safety.floor import Route

NOW = datetime(2026, 8, 1, 9, 0, tzinfo=UTC)


def preference(**overrides) -> Claim:
    """One claim as the parser hands it over: a class of mail, and the words that said so."""
    base = Claim(
        claim_id="clm-3ddb5fd5e1fd",
        type=ClaimType.PREFERENCE,
        quote="always archive promotions",
        source_message_id="msg-in-wajo-0009",
        source_case_id="WAJO-0009",
        recorded_at=NOW,
        scope=ClaimScope(intent="newsletter"),
        scope_anchor=ScopeAnchor.INTENT,
        confidence=0.9,
        action_id="email.archive",
        starts_after_case_id="WAJO-0009",
    )
    return replace(base, **overrides)


def memory() -> ClaimStore:
    return ClaimStore(grant=session_grant(purpose="test session"))


def test_rules_survive_a_restart(tmp_path):
    """A rule kept in one run is in force in the next one, which is a separate process."""
    path = tmp_path / "prefs.jsonl"
    first = ClaimStore(grant=session_grant(purpose="test session"), path=path)
    rule = replace(preference(), route=Route.PROCEED_SILENTLY, params={"label": "Promotions"})
    replaced = replace(rule, claim_id="clm-replaced", superseded_by=rule.claim_id)
    first.store(rule)
    first.store(replaced)
    assert first.save() == 2

    reopened = ClaimStore(grant=session_grant(purpose="next session"), path=path)
    assert reopened.loaded == 2
    assert reopened.claims == (rule, replaced)
    # The replaced one is history, not something in force.
    assert reopened.matching(intent="newsletter") == (rule,)


def test_a_store_without_consent_neither_reads_nor_writes(tmp_path):
    """Consent is what makes a rule usable, not the file being there."""
    path = tmp_path / "prefs.jsonl"
    path.write_text("{\n}", encoding="utf-8")
    store = ClaimStore(grant=Grant(capability=Capability.LEARN), path=path)

    assert store.loaded == 0
    assert store.save() == 0
    assert "no consent" in store.refusal
    assert path.read_text(encoding="utf-8") == "{\n}"


def test_a_corrupted_rule_file_fails_loudly(tmp_path):
    path = tmp_path / "prefs.jsonl"
    path.write_text('{"claim_id": "clm-1"}\n', encoding="utf-8")
    with pytest.raises(ClaimError, match="not readable"):
        ClaimStore(grant=session_grant(purpose="test session"), path=path)


def test_a_preference_round_trips_with_its_source():
    """The plan's check after 4.2: a preference comes back with where it came from."""
    store = memory()
    stored = store.store(preference())
    assert store.claims == (stored,)
    assert stored.quote == "always archive promotions"
    assert stored.source_message_id == "msg-in-wajo-0009"
    assert stored.source_case_id == "WAJO-0009"
    assert stored.recorded_at == NOW
    assert stored.scope == ClaimScope(intent="newsletter")
    assert stored.confidence == 0.9
    assert stored.describe() == (
        "archive future newsletter mail. This starts after WAJO-0009, with the next arrival."
    )


def test_every_type_the_plan_names_is_allowed_and_nothing_else():
    assert {kind.value for kind in ClaimType} == {
        "fact",
        "event",
        "preference",
        "boundary",
        "correction",
    }
    with pytest.raises(ValueError):
        ClaimType("opinion")


@pytest.mark.parametrize(
    ("field", "value", "expected"),
    [
        ("quote", "   ", "quote"),
        ("source_message_id", "", "source_message_id"),
        ("source_case_id", "", "source_case_id"),
        ("confidence", 0.0, "confidence"),
        ("confidence", 1.5, "confidence"),
    ],
)
def test_an_underspecified_claim_does_not_exist(field: str, value: object, expected: str):
    with pytest.raises(ClaimError, match=expected):
        preference(**{field: value})


def test_a_claim_with_no_timestamp_cannot_be_audited():
    with pytest.raises(ClaimError, match="timestamp"):
        preference(recorded_at=None)


def test_an_unresolved_scope_is_refused_until_the_mail_is_settled():
    with pytest.raises(ClaimError, match="unresolved"):
        preference(scope=ClaimScope(), scope_anchor=ScopeAnchor.CONTEXT)
    # The whole inbox is not unresolved: it was said out loud, which is why it is allowed.
    widened = preference(scope=ClaimScope(), scope_anchor=ScopeAnchor.GLOBAL)
    assert widened.scope.resolved is False


@pytest.mark.parametrize(
    "quote",
    [
        "never notify me about the church newsletter",
        "stop showing me political fundraising",
        "he is diabetic, so flag his medication refills",
        "ignore the lgbtq pride mail",
        "she is pregnant, mute the parenting list",
        "leave the ethnic community updates alone",
    ],
)
def test_a_claim_about_a_protected_attribute_is_never_stored(quote: str):
    with pytest.raises(ClaimError, match="protected attribute"):
        preference(quote=quote)


def test_ordinary_mail_words_are_not_mistaken_for_protected_ones():
    for quote in (
        "always archive promotions",
        "never notify me about receipts",
        "escalate anything asking for a wire transfer",
        "ignore status emails from acme.example",
    ):
        assert SENSITIVE_ATTRIBUTES.search(quote) is None
        assert preference(quote=quote).quote == quote


def test_the_scope_has_no_axis_for_who_the_user_is():
    """Protected attributes are out of memory by construction, not by a filter: the only
    axes a claim can be scoped to are about mail."""
    assert set(ClaimScope.__annotations__) == {"sender", "domain", "intent"}


def test_retrieval_returns_the_claims_that_bear_on_one_mail():
    store = memory()
    sender_bound = store.store(preference(quote="ignore status emails", scope=ClaimScope(sender="status@acme.example"), scope_anchor=ScopeAnchor.EXPLICIT))
    class_bound = store.store(preference(quote="always archive promotions", scope=ClaimScope(intent="newsletter"), scope_anchor=ScopeAnchor.INTENT))
    global_bound = store.store(preference(quote="ignore everything from now", scope=ClaimScope(), scope_anchor=ScopeAnchor.GLOBAL, confidence=1.0))

    for_one_mail = store.matching(
        sender="status@acme.example", domain="acme.example", intent="information request"
    )
    assert {claim.claim_id for claim in for_one_mail} == {
        sender_bound.claim_id,
        global_bound.claim_id,
    }
    elsewhere = store.matching(
        sender="promos@shopzilla.example", domain="shopzilla.example", intent="newsletter"
    )
    assert {claim.claim_id for claim in elsewhere} == {
        class_bound.claim_id,
        global_bound.claim_id,
    }


def test_a_superseded_claim_is_not_retrieved():
    store = memory()
    old = store.store(preference(quote="always archive promotions"))
    new = store.store(preference(quote="always label promotions", claim_id="clm-new"))
    assert old.active and new.active
    store.store(replace(old, superseded_by=new.claim_id))
    assert {claim.claim_id for claim in store.matching(intent="newsletter")} == {new.claim_id}


def test_a_claim_can_carry_the_work_it_asks_for():
    claim = preference(route=Route.PROCEED_SILENTLY, action_id="email.archive")
    assert claim.route is Route.PROCEED_SILENTLY
    assert claim.describe().startswith("silently archive")
