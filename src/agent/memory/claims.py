from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from typing import Any

from agent.memory.consent import Capability, ConsentRequired, Grant
from agent.safety.floor import Route


class ClaimError(ValueError):
    """Raised when a claim is underspecified, or about something never stored."""


class ClaimType(StrEnum):
    """What kind of thing the user told us. Each still needs its evidence."""

    FACT = "fact"
    EVENT = "event"
    PREFERENCE = "preference"
    BOUNDARY = "boundary"
    CORRECTION = "correction"


class ScopeAnchor(StrEnum):
    """How the claim's scope was arrived at, which is what its confidence means."""

    EXPLICIT = "explicit"
    INTENT = "intent"
    CONTEXT = "context"
    GLOBAL = "global"
    UNRESOLVED = "unresolved"


# Never inferred, never stored. The schema has no axis for who the user is - scope is
# sender, domain and intent, all of them about mail - so this is the second line rather
# than the only one: a quote that names one of these is refused, not remembered.
SENSITIVE_ATTRIBUTES = re.compile(
    r"\b(religio\w*|muslim|christian|jewish|hindu|atheis\w*|church|mosque|synagogue"
    r"|politic\w*|democrat|republican|voted?|voter|election"
    r"|health|diagnos\w*|medication|prescription|therapy|illness|disab\w*|hiv"
    r"|pregnan\w*|maternity|paternity|mental health"
    r"|gay|lesbian|bisexual|transgender|queer|lgbtq\w*|sexual\w*|orientation"
    r"|ethnic\w*|racial|racism|nationality|immigration status)\b",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class ClaimScope:
    """Where a claim applies: the axes the learner's buckets are built from."""

    sender: str | None = None
    domain: str | None = None
    intent: str | None = None

    @property
    def resolved(self) -> bool:
        """Whether the claim names anything narrower than the whole mailbox."""
        return bool(self.sender or self.domain or self.intent)

    def as_key(self) -> tuple[str, ...]:
        """A stable key for the claim's scope, for ids and later comparison."""
        return (self.sender or "", self.domain or "", self.intent or "")


@dataclass(frozen=True)
class Claim:
    """One thing to remember, with the evidence that justifies it.

    Required by the schema: the user's exact words, the message they were looking at,
    when it was recorded, where it applies, and how sure the parser was. A claim that is
    missing any of those, or that would say something about a protected attribute, does
    not exist.
    """

    claim_id: str
    type: ClaimType
    quote: str
    source_message_id: str
    source_case_id: str
    recorded_at: datetime
    scope: ClaimScope
    scope_anchor: ScopeAnchor
    confidence: float
    action_id: str | None = None
    route: Route | None = None
    params: Mapping[str, Any] = field(default_factory=dict)
    starts_after_case_id: str | None = None
    superseded_by: str | None = None

    def __post_init__(self) -> None:
        _require_text(self.quote, "quote")
        _require_text(self.source_message_id, "source_message_id")
        _require_text(self.source_case_id, "source_case_id")
        if self.recorded_at is None:
            raise ClaimError("a claim with no timestamp cannot be audited")
        if not 0.0 < self.confidence <= 1.0:
            raise ClaimError(f"confidence {self.confidence!r} is not in (0, 1]")
        if not self.scope.resolved and self.scope_anchor is not ScopeAnchor.GLOBAL:
            raise ClaimError(
                "the scope is unresolved: which mail this applies to has to be settled first"
            )
        if SENSITIVE_ATTRIBUTES.search(self.quote):
            raise ClaimError("a claim about a protected attribute is never stored")

    def describe(self) -> str:
        """The claim in plain words: what to do, where it applies, from when."""
        return f"{_action_words(self)} {_scope_words(self)}. {_start_words(self)}."

    @property
    def active(self) -> bool:
        """Whether this is the claim in force, rather than one a correction replaced."""
        return self.superseded_by is None


class ClaimStore:
    """The one claims table, and the only way into it.

    Closed by default: a store with no grant keeps nothing, so anything that means to
    learn has to hand it a grant that says so. ``stored_claims`` is what the plan's 4.1
    check reads.
    """

    def __init__(self, grant: Grant | None = None) -> None:
        self.grant = grant if grant is not None else Grant(capability=Capability.LEARN)
        self._claims: list[Claim] = []

    @property
    def stored_claims(self) -> int:
        """How many claims are in memory."""
        return len(self._claims)

    @property
    def claims(self) -> tuple[Claim, ...]:
        return tuple(self._claims)

    def may_learn(self, *, at: datetime) -> bool:
        return self.grant.may_learn(at=at)

    def store(self, claim: Claim) -> Claim:
        """Keep a confirmed claim, if there is consent for it. The same claim is kept once."""
        if not self.may_learn(at=claim.recorded_at):
            raise ConsentRequired(f"nothing was stored: {self.grant.why_not(at=claim.recorded_at)}")
        # The same claim twice is one claim: a correction carries the same id and replaces
        # what it corrects, which is how the superseded flag below ever gets set.
        self._claims = [stored for stored in self._claims if stored.claim_id != claim.claim_id]
        self._claims.append(claim)
        return claim

    def matching(self, *, sender: str = "", domain: str = "", intent: str = "") -> tuple[Claim, ...]:
        """The claims in force that bear on one mail, narrowest first.

        A claim with no scope bears on every mail; a claim scoped to something else does
        not bear on this one.
        """
        bearing = [
            claim
            for claim in self._claims
            if claim.active and _bears_on(claim, sender=sender, domain=domain, intent=intent)
        ]
        return tuple(sorted(bearing, key=lambda claim: len(claim.scope.as_key())))


def claim_id_for(
    quote: str,
    route: Route | None,
    action_id: str | None,
    params: Mapping[str, Any],
    scope: ClaimScope,
) -> str:
    """A stable id for the same claim said twice, so it is never stored twice."""
    payload = json.dumps(
        {
            "quote": quote.lower(),
            "route": route.value if route else None,
            "action": action_id,
            "params": dict(sorted(params.items())),
            "scope": scope.as_key(),
        },
        sort_keys=True,
    )
    return f"clm-{hashlib.sha256(payload.encode('utf-8')).hexdigest()[:12]}"


def _bears_on(claim: Claim, *, sender: str, domain: str, intent: str) -> bool:
    scope = claim.scope
    if scope.sender:
        return scope.sender.lower() == sender.lower()
    if scope.domain:
        return scope.domain.lower() == domain.lower()
    if scope.intent:
        return scope.intent.lower() == intent.lower()
    return True


def _require_text(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ClaimError(f"a claim needs its {field_name}")


def _action_words(claim: Claim) -> str:
    """The work in the user's own terms, from the pipeline's action vocabulary."""
    if claim.route is Route.ESCALATE:
        return "escalate"
    if claim.route is Route.ASK_FIRST_WITH_PREDRAFT:
        return "draft a reply to and ask you about"
    label = claim.params.get("label")
    if label:
        return f"label as {label} and tell me about"
    if claim.action_id == "email.archive" and claim.route is Route.PROCEED_SILENTLY:
        return "silently archive"
    if claim.action_id == "email.archive":
        return "archive"
    if claim.route is Route.PROCEED_SILENTLY:
        return "stop telling me about"
    if claim.route is Route.PROCEED_AND_NOTIFY:
        return "tell me about"
    return "handle"


def _scope_words(claim: Claim) -> str:
    scope = claim.scope
    if claim.scope_anchor is ScopeAnchor.GLOBAL:
        return "every future arrival"
    if scope.sender:
        return f"future mail from {scope.sender}"
    if scope.domain:
        return f"future mail from anyone at {scope.domain}"
    if scope.intent:
        return f"future {scope.intent} mail"
    return "future mail"


def _start_words(claim: Claim) -> str:
    if claim.starts_after_case_id:
        return f"This starts after {claim.starts_after_case_id}, with the next arrival"
    return "This starts with the next arrival"
