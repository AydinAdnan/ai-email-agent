"""Model proposal gateway (plan Commit 5.3).

A thin provider interface with a timeout and one schema-repair retry. What comes back
is always an untrusted ``Proposal``: it can propose a route and a candidate action, and
it can never authorize one. Authorization stays with the safety floor, which is the
only thing in the repository that turns a proposal into a decision.

The gateway does not trust prose either. A provider answers with text, the text has to
parse into the proposal schema, and a parse failure buys exactly one repair attempt
with the parser's complaint quoted back. A second failure raises ``ProposalError`` and
the caller fails closed - escalation, not a guess.

``RuleProvider`` answers from :mod:`agent.triage` and needs no network, which is what
makes the pipe testable and lets a run work offline. ``OpenAIProvider`` renders the
same request as a prompt and is used only when a key is configured.
"""
import asyncio
import json
import os
import re
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any, Protocol

from agent.events import Message
from agent.safety.floor import Route
from agent.triage import RECEIPT_SILENT_THRESHOLD, Triage, amount_in

# The tool the pipeline proposes when it has no action to take. The floor does not know
# it, so it fails closed to ESCALATE, which is the honest outcome for "nothing applies".
NO_ACTION_TOOL = "unsupported"

PROPOSAL_SCHEMA = {
    "route": "one of " + ", ".join(route.value for route in Route),
    "action_id": "a tool id such as email.apply_label, or null when nothing applies",
    "tool_name": "the tool the action maps to, or null",
    "params": "object of tool arguments",
    "rationale": "one short line explaining the route",
    "confidence": "0.0 to 1.0",
}

ROUTE_BY_RELATIONSHIP: Mapping[str, Route] = {
    "newsletter/marketing": Route.PROCEED_SILENTLY,
    "cloud/billing": Route.PROCEED_AND_NOTIFY,
    "self/system notification": Route.PROCEED_AND_NOTIFY,
    "vendor": Route.PROCEED_AND_NOTIFY,
    "colleague": Route.ASK_FIRST_WITH_PREDRAFT,
    "manager": Route.ASK_FIRST_WITH_PREDRAFT,
    "friend": Route.ASK_FIRST_WITH_PREDRAFT,
    "recruiter": Route.ASK_FIRST_WITH_PREDRAFT,
    "unknown": Route.ESCALATE,
    "spoofed/unverified": Route.ESCALATE,
}

# What the pipeline would do about the mail, per intent, when the sender relationship
# leaves the choice open.
ACTION_BY_INTENT: Mapping[str, tuple[str, str, Mapping[str, Any]]] = {
    "newsletter": ("email.apply_label", "label", {"label": "Newsletter"}),
    "cloud/AWS bill": ("email.apply_label", "label", {"label": "Finance/Cloud"}),
    "receipt": ("email.apply_label", "label", {"label": "Finance/Receipts"}),
    "scheduling": ("email.create_draft", "create_draft", {}),
    "information request": ("email.create_draft", "create_draft", {}),
    "customer support": ("email.create_draft", "create_draft", {}),
    "recruiter follow-up": ("email.create_draft", "create_draft", {}),
    "security alert": ("email.apply_label", "label", {"label": "Security"}),
}


# Intents that ask the reader for access, money or files. The persona policy says an
# unknown sender making that ask escalates immediately, so the pipeline does not get to
# choose a quieter route for them: only a sender the mailbox already knows may be asked.
ESCALATING_INTENTS = frozenset({"financial request", "account verification", "attachment/document request"})

# Persona boundary: no credential or secret disclosure under any circumstances, so an
# ask for one escalates whoever sends it. An ask shape, not a keyword: a security notice
# that merely mentions a password is not a request for one.
CREDENTIAL_ASKS = re.compile(
    r"(reply|send|share|forward|provide|give|confirm|paste|need|require)\b.{0,40}"
    r"\b(key|password|passphrase|token|credential|secrets?|api key|mfa code)\b"
    r"|(secret|api|access|private|production|stripe) key|\bsk_live\b|\bmfa code\b",
    re.IGNORECASE,
)

# Persona rule 6: an outside sender asking for files, access, money, forwarding or
# secrecy escalates immediately. Inside the mailbox the same ask may be answerable, so
# this one only applies to senders the mailbox does not already know.
ESCALATING_ASKS = re.compile(
    r"search (your|the) inbox|forward\b.{0,40}\b(emails?|notes|threads?|inbox)\b"
    r"|term sheet|acquisition offer|keep (this|it) (between us|quiet)|don'?t tell",
    re.IGNORECASE,
)

