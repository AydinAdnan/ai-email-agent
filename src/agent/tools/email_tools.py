"""The simulated email tools (Phase 3.3).

Six tools over one in-memory mailbox: read, label, archive, draft, notify, and a
receipt-only send. The send is the interesting one - it validates exactly like a real
send, records the intent on the receipt, and puts nothing on the wire, which is what
lets the whole pipeline be exercised without an email account.

The mailbox is the only state that commits touch. Nothing here knows about the
dataset, a case id or a label: a tool takes an address, a message id and words, which
is all a real adapter would get too.
"""
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any, ClassVar

from agent.tools.registry import Effect, Tool, ToolError, ToolRegistry


@dataclass
class Notification:
    """A message to the user's own assistant, never to anyone else."""

    text: str
    email_id: str = ""
    case_id: str = ""


@dataclass
class Draft:
    """A private draft. Preparation, not sending."""

    email_id: str
    body: str
    to: tuple[str, ...] = ()


@dataclass
class SimulatedMailbox:
    """Everything a commit can change, and nothing a prepare can."""

    labels: dict[str, list[str]] = field(default_factory=dict)
    archived: list[str] = field(default_factory=list)
    drafts: dict[str, Draft] = field(default_factory=dict)
    notifications: list[Notification] = field(default_factory=list)
    # The send tool never appends here. It exists so a test can assert zero sends
    # rather than infer it from the absence of a method.
    sends: list[dict[str, Any]] = field(default_factory=list)

    def add_label(self, email_id: str, label: str) -> None:
        labels = self.labels.setdefault(email_id, [])
        if label not in labels:
            labels.append(label)

    def labels_for(self, email_id: str) -> tuple[str, ...]:
        return tuple(self.labels.get(email_id, ()))


def _email_id(params: Mapping[str, Any]) -> str:
    email_id = str(params.get("email_id", "")).strip()
    if not email_id:
        raise ToolError("email_id is required")
    return email_id


class ReadEmail(Tool):
    """Read-only: returns the message it was pointed at."""

    name: ClassVar[str] = "read_email"
    action_ids: ClassVar[tuple[str, ...]] = ("email.read", "email.get")

    def __init__(self, mailbox: SimulatedMailbox) -> None:
        self.mailbox = mailbox

    def check(self, params: Mapping[str, Any]) -> None:
        _email_id(params)

    def apply(self, params: Mapping[str, Any]) -> tuple[Effect, ...]:
        email_id = _email_id(params)
        return (Effect(tool=self.name, target=email_id, detail="read"),)


class LabelEmail(Tool):
    """Applies one label to one message."""

    name: ClassVar[str] = "label"
    action_ids: ClassVar[tuple[str, ...]] = ("email.apply_label", "email.label")

    def __init__(self, mailbox: SimulatedMailbox) -> None:
        self.mailbox = mailbox

    def check(self, params: Mapping[str, Any]) -> None:
        _email_id(params)
        if not str(params.get("label", "")).strip():
            raise ToolError("label is required")

    def apply(self, params: Mapping[str, Any]) -> tuple[Effect, ...]:
        email_id = _email_id(params)
        label = str(params["label"]).strip()
        before = self.mailbox.labels_for(email_id)
        self.mailbox.add_label(email_id, label)
        detail = f"labelled {label}" if label not in before else f"already had {label}"
        return (Effect(tool=self.name, target=email_id, detail=detail),)


class ArchiveEmail(Tool):
    """Files a message out of the inbox."""

    name: ClassVar[str] = "archive"
    action_ids: ClassVar[tuple[str, ...]] = ("email.archive", "email.move_to_archive")

    def __init__(self, mailbox: SimulatedMailbox) -> None:
        self.mailbox = mailbox

    def check(self, params: Mapping[str, Any]) -> None:
        _email_id(params)

    def apply(self, params: Mapping[str, Any]) -> tuple[Effect, ...]:
        email_id = _email_id(params)
        if email_id not in self.mailbox.archived:
            self.mailbox.archived.append(email_id)
        return (Effect(tool=self.name, target=email_id, detail="archived"),)


