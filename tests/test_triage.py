"""Deterministic pre-triage: mail-only, deterministic, and measured against the labels."""
import pytest

from agent.dataset import DEFAULT_DATASET_PATH, Manifest
from agent.events import Direction, Message, SenderIdentity
from agent.triage import (
    INTENTS,
    RECEIPT_SILENT_THRESHOLD,
    RELATIONSHIP_CLASSES,
    amount_in,
    triage,
)

# The dataset is the only place with ground truth, so the agreement floors are read
# from it. They are floors, not targets: they exist so a rule change that makes the
# classifier worse has to say so out loud.
MIN_INTENT_AGREEMENT = 0.62
MIN_RELATIONSHIP_AGREEMENT = 0.70


def message(
    sender: str,
    *,
    display: str = "",
    verified: bool = True,
    subject: str = "",
    body: str = "",
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


@pytest.fixture(scope="module")
def manifest() -> Manifest:
    return Manifest.load(DEFAULT_DATASET_PATH)


@pytest.fixture(scope="module")
def guesses(manifest: Manifest):
    return [(case, triage(case.event.message)) for case in manifest.cases]


def test_every_guess_uses_the_dataset_vocabulary(guesses) -> None:
    for _case, guess in guesses:
        assert guess.intent in INTENTS
        assert guess.relationship_class in RELATIONSHIP_CLASSES
        assert guess.signals, "a guess with no signals explains nothing"


def test_intent_agreement_holds(guesses) -> None:
    hits = sum(guess.intent == case.labels.intent for case, guess in guesses)
    assert hits / len(guesses) >= MIN_INTENT_AGREEMENT, f"{hits}/{len(guesses)}"


def test_relationship_agreement_holds(guesses) -> None:
    hits = sum(guess.relationship_class == case.labels.relationship_class for case, guess in guesses)
    assert hits / len(guesses) >= MIN_RELATIONSHIP_AGREEMENT, f"{hits}/{len(guesses)}"


def test_nothing_about_the_labels_reaches_the_classifier(guesses) -> None:
    """The classifier's input is a Message, so a label cannot be an input.

    Feeding it a message whose case is labelled one way and reading the guess is the
    only way to show that: the guess depends on the mail, and the same mail in another
    case would guess the same.
    """
    by_mail: dict[tuple[str, str, str], set[str]] = {}
    for case, guess in guesses:
        message = case.event.message
        by_mail.setdefault(
            (message.sender.email, message.subject, message.body), set()
        ).add(guess.intent)
    assert all(len(intents) == 1 for intents in by_mail.values())


def test_an_unverified_sender_never_reads_as_a_known_relationship() -> None:
    guess = triage(message("billing@unknown.example", verified=False, subject="Your invoice"))
    assert guess.relationship_class == "unknown"


def test_an_unverified_authority_claim_is_spoofing() -> None:
    guess = triage(
        message(
            "reset@external-desk.example",
            display="IT Support",
            verified=False,
            subject="Reset your password",
        )
    )
    assert guess.relationship_class == "spoofed/unverified"
    assert guess.confidence > 0.9


def test_an_unverified_stranger_asking_for_access_is_spoofing() -> None:
    guess = triage(
        message("kevin@contractor.example", verified=False, subject="Grant admin access to production")
    )
    assert guess.relationship_class == "spoofed/unverified"


def test_a_known_sender_wins_over_every_marker() -> None:
    guess = triage(
        message("billing@cloud.example", display="Cloud", subject="Amazon Web Services Invoice"),
        known_senders={"billing@cloud.example": "friend"},
    )
    assert guess.relationship_class == "friend"
    assert guess.confidence == 1.0


def test_internal_mail_reads_as_a_colleague() -> None:
    guess = triage(message("elena@techcorp.synthetic.example", subject="Quick catchup this week?"))
    assert guess.relationship_class == "colleague"
    assert guess.intent == "scheduling"


def test_a_cloud_invoice_is_not_read_as_a_payment_request() -> None:
    """An AWS invoice says a payment is due; it is still a bill, not a wire request."""
    guess = triage(
        message(
            "no-reply@billing.aws.synthetic.example",
            subject="Amazon Web Services Invoice #INV-1 Available",
            body="Your invoice is available. Payment due date: August 20, 2026.",
        )
    )
    assert guess.intent == "cloud/AWS bill"


def test_bulk_promo_mail_without_a_marker_is_still_bulk() -> None:
    guess = triage(
        message("growth@saas.example", subject="Exclusive 50% discount on B2B analytics webinar")
    )
    assert guess.intent == "newsletter"
    assert guess.relationship_class == "newsletter/marketing"


def test_a_build_result_is_bulk_mail_not_a_question() -> None:
    """A machine notice asks the reader nothing, so it is filed rather than answered.

    Reading the fallback as an information request made a green build and a pull request
    opening arrive as questions, which earns a drafted reply no reader can answer.
    """
    guess = triage(
        message(
            "builds@circleci.example",
            subject="[Success] Build #1204 on feature/caching",
            body="All 312 tests passed in 4m12s. Nothing to review.",
        )
    )
    assert guess.intent == "newsletter"
    assert guess.relationship_class == "newsletter/marketing"


def test_a_machine_notice_that_reports_a_fault_stays_a_notification() -> None:
    """The other half of the same rule: a fault is something the reader has to know."""
    guess = triage(
        message(
            "alerts@sentry.example",
            subject="[Fatal] Unhandled OutOfMemoryError in worker queue",
            body="Events: 37 in the last hour. The worker restarted twice.",
        )
    )
    assert guess.intent == "security alert"
    assert guess.relationship_class == "self/system notification"


def test_money_is_read_from_the_mail() -> None:
    assert amount_in("Your receipt from Corner Cafe ($14.50)") == 14.5
    assert amount_in("Total: $1,204.00") == 1204.0
    assert amount_in("no amounts here") is None
    assert RECEIPT_SILENT_THRESHOLD == 50.0


def test_an_ambiguous_message_asks_for_a_model() -> None:
    guess = triage(message("someone@somewhere.example", subject="Hello"))
    assert guess.needs_model is True
    assert guess.confidence < 0.9
