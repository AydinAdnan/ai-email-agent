"""Canonical versioned events (Phase 3.1).

SenderIdentity, Attachment, Message, Thread, EmailEvent and FeedbackEvent are the
only shapes the graph, the trace sink and the eval lanes exchange. Email content
lives in Message; no verdict, route or grant is ever carried inside it.

Three things are enforced here instead of being trusted downstream:

- Identity and ordering: ids must be present and unique, and a stream is ordered
  by ``sequence_index``. File order is not a contract.
- Learnability: only explicit user decisions may update the learner, so silence
  and the user's own reply cannot carry ``explicit_for_learning=True``.
- Versioning: every model states the schema version it was written with, so a
  replayed stream can refuse a shape it does not understand.
"""
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from src.agent.safety.floor import Route

EVENT_SCHEMA_VERSION = "1"


class Direction(StrEnum):
    """Which way a message travelled in its thread."""

    INBOUND = "inbound"
    OUTBOUND = "outbound"


class FeedbackKind(StrEnum):
    """What the user did after seeing a decision.

    Values are the dataset's ``observed_user_feedback.kind`` vocabulary verbatim.
    ALWAYS_DO_THIS and NEVER_DO_THIS are scoped policy claims rather than one-off
    decisions; REJECT, REPLY and REVERT come from the build plan and are not yet
    exercised by the sample dataset.
    """

    NONE = "none"
    APPROVE = "approve"
    REJECT = "reject"
    IGNORE_OBSERVED = "ignore_observed"
    EDIT_DRAFT = "edit_draft"
    REPLY = "reply"
    CHANGE_TIER = "change_tier"
    REVERT = "revert"
    ALWAYS_DO_THIS = "always_do_this"
    NEVER_DO_THIS = "never_do_this"


# Approvals, rejections, draft edits, tier corrections, reverts and the scoped
# always/never claims are explicit decisions. Silence ("none", "ignore_observed")
# and the user's own reply are observations, not decisions, and must never move a
# posterior: this is the plan's "silence is not approval" rule in code.
LEARNABLE_FEEDBACK_KINDS = frozenset(
    {
        FeedbackKind.APPROVE,
        FeedbackKind.REJECT,
        FeedbackKind.EDIT_DRAFT,
        FeedbackKind.CHANGE_TIER,
        FeedbackKind.REVERT,
        FeedbackKind.ALWAYS_DO_THIS,
        FeedbackKind.NEVER_DO_THIS,
    }
)


def is_learnable(kind: FeedbackKind) -> bool:
    """Return whether this kind of feedback may update the learner."""
    return kind in LEARNABLE_FEEDBACK_KINDS


class EventValidationError(ValueError):
    """Raised when a canonical event violates the schema."""


class DuplicateEventError(EventValidationError):
    """Raised when a stream carries the same case or message twice."""


class OutOfOrderEventError(EventValidationError):
    """Raised when a stream is not in ascending sequence order."""