class CreateDraft(Tool):
    """Writes a private draft. Reversible, and never a send."""

    name: ClassVar[str] = "create_draft"
    action_ids: ClassVar[tuple[str, ...]] = ("email.create_draft", "email.draft")

    def __init__(self, mailbox: SimulatedMailbox) -> None:
        self.mailbox = mailbox

    def check(self, params: Mapping[str, Any]) -> None:
        _email_id(params)
        if not str(params.get("body", "")).strip():
            raise ToolError("body is required")

    def apply(self, params: Mapping[str, Any]) -> tuple[Effect, ...]:
        email_id = _email_id(params)
        recipients = params.get("to") or params.get("recipients") or ()
        if isinstance(recipients, str):
            recipients = (recipients,)
        self.mailbox.drafts[email_id] = Draft(
            email_id=email_id,
            body=str(params["body"]),
            to=tuple(str(item) for item in recipients),
        )
        return (Effect(tool=self.name, target=email_id, detail="draft saved"),)


class NotifyUser(Tool):
    """Tells the user what happened. Local to the assistant, so the floor treats it
    as reversible and it is what the PROCEED_AND_NOTIFY route commits."""

    name: ClassVar[str] = "notify"
    action_ids: ClassVar[tuple[str, ...]] = ("email.notify",)

    def __init__(self, mailbox: SimulatedMailbox) -> None:
        self.mailbox = mailbox

    def check(self, params: Mapping[str, Any]) -> None:
        if not str(params.get("text", "")).strip():
            raise ToolError("text is required")

    def apply(self, params: Mapping[str, Any]) -> tuple[Effect, ...]:
        notification = Notification(
            text=str(params["text"]),
            email_id=str(params.get("email_id", "")),
            case_id=str(params.get("case_id", "")),
        )
        self.mailbox.notifications.append(notification)
        target = notification.email_id or notification.case_id or "user"
        return (Effect(tool=self.name, target=target, detail="notified the user"),)


class SendEmail(Tool):
    """A send that validates like a real one and never leaves the mailbox.

    Recipients are required, and the intent is recorded on the receipt, so the run can
    be graded on what it *would* have sent while nothing is sent at all.
    """

    name: ClassVar[str] = "send_email"
    action_ids: ClassVar[tuple[str, ...]] = ("email.send", "email.send_email")
    leaves_the_mailbox: ClassVar[bool] = True

    def __init__(self, mailbox: SimulatedMailbox) -> None:
        self.mailbox = mailbox

    def check(self, params: Mapping[str, Any]) -> None:
        recipients = params.get("to") or params.get("recipients") or ()
        if isinstance(recipients, str):
            recipients = (recipients,)
        if not [item for item in recipients if str(item).strip()]:
            raise ToolError("a send needs at least one recipient")
        if not str(params.get("body", "")).strip():
            raise ToolError("a send needs a body")

    def apply(self, params: Mapping[str, Any]) -> tuple[Effect, ...]:
        recipients = params.get("to") or params.get("recipients") or ()
        if isinstance(recipients, str):
            recipients = (recipients,)
        addresses = ",".join(sorted(str(item) for item in recipients))
        return (
            Effect(
                tool=self.name,
                target=addresses,
                detail=f"simulated send to {addresses} (nothing left the mailbox)",
            ),
        )


TOOL_CLASSES: tuple[type[Tool], ...] = (
    ReadEmail,
    LabelEmail,
    ArchiveEmail,
    CreateDraft,
    NotifyUser,
    SendEmail,
)

# One place maps the dataset's action ids to the tools that implement them. A dataset
# id with no entry - ``email.forward``, ``finance.pay_invoice``, ``secrets.disclose`` -
# has no tool on purpose, and the floor's unrecognized-tool rule escalates it.
ACTION_TO_TOOL: Mapping[str, str] = {
    action_id: tool_class.name
    for tool_class in TOOL_CLASSES
    for action_id in tool_class.action_ids
}


def build_registry(mailbox: SimulatedMailbox | None = None) -> ToolRegistry:
    """Every simulated tool, over one mailbox."""
    held = mailbox if mailbox is not None else SimulatedMailbox()
    return ToolRegistry(tool_class(held) for tool_class in TOOL_CLASSES)


__all__ = [
    "ACTION_TO_TOOL",
    "TOOL_CLASSES",
    "ArchiveEmail",
    "CreateDraft",
    "Draft",
    "LabelEmail",
    "Notification",
    "NotifyUser",
    "ReadEmail",
    "SendEmail",
    "SimulatedMailbox",
    "build_registry",
]
