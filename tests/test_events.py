"""Unit tests for the canonical events (Phase 3.1).

Covers:
- Identity and versioning guarantees on every model
- Duplicate-id and out-of-order stream fixtures rejected
- Every feedback kind round-trips with explicit_for_learning intact
- "Silence is not approval" enforced on the learner flag
- The models actually fit the dataset's rows
"""
import json
from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

from agent.dataset import event_from_row
from agent.events import (
    EVENT_SCHEMA_VERSION,
    LEARNABLE_FEEDBACK_KINDS,
    Attachment,
    Direction,
    DuplicateEventError,
    EmailEvent,
    EventValidationError,
    FeedbackEvent,
    FeedbackKind,
    Message,
    OutOfOrderEventError,
    SenderIdentity,
    Thread,
    is_learnable,
    validate_stream,
)
from agent.safety.floor import Route

DATASET_PATH = Path(__file__).parent.parent / "docs" / "wajo_dataset.jsonl"


def _load_dataset() -> list[dict]:
    assert DATASET_PATH.exists(), f"dataset missing at {DATASET_PATH}"
    with open(DATASET_PATH, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def _event(case_id: str, sequence_index: int, message_id: str, thread_id: str = "th-1") -> EmailEvent:
    return EmailEvent(
        case_id=case_id,
        sequence_index=sequence_index,
        message=Message(
            message_id=message_id,
            thread_id=thread_id,
            sender=SenderIdentity(email="news@engweekly.synthetic.example"),
        ),
        thread=Thread(thread_id=thread_id),
    )


def _feedback(kind: FeedbackKind, explicit: bool | None = None, event_id: str = "fb-1") -> FeedbackEvent:
    return FeedbackEvent(
        event_id=event_id,
        case_id="WAJO-0001",
        kind=kind,
        explicit_for_learning=is_learnable(kind) if explicit is None else explicit,
    )


# ============================================================================
# 1. Identity and versioning
# ============================================================================

def test_models_are_frozen():
    """A canonical event cannot be mutated after it is built."""
    event = _event("WAJO-0001", 1, "msg-in-1")
    with pytest.raises(FrozenInstanceError):
        event.case_id = "WAJO-9999"  # type: ignore[misc]


@pytest.mark.parametrize(
    "build",
    [
        lambda: SenderIdentity(email="  "),
        lambda: Attachment(filename="", content_type="text/plain"),
        lambda: Message(message_id="", thread_id="th-1", sender=SenderIdentity(email="a@b.test")),
        lambda: Message(message_id="m-1", thread_id="", sender=SenderIdentity(email="a@b.test")),
        lambda: Thread(thread_id=""),
        lambda: EmailEvent(
            case_id="",
            sequence_index=1,
            message=Message("m-1", "th-1", SenderIdentity(email="a@b.test")),
            thread=Thread("th-1"),
        ),
        lambda: EmailEvent(
            case_id="WAJO-0001",
            sequence_index=0,
            message=Message("m-1", "th-1", SenderIdentity(email="a@b.test")),
            thread=Thread("th-1"),
        ),
        lambda: Message(
            message_id="m-1",
            thread_id="th-1",
            sender={"email": "a@b.test"},  # type: ignore[arg-type]
        ),
        lambda: Message(
            message_id="m-1",
            thread_id="th-1",
            sender=SenderIdentity(email="a@b.test"),
            attachments=("not-an-attachment",),  # type: ignore[arg-type]
        ),
    ],
)
def test_missing_identity_is_rejected(build):
    """Empty ids and malformed fields fail at construction, not at use."""
    with pytest.raises(EventValidationError):
        build()


def test_every_model_carries_the_schema_version():
    """A replayed stream can refuse a shape it does not understand."""
    event = _event("WAJO-0001", 1, "msg-in-1")
    assert EVENT_SCHEMA_VERSION == "1"
    assert event.schema_version == EVENT_SCHEMA_VERSION
    assert event.message.schema_version == EVENT_SCHEMA_VERSION
    assert event.thread.schema_version == EVENT_SCHEMA_VERSION
    assert _feedback(FeedbackKind.APPROVE).schema_version == EVENT_SCHEMA_VERSION


# ============================================================================
# 2. Thread invariants
# ============================================================================

def test_thread_rejects_a_message_from_another_thread():
    """History cannot smuggle a message that belongs to a different thread."""
    foreign = Message(
        message_id="msg-hist-9",
        thread_id="th-other",
        sender=SenderIdentity(email="news@engweekly.synthetic.example"),
    )
    with pytest.raises(EventValidationError):
        Thread(thread_id="th-1", messages_before=(foreign,))


def test_thread_rejects_duplicate_message_ids():
    """History ids are unique, even though the dataset reuses them across cases."""
    message = Message(
        message_id="msg-hist-1",
        thread_id="th-1",
        sender=SenderIdentity(email="news@engweekly.synthetic.example"),
    )
    with pytest.raises(DuplicateEventError):
        Thread(thread_id="th-1", messages_before=(message, message))


def test_event_rejects_a_message_that_does_not_belong_to_its_thread():
    """The arriving message and the thread it is attached to must agree."""
    with pytest.raises(EventValidationError):
        EmailEvent(
            case_id="WAJO-0001",
            sequence_index=1,
            message=Message(
                message_id="msg-in-1",
                thread_id="th-other",
                sender=SenderIdentity(email="news@engweekly.synthetic.example"),
            ),
            thread=Thread(thread_id="th-1"),
        )


def test_an_event_carries_no_classification():
    """The dataset's answers live on the Case, so a decision path cannot read them."""
    event = _event("WAJO-0001", 1, "m-1")
    for leaked in ("intent", "relationship_class", "gold", "autonomy_outcome"):
        assert not hasattr(event, leaked), f"EmailEvent must not carry {leaked}"


# ============================================================================
# 3. Stream order and duplicate rejection
# ============================================================================

def test_ordered_stream_is_accepted():
    """A unique, ascending stream passes."""
    validate_stream([_event("WAJO-0001", 1, "m-1"), _event("WAJO-0002", 2, "m-2")])


def test_duplicate_case_id_is_rejected():
    """The same case arriving twice would double-count in the report denominators."""
    with pytest.raises(DuplicateEventError):
        validate_stream([_event("WAJO-0001", 1, "m-1"), _event("WAJO-0001", 2, "m-2")])


def test_duplicate_message_id_is_rejected():
    """The same message arriving twice is a replay, not a new arrival."""
    with pytest.raises(DuplicateEventError):
        validate_stream([_event("WAJO-0001", 1, "m-1"), _event("WAJO-0002", 2, "m-1")])


def test_out_of_order_stream_is_rejected():
    """Sequence order is the contract; file order and wall-clock time are not."""
    with pytest.raises(OutOfOrderEventError):
        validate_stream([_event("WAJO-0002", 2, "m-2"), _event("WAJO-0001", 1, "m-1")])


def test_repeated_sequence_index_is_rejected():
    """Equal sequence indices are ambiguous, so they are refused as well."""
    with pytest.raises(OutOfOrderEventError):
        validate_stream([_event("WAJO-0001", 1, "m-1"), _event("WAJO-0002", 1, "m-2")])


# ============================================================================
# 4. Feedback kinds and the learner flag
# ============================================================================

@pytest.mark.parametrize("kind", list(FeedbackKind))
def test_every_feedback_kind_round_trips_with_its_flag(kind):
    """Each kind survives construction with explicit_for_learning intact."""
    event = _feedback(kind)
    assert event.kind is kind
    assert event.explicit_for_learning == is_learnable(kind)


@pytest.mark.parametrize(
    "kind",
    [FeedbackKind.NONE, FeedbackKind.IGNORE_OBSERVED, FeedbackKind.REPLY],
)
def test_silence_and_observation_cannot_teach(kind):
    """"Silence is not approval": a non-decision claiming the learning flag fails."""
    with pytest.raises(EventValidationError):
        _feedback(kind, explicit=True)


@pytest.mark.parametrize(
    "kind",
    [
        FeedbackKind.APPROVE,
        FeedbackKind.REJECT,
        FeedbackKind.EDIT_DRAFT,
        FeedbackKind.CHANGE_TIER,
        FeedbackKind.REVERT,
        FeedbackKind.ALWAYS_DO_THIS,
        FeedbackKind.NEVER_DO_THIS,
    ],
)
def test_explicit_decisions_must_be_flagged_learnable(kind):
    """An explicit decision that disclaims learning is a bug, not a preference."""
    assert kind in LEARNABLE_FEEDBACK_KINDS
    with pytest.raises(EventValidationError):
        _feedback(kind, explicit=False)


def test_feedback_rejects_a_raw_string_kind():
    """The enum is the vocabulary; a loose string is refused rather than coerced."""
    with pytest.raises(EventValidationError):
        FeedbackEvent(
            event_id="fb-1",
            case_id="WAJO-0001",
            kind="approve",  # type: ignore[arg-type]
            explicit_for_learning=True,
        )


# ============================================================================
# 5. Grounding in the dataset
# ============================================================================

def test_dataset_feedback_vocabulary_and_flags_are_representable():
    """Every kind in the dataset parses, and its learner flag matches the rule.

    This is the check that Commit 3.1's contract fits real data: 49 explicit
    decisions are learnable, and the 91 silences/observations are not.
    """
    rows = _load_dataset()
    assert rows, "dataset is empty"

    learnable = 0
    for row in rows:
        raw = row["observed_user_feedback"]
        event = FeedbackEvent(
            event_id=f"{row['case_id']}:feedback",
            case_id=row["case_id"],
            kind=FeedbackKind(raw["kind"]),
            explicit_for_learning=raw["explicit_for_learning"],
            text=raw["feedback_text"] or "",
            edited_draft=raw["edited_draft"],
            chosen_action_id=raw["chosen_action_id"],
            chosen_route=Route(raw["chosen_autonomy_outcome"]),
        )
        learnable += event.explicit_for_learning

    assert learnable == 49
    non_learnable = {
        row["observed_user_feedback"]["kind"]
        for row in rows
        if not row["observed_user_feedback"]["explicit_for_learning"]
    }
    assert non_learnable == {"none", "ignore_observed"}


def test_dataset_rows_convert_to_canonical_events():
    """Real rows (history, attachments, sender identity) fit the models as written."""
    rows = _load_dataset()
    events = [event_from_row(row) for row in rows]

    validate_stream(events)
    assert len(events) == len(rows)

    with_history = [e for e in events if e.thread.messages_before]
    assert with_history, "dataset rows are expected to carry prior thread messages"
    assert all(m.thread_id == e.thread.thread_id for e in with_history for m in e.thread.messages_before)

    with_attachments = [e for e in events if e.message.attachments]
    assert with_attachments, "dataset rows are expected to carry attachments"
    assert any(a.text for e in with_attachments for a in e.message.attachments), (
        "attachment text must be reachable: the tripwire scanner reads it"
    )

    assert all(e.message.sender.verified_identity in (True, False) for e in events)
    assert {e.message.direction for e in events} == {Direction.INBOUND}


def test_dataset_stream_survives_the_ordering_contract():
    """The dataset is in file order already, and its indices are unique and ascending."""
    events = [event_from_row(row) for row in _load_dataset()]
    validate_stream(events)  # raises OutOfOrderEventError / DuplicateEventError otherwise

    reversed_stream = list(reversed(events))
    with pytest.raises(OutOfOrderEventError):
        validate_stream(reversed_stream)