INTERNAL_RELATIONSHIPS = frozenset({"colleague", "manager", "friend"})


class ProposalError(RuntimeError):
    """Raised when a provider cannot produce a usable proposal, after one repair."""


@dataclass(frozen=True)
class Proposal:
    """An untrusted suggestion. Nothing acts on it without the floor."""

    route: Route
    action_id: str | None
    tool_name: str | None
    params: Mapping[str, Any] = field(default_factory=dict)
    rationale: str = ""
    confidence: float = 0.0
    provider: str = ""


@dataclass(frozen=True)
class ProposalRequest:
    """Everything a provider is allowed to see: the mail, plus what triage inferred."""

    message: Message
    hints: Triage
    repair_note: str = ""

    def as_prompt(self) -> str:
        """The request rendered for a text model. The mail is the only input."""
        message = self.message
        attachments = ", ".join(item.filename for item in message.attachments) or "none"
        prompt = (
            "You are proposing how an email agent should handle one message. You are\n"
            "proposing only: a safety floor decides what is allowed, and it can veto you.\n"
            "Answer with one JSON object and nothing else, with keys:\n"
            f"{json.dumps(PROPOSAL_SCHEMA, indent=2)}\n\n"
            f"from: {message.sender.display_name} <{message.sender.email}>\n"
            f"to: {', '.join(message.recipients)}\n"
            f"subject: {message.subject}\n"
            f"attachments: {attachments}\n"
            f"body:\n{message.body}\n\n"
            f"hints: intent={self.hints.intent!r} "
            f"relationship={self.hints.relationship_class!r} "
            f"signals={'; '.join(self.hints.signals) or 'none'}\n"
        )
        if self.repair_note:
            prompt += f"\nYour previous answer was rejected: {self.repair_note}\n"
        return prompt


class ProposalProvider(Protocol):
    """A source of untrusted proposal text."""

    name: str

    async def complete(self, request: ProposalRequest) -> str:
        """Return raw proposal text for one request."""


class RuleProvider:
    """The offline provider: proposes from triage, no network, deterministic.

    It is a stand-in for a model, and it is deliberately conservative about the routes
    where being wrong is expensive - an unverified stranger asking for access, money or
    files escalates rather than asks.
    """

    name = "rules"

    async def complete(self, request: ProposalRequest) -> str:
        return json.dumps(self.build(request.message, request.hints), sort_keys=True)

    def build(self, message: Message, hints: Triage) -> dict[str, Any]:
        """The rule proposal, before it is serialised like any other provider's."""
        route = ROUTE_BY_RELATIONSHIP[hints.relationship_class]
        action_id: str | None = NO_ACTION_TOOL
        tool_name: str | None = NO_ACTION_TOOL
        params: Mapping[str, Any] = {}

        outside = hints.relationship_class not in INTERNAL_RELATIONSHIPS
        ask = f"{message.subject}\n{message.body}"
        if (
            CREDENTIAL_ASKS.search(ask)
            or (hints.intent in ESCALATING_INTENTS and outside)
            or (outside and ESCALATING_ASKS.search(ask))
        ):
            route = Route.ESCALATE

        if route is not Route.ESCALATE:
            if hints.intent == "receipt":
                route = _receipt_route(message)
            chosen = ACTION_BY_INTENT.get(hints.intent)
            if chosen is not None:
                action_id, tool_name, params = chosen

        if route is Route.ESCALATE:
            action_id, tool_name, params = None, None, {}

        return {
            "route": route.value,
            "action_id": action_id,
            "tool_name": tool_name,
            "params": dict(params),
            "rationale": f"{hints.intent} from a {hints.relationship_class} sender",
            "confidence": hints.confidence,
        }


class OpenAIProvider:
    """The model provider. Used only when a key is configured."""

    name = "openai"

    def __init__(self, model: str = "gpt-4o-mini", temperature: float = 0.0) -> None:
        self.model = model
        self.temperature = temperature

    async def complete(self, request: ProposalRequest) -> str:
        """Ask the model for one proposal, off the event loop."""
        from openai import AsyncOpenAI  # imported here so the offline path needs no SDK

        client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])
        response = await client.chat.completions.create(
            model=self.model,
            temperature=self.temperature,
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": "You propose actions for an email agent. You never authorize.",
                },
                {"role": "user", "content": request.as_prompt()},
            ],
        )
        return response.choices[0].message.content or ""


