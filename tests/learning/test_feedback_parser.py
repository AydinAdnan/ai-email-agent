"""The constrained feedback parser, the scope echo, and what a claim has to be to exist.

The plan's three fixtures are here: a cron suppression, an all-promotions clarification,
and the ambiguous "everything" that must not become a global rule on its own.
"""
from datetime import UTC, datetime

from agent.learning.feedback import (
    FeedbackContext,
    Reading,
    confirm_claim,
    confirm_words,
    read_feedback,
)
from agent.memory.claims import ClaimScope, ClaimStore, ClaimType, ScopeAnchor
from agent.memory.consent import session_grant
from agent.safety.floor import Route

NOW = datetime(2026, 8, 1, 9, 0, tzinfo=UTC)

CRON = FeedbackContext(
    case_id="WAJO-0052",
    sender="status@acme.example",
    intent="information request",
    relationship_class="self/system notification",
    route=Route.PROCEED_AND_NOTIFY,
    action_id="email.apply_label",
    subject="Nightly cron status: 3 jobs failed",
    message_id="msg-in-wajo-0052",
)
PROMO = FeedbackContext(
    case_id="WAJO-0009",
    sender="promos@shopzilla.example",
    intent="newsletter",
    relationship_class="newsletter/marketing",
    route=Route.PROCEED_SILENTLY,
    action_id="email.apply_label",
    subject="Spring promotions inside",
    message_id="msg-in-wajo-0009",
)


def read(text: str, context: FeedbackContext | None = None) -> Reading:
    return read_feedback(text, context=context, recorded_at=NOW)


def store() -> ClaimStore:
    """A session's store: consent for this purpose, for this session."""
    return ClaimStore(grant=session_grant(purpose="test session"))


def stored(reading: Reading, answer: str, context: FeedbackContext | None = None) -> object:
    """What confirming a reading with this answer would store, or None for nothing."""
    claim = confirm_claim(reading.claim, answer, context=context, recorded_at=NOW)
    return store().store(claim) if claim is not None else None


def test_a_cron_suppression_is_scoped_to_the_mail_it_was_typed_about() -> None:
    reading = read("ignore future cron status emails", CRON)
    claim = reading.claim
    assert claim is not None
    assert claim.type is ClaimType.BOUNDARY
    assert claim.scope.sender == "status@acme.example"
    assert claim.scope.intent == "information request"
    assert claim.scope_anchor is ScopeAnchor.CONTEXT
    assert claim.route is Route.PROCEED_SILENTLY
    assert claim.action_id == "email.archive"
    assert claim.source_case_id == claim.starts_after_case_id == "WAJO-0052"
    assert reading.kind.value == "never_do_this"
    # The echo states the action, the scope and the start point, in plain words, and it
    # is the sentence the plan's worked example prints.
    assert "silently archive future mail from status@acme.example" in reading.echo
    assert "This starts after WAJO-0052, with the next arrival" in reading.echo
    # Nothing is in memory until the user confirms, and then exactly one claim is.
    memory = store()
    assert memory.stored_claims == 0
    assert reading.prompt is not None
    confirmed = confirm_claim(claim, "yes", context=CRON, recorded_at=NOW)
    assert confirmed is not None
    assert memory.store(confirmed).route is Route.PROCEED_SILENTLY
    assert memory.stored_claims == 1
    # The claim carries its own evidence, not just the words.
    assert confirmed.quote == "ignore future cron status emails"
    assert confirmed.source_message_id == "msg-in-wajo-0052"
    assert confirmed.recorded_at == NOW


def test_an_explicit_address_is_the_scope_it_names() -> None:
    reading = read("always archive mail from status@acme.example", CRON)
    assert reading.claim is not None
    assert reading.claim.scope == ClaimScope(sender="status@acme.example")
    assert reading.claim.scope_anchor is ScopeAnchor.EXPLICIT
    assert reading.claim.action_id == "email.archive"
    assert reading.claim.confidence == 1.0


def test_a_promotions_clarification_resolves_through_the_classifier_vocabulary() -> None:
    """A person saying "promotions" names a class, and the class words are the ones the
    classifier already reads rather than a second list kept in step by hand."""
    reading = read("always archive promotions", PROMO)
    claim = reading.claim
    assert claim is not None
    assert claim.scope == ClaimScope(intent="newsletter")
    assert claim.scope_anchor is ScopeAnchor.INTENT
    assert claim.type is ClaimType.PREFERENCE
    # Archiving is the work; nothing in the line said whether to announce it, so the
    # claim does not pretend to know and the echo does not either.
    assert claim.route is None and claim.action_id == "email.archive"
    assert "archive future newsletter mail" in reading.echo


