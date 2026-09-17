from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


class ConsentRequired(RuntimeError):
    """Raised when something would be learned without consent for it."""

    code = "CONSENT_REQUIRED"


class Capability(StrEnum):
    """What the agent is able to do. Holding one says nothing about being allowed to."""

    READ = "mail.read"
    ACT = "mail.act"
    SEND = "mail.send"
    LEARN = "learn"


class Retention(StrEnum):
    """How long what was learned may be kept."""

    SESSION = "session"
    THIRTY_DAYS = "30d"
    UNTIL_REVOKED = "until_revoked"


@dataclass(frozen=True)
class LearningConsent:
    """What may be learned, for what purpose, kept how long, and until when."""

    purpose: str
    retention: Retention
    expiry: datetime | None = None
    granted_by: str = "user"

    def __post_init__(self) -> None:
        if not self.purpose.strip():
            raise ValueError("consent has to name a purpose")
        if not self.granted_by.strip():
            raise ValueError("consent has to name who granted it")

    def allows(self, *, at: datetime) -> bool:
        """Whether this consent still stands at a moment."""
        return self.expiry is None or at < self.expiry


@dataclass(frozen=True)
class Grant:
    """A capability and the consent that travels with it, separate objects on purpose.

    The capability alone permits nothing: ``may_learn`` is false for every combination
    that is not the learn capability *and* unexpired consent for a named purpose.
    """

    capability: Capability
    consent: LearningConsent | None = None

    def may_learn(self, *, at: datetime) -> bool:
        return (
            self.capability is Capability.LEARN
            and self.consent is not None
            and self.consent.allows(at=at)
        )

    def why_not(self, *, at: datetime) -> str:
        """One line a transcript can print about why nothing was kept."""
        if self.capability is not Capability.LEARN:
            return f"the agent holds {self.capability.value}, not learning"
        if self.consent is None:
            return "no consent to learn was given"
        return f"consent expired {self.consent.expiry.isoformat()}"  # type: ignore[union-attr]


def session_grant(*, purpose: str) -> Grant:
    """What a session carries when a human is present and typing.

    Consent is granted by a session on purpose, never by default: a store with no grant
    keeps nothing, so any code that means to learn has to say so out loud.
    """
    return Grant(
        capability=Capability.LEARN,
        consent=LearningConsent(purpose=purpose, retention=Retention.SESSION),
    )