class ProposalGateway:
    """Turns provider text into a validated proposal, with one repair attempt."""

    def __init__(self, provider: ProposalProvider, *, timeout: float = 20.0) -> None:
        self.provider = provider
        self.timeout = timeout
        self.repairs = 0
        self.failures = 0

    async def propose(self, message: Message, hints: Triage) -> Proposal:
        """Ask the provider, repair once if the answer does not parse, then fail closed."""
        request = ProposalRequest(message=message, hints=hints)
        try:
            first = await self._ask(request)
            return parse_proposal(first, provider=self.provider.name)
        except (ProposalError, TimeoutError) as first_error:
            self.repairs += 1
            repair = ProposalRequest(message=message, hints=hints, repair_note=str(first_error))
            try:
                second = await self._ask(repair)
                return parse_proposal(second, provider=self.provider.name)
            except (ProposalError, TimeoutError) as second_error:
                self.failures += 1
                raise ProposalError(
                    f"{self.provider.name} proposed nothing usable after one repair: "
                    f"{second_error}"
                ) from second_error

    async def _ask(self, request: ProposalRequest) -> str:
        return await asyncio.wait_for(self.provider.complete(request), self.timeout)


_FENCE = re.compile(r"^\s*```(?:json)?\s*|\s*```\s*$")


def parse_proposal(raw: str, provider: str = "") -> Proposal:
    """Validate one provider answer. Anything unexpected is an error, not a default."""
    if not isinstance(raw, str) or not raw.strip():
        raise ProposalError("empty response")
    try:
        payload = json.loads(_FENCE.sub("", raw))
    except json.JSONDecodeError as error:
        raise ProposalError(f"not JSON: {error}") from error
    if not isinstance(payload, dict):
        raise ProposalError(f"expected a JSON object, got {type(payload).__name__}")

    missing = [key for key in ("route", "rationale") if key not in payload]
    if missing:
        raise ProposalError(f"missing keys: {', '.join(missing)}")

    try:
        route = Route(str(payload["route"]).strip())
    except ValueError as error:
        raise ProposalError(
            f"route must be one of {[item.value for item in Route]}, got {payload['route']!r}"
        ) from error

    params = payload.get("params") or {}
    if not isinstance(params, dict):
        raise ProposalError("params must be an object")
    confidence = payload.get("confidence", 0.0)
    if not isinstance(confidence, int | float) or not 0.0 <= float(confidence) <= 1.0:
        raise ProposalError(f"confidence must be between 0 and 1, got {confidence!r}")

    action_id = payload.get("action_id")
    tool_name = payload.get("tool_name")
    if action_id is not None and not isinstance(action_id, str):
        raise ProposalError("action_id must be a string or null")
    if tool_name is not None and not isinstance(tool_name, str):
        raise ProposalError("tool_name must be a string or null")
    if (action_id is None) != (tool_name is None):
        raise ProposalError("action_id and tool_name must both be set or both be null")
    if route is Route.ESCALATE and action_id is not None:
        raise ProposalError("escalation carries no action")

    return Proposal(
        route=route,
        action_id=action_id,
        tool_name=tool_name,
        params=params,
        rationale=str(payload["rationale"])[:500],
        confidence=float(confidence),
        provider=provider,
    )


def _receipt_route(message: Message) -> Route:
    """The persona policy's receipt threshold, applied to the amount the mail states."""
    amount = amount_in(f"{message.subject} {message.body}")
    if amount is None or amount <= RECEIPT_SILENT_THRESHOLD:
        return Route.PROCEED_SILENTLY
    return Route.PROCEED_AND_NOTIFY


def build_provider(name: str) -> ProposalProvider:
    """Resolve a provider by name, refusing one that cannot run here."""
    if name == RuleProvider.name:
        return RuleProvider()
    if name == OpenAIProvider.name:
        if not os.environ.get("OPENAI_API_KEY"):
            raise ProposalError("OPENAI_API_KEY is not set, so the model provider cannot run")
        return OpenAIProvider()
    raise ProposalError(f"unknown provider {name!r}")


__all__ = [
    "ACTION_BY_INTENT",
    "CREDENTIAL_ASKS",
    "ESCALATING_ASKS",
    "ESCALATING_INTENTS",
    "INTERNAL_RELATIONSHIPS",
    "NO_ACTION_TOOL",
    "PROPOSAL_SCHEMA",
    "ROUTE_BY_RELATIONSHIP",
    "OpenAIProvider",
    "Proposal",
    "ProposalError",
    "ProposalGateway",
    "ProposalProvider",
    "ProposalRequest",
    "RuleProvider",
    "build_provider",
    "parse_proposal",
]