def test_an_ambiguous_everything_is_offered_narrow_and_asked_about() -> None:
    """"everything" is ambiguous, so the narrow reading tied to the active item is a
    guess that has to be confirmed rather than a global rule stored quietly."""
    reading = read("ignore everything from now", CRON)
    claim = reading.claim
    assert claim is not None
    assert claim.scope_anchor is ScopeAnchor.CONTEXT
    assert claim.confidence < 0.8
    assert reading.prompt is not None and "every future arrival" in reading.prompt

    memory = store()
    assert memory.stored_claims == 0
    confirmed = confirm_claim(claim, "yes", context=CRON, recorded_at=NOW)
    assert confirmed is not None
    memory.store(confirmed)
    assert memory.stored_claims == 1


def test_the_whole_inbox_is_never_the_default_reading() -> None:
    """The one reading the parser will not assume is the one it stores only when said."""
    with_context = read("ignore everything from now", CRON)
    widened = confirm_claim(with_context.claim, "the whole inbox", context=CRON, recorded_at=NOW)
    assert widened is not None
    assert widened.scope_anchor is ScopeAnchor.GLOBAL
    assert widened.scope == ClaimScope()
    assert "every future arrival" in widened.describe()


def test_a_line_that_names_no_scope_is_offered_narrow_and_asked_about() -> None:
    """An action with no scope word at all falls back to the mail in front of the user, at
    the confidence that makes the echo ask - it is not a reason for the run to stop."""
    reading = read("stop notifying me", CRON)
    claim = reading.claim
    assert claim is not None
    assert claim.scope == ClaimScope(sender="status@acme.example", intent="information request")
    assert claim.scope_anchor is ScopeAnchor.CONTEXT
    assert claim.confidence < 0.8
    assert "every future arrival" in (reading.prompt or "")
    assert stored(reading, "yes", CRON) is not None


def test_a_line_with_no_mail_in_front_of_it_is_heard_and_not_kept() -> None:
    """A claim has to name the mail it came from, so a rule stated with nothing in front
    of the user is not remembered rather than guessed into a global one."""
    reading = read("ignore everything from now")
    assert reading.claim is None
    assert reading.kind.value == "none"
    assert "needs the mail it came from" in reading.echo
    assert stored(reading, "yes") is None


def test_the_answer_can_name_the_scope_the_question_asked_for() -> None:
    reading = read("ignore everything from now", CRON)
    narrowed = confirm_claim(reading.claim, "only from status@acme.example", context=CRON, recorded_at=NOW)
    assert narrowed is not None
    assert narrowed.scope.sender == "status@acme.example"
    assert narrowed.scope_anchor is ScopeAnchor.EXPLICIT
    assert narrowed.route is Route.PROCEED_SILENTLY


def test_a_plain_yes_or_no_is_a_decision_and_not_a_rule() -> None:
    yes = read("yes, send it", CRON)
    assert yes.kind.value == "approve"
    assert yes.claim is None and yes.prompt is None and yes.stores is False
    assert yes.explicit_for_learning is True
    no = read("no, don't do that", CRON)
    assert no.kind.value == "reject"
    assert no.claim is None


def test_a_sender_correction_is_read_as_a_correction() -> None:
    reading = read("actually david is a spoof, always escalate mail from david@techcorp.example", CRON)
    assert reading.claim is not None
    assert reading.claim.type is ClaimType.CORRECTION
    assert reading.claim.route is Route.ESCALATE
    assert reading.claim.scope.sender == "david@techcorp.example"
    assert reading.kind.value == "change_tier"


def test_a_request_for_an_action_no_tool_holds_is_refused_not_stored() -> None:
    """The parser extracts candidates and cannot invent capability."""
    reading = read("always delete everything from status@acme.example", CRON)
    assert reading.claim is None
    assert reading.kind.value == "none"
    assert "not an action I hold" in reading.echo


def test_an_unreadable_line_stores_nothing_and_says_so() -> None:
    reading = read("hmm", CRON)
    assert reading.claim is None and reading.kind.value == "none"
    assert "nothing was stored" in reading.echo


def test_the_same_claim_twice_is_stored_once() -> None:
    first = read("always archive mail from status@acme.example", CRON)
    same = read("always archive mail from status@acme.example", CRON)
    assert first.claim is not None and same.claim is not None
    assert first.claim.claim_id == same.claim.claim_id
    memory = store()
    memory.store(first.claim)
    memory.store(same.claim)
    assert memory.stored_claims == 1


def test_confirm_words_reads_the_two_answers_a_prompt_needs() -> None:
    assert confirm_words("yes") is True
    assert confirm_words("no thanks") is False
    assert confirm_words("maybe later") is None
    assert confirm_words("") is None