def _require_text(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise EventValidationError(f"{field_name} must be a non-empty string")


@dataclass(frozen=True)
class SenderIdentity:
    """Who an email claims to come from, and whether that claim is verified.

    ``verified_identity`` is the difference between an authority claim and an
    authority fact, so it travels with the address rather than with the body.
    """

    email: str
    display_name: str = ""
    verified_identity: bool = False

    def __post_init__(self) -> None:
        _require_text(self.email, "SenderIdentity.email")


@dataclass(frozen=True)
class Attachment:
    """An attachment as metadata, plus its text when the text is extractable.

    Attachment text is untrusted email content: the tripwire scanner reads it
    before any model does.
    """

    filename: str
    content_type: str
    text: str | None = None
    size_bytes: int | None = None
    sha256: str | None = None
    contains_pii: bool | None = None
    contains_financial_data: bool | None = None

    def __post_init__(self) -> None:
        _require_text(self.filename, "Attachment.filename")
        _require_text(self.content_type, "Attachment.content_type")


@dataclass(frozen=True)
class Message:
    """One email message, in a thread, in one direction."""

    message_id: str
    thread_id: str
    sender: SenderIdentity
    recipients: tuple[str, ...] = ()
    direction: Direction = Direction.INBOUND
    parent_message_id: str | None = None
    cc: tuple[str, ...] = ()
    subject: str = ""
    body: str = ""
    quoted_text: str | None = None
    attachments: tuple[Attachment, ...] = ()
    sent_at: datetime | None = None
    schema_version: str = EVENT_SCHEMA_VERSION

    def __post_init__(self) -> None:
        _require_text(self.message_id, "Message.message_id")
        _require_text(self.thread_id, "Message.thread_id")
        if not isinstance(self.sender, SenderIdentity):
            raise EventValidationError("Message.sender must be a SenderIdentity")
        if not all(isinstance(item, Attachment) for item in self.attachments):
            raise EventValidationError("Message.attachments must contain Attachments")


@dataclass(frozen=True)
class Thread:
    """A conversation: the messages that arrived before this case, oldest first."""

    thread_id: str
    messages_before: tuple[Message, ...] = ()
    parent_message_id: str | None = None
    schema_version: str = EVENT_SCHEMA_VERSION

    def __post_init__(self) -> None:
        _require_text(self.thread_id, "Thread.thread_id")
        seen: set[str] = set()
        for message in self.messages_before:
            if not isinstance(message, Message):
                raise EventValidationError("Thread.messages_before must contain Messages")
            if message.message_id in seen:
                raise DuplicateEventError(
                    f"thread {self.thread_id} repeats message {message.message_id}"
                )
            seen.add(message.message_id)
            if message.thread_id != self.thread_id:
                raise EventValidationError(
                    f"message {message.message_id} belongs to thread {message.thread_id}, "
                    f"not {self.thread_id}"
                )


@dataclass(frozen=True)
class EmailEvent:
    """An email arriving for a case: the unit the graph consumes and replays."""

    case_id: str
    sequence_index: int
    message: Message
    thread: Thread
    intent: str
    relationship_class: str
    schema_version: str = EVENT_SCHEMA_VERSION

    def __post_init__(self) -> None:
        _require_text(self.case_id, "EmailEvent.case_id")
        _require_text(self.intent, "EmailEvent.intent")
        _require_text(self.relationship_class, "EmailEvent.relationship_class")
        if self.sequence_index < 1:
            raise EventValidationError("EmailEvent.sequence_index starts at 1")
        if not isinstance(self.message, Message) or not isinstance(self.thread, Thread):
            raise EventValidationError("EmailEvent needs a Message and a Thread")
        if self.message.thread_id != self.thread.thread_id:
            raise EventValidationError(
                f"event {self.case_id} carries message {self.message.message_id} from thread "
                f"{self.message.thread_id} but thread {self.thread.thread_id}"
            )

    @property
    def message_id(self) -> str:
        """The id of the arriving message."""
        return self.message.message_id


@dataclass(frozen=True)
class FeedbackEvent:
    """What the user did with a decision, and whether it may teach the learner."""

    event_id: str
    case_id: str
    kind: FeedbackKind
    explicit_for_learning: bool
    text: str = ""
    edited_draft: str | None = None
    chosen_action_id: str | None = None
    chosen_route: Route | None = None
    recorded_at: datetime | None = None
    schema_version: str = EVENT_SCHEMA_VERSION

    def __post_init__(self) -> None:
        _require_text(self.event_id, "FeedbackEvent.event_id")
        _require_text(self.case_id, "FeedbackEvent.case_id")
        if not isinstance(self.kind, FeedbackKind):
            raise EventValidationError(
                f"FeedbackEvent.kind must be a FeedbackKind, got {type(self.kind).__name__}"
            )
        if self.explicit_for_learning != is_learnable(self.kind):
            raise EventValidationError(
                f"feedback kind '{self.kind.value}' must carry "
                f"explicit_for_learning={is_learnable(self.kind)}; silence, observation "
                "and the user's own reply never update the learner"
            )


def validate_stream(events: Sequence[EmailEvent]) -> None:
    """Reject a stream that repeats a case or message, or drifts out of order.

    Order is ``sequence_index``, never file order: the dataset's file happens to be
    sorted, and one timestamp inversion at the learning/held-out boundary means
    wall-clock time cannot be the ordering contract either.
    """
    seen_cases: set[str] = set()
    seen_messages: set[str] = set()
    previous_index: int | None = None

    for event in events:
        if not isinstance(event, EmailEvent):
            raise EventValidationError("validate_stream expects EmailEvents")
        if event.case_id in seen_cases:
            raise DuplicateEventError(f"case {event.case_id} appears twice in the stream")
        if event.message_id in seen_messages:
            raise DuplicateEventError(f"message {event.message_id} appears twice in the stream")
        seen_cases.add(event.case_id)
        seen_messages.add(event.message_id)

        if previous_index is not None and event.sequence_index <= previous_index:
            raise OutOfOrderEventError(
                f"{event.case_id} has sequence_index {event.sequence_index} after "
                f"{previous_index}"
            )
        previous_index = event.sequence_index


__all__ = [
    "EVENT_SCHEMA_VERSION",
    "LEARNABLE_FEEDBACK_KINDS",
    "Attachment",
    "Direction",
    "DuplicateEventError",
    "EmailEvent",
    "EventValidationError",
    "FeedbackEvent",
    "FeedbackKind",
    "Message",
    "OutOfOrderEventError",
    "SenderIdentity",
    "Thread",
    "is_learnable",
    "validate_stream",
]
