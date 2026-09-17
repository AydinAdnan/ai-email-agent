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
from dataclasses import dataclass, field, replace
from typing import Any, Protocol

from agent.events import Message
from agent.safety.floor import Route, strictest
from agent.tools.email_tools import ACTION_TO_TOOL, action_vocabulary, tool_for_action
from agent.triage import RECEIPT_SILENT_THRESHOLD, Triage, amount_in

# The action a proposal names when it has nothing to do. The floor does not know the
# tool it resolves to, so it fails closed to ESCALATE, which is the honest outcome for
# "nothing applies". It is also the action the dataset itself uses for such a case.
NO_ACTION_TOOL = "unsupported"

PROPOSAL_SCHEMA = {
    "route": "one of " + ", ".join(route.value for route in Route),
    "action_id": "one of the actions below, or null when nothing applies",
    "params": "only that action's arguments; never the message you were given",
    "rationale": "one short line explaining the route",
    "confidence": "0.0 to 1.0",
}

# A schema a small model must fill, not a shape it is asked to imitate. Every key is
# required and the action is an enum, so a proposal cannot omit an explanation or invent
# an action. Sending it is what removes the missing-key repairs a description-shaped
# prompt produced, and what keeps the action vocabulary to the one the registry holds.
PROPOSAL_JSON_SCHEMA: Mapping[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": list(PROPOSAL_SCHEMA),
    "properties": {
        "route": {"type": "string", "enum": [route.value for route in Route]},
        "action_id": {"type": ["string", "null"], "enum": [*ACTION_TO_TOOL, None]},
        "params": {"type": "object"},
        "rationale": {"type": "string"},
        "confidence": {"type": "number"},
    },
}

RESPONSE_FORMAT: Mapping[str, Any] = {
    "type": "json_schema",
    "json_schema": {"name": "proposal", "strict": True, "schema": PROPOSAL_JSON_SCHEMA},
}

# What a proposer may ask for, rendered from the registry so a small model is never left
# to guess a tool's name from a dataset id, and so the vocabulary cannot drift from the
# tools that actually exist.
ACTION_VOCABULARY = action_vocabulary()

# One answer to copy the shape of. Cheaper for a small model than reading five
# descriptions, and it shows what a filled-in ``params`` looks like.
PROPOSAL_EXAMPLE = json.dumps(
    {
        "route": Route.PROCEED_AND_NOTIFY.value,
        "action_id": "email.apply_label",
        "params": {"label": "Finance/Cloud"},
        "rationale": "a cloud bill from a known billing sender",
        "confidence": 0.7,
    }
)

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
# leaves the choice open: the action id, and the arguments it carries.
ACTION_BY_INTENT: Mapping[str, tuple[str, Mapping[str, Any]]] = {
    "newsletter": ("email.apply_label", {"label": "Newsletter"}),
    "cloud/AWS bill": ("email.apply_label", {"label": "Finance/Cloud"}),
    "receipt": ("email.apply_label", {"label": "Finance/Receipts"}),
    "scheduling": ("email.create_draft", {}),
    "information request": ("email.create_draft", {}),
    "customer support": ("email.create_draft", {}),
    "recruiter follow-up": ("email.create_draft", {}),
    "security alert": ("email.apply_label", {"label": "Security"}),
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


def persona_demanded_route(message: Message, hints: Triage) -> Route | None:
    """The route this mail compels on the persona's own account, or None when free.

    These are the persona's hard rules, not the floor's: no credential is disclosed to
    anyone, and a sender the mailbox does not already know asking for access, money or
    files is not a routine request. They used to live inside ``RuleProvider``, which
    made them true only of the offline stand-in - a model could propose a quiet route
    for the same mail and be believed. They are checked against every proposal instead.
    """
    outside = hints.relationship_class not in INTERNAL_RELATIONSHIPS
    ask = f"{message.subject}\n{message.body}"
    if (
        CREDENTIAL_ASKS.search(ask)
        or (hints.intent in ESCALATING_INTENTS and outside)
        or (outside and ESCALATING_ASKS.search(ask))
    ):
        return Route.ESCALATE
    return None


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
        fields = "\n".join(f'  "{key}": {text},' for key, text in PROPOSAL_SCHEMA.items())
        prompt = (
            "You are proposing how an email agent should handle one message. You are\n"
            "proposing only: a safety floor decides what is allowed, and it can veto you.\n"
            "Answer with one JSON object and nothing else, with every key:\n"
            f"{{\n{fields}\n}}\n\n"
            "The actions you may name, and the arguments each one takes:\n"
            f"{ACTION_VOCABULARY}\n"
            "An answer to copy the shape of:\n"
            f"{PROPOSAL_EXAMPLE}\n"
            "Name no other action, copy no other fields, and put nothing from the\n"
            "message into params unless an action above asks for it.\n\n"
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
        params: Mapping[str, Any] = {}

        if route is not Route.ESCALATE:
            if hints.intent == "receipt":
                route = _receipt_route(message)
            chosen = ACTION_BY_INTENT.get(hints.intent)
            if chosen is not None:
                action_id, params = chosen

        if route is Route.ESCALATE:
            action_id, params = None, {}

        return {
            "route": route.value,
            "action_id": action_id,
            "params": dict(params),
            "rationale": f"{hints.intent} from a {hints.relationship_class} sender",
            "confidence": hints.confidence,
        }


# Any OpenAI-compatible endpoint works here: the shape of the call is identical and only
# the base URL, the key's variable name and the model differ. OpenRouter goes through
# this path, which is why the model is configuration rather than a constant.
@dataclass(frozen=True)
class Endpoint:
    """An OpenAI-compatible endpoint's settings."""

    name: str
    api_key_env: str
    base_url: str
    default_model: str
    # Whether the endpoint accepts a structured-output response_format. A model that does
    # not support it answers with an error rather than with JSON, and the gateway's repair
    # attempt cannot fix a refused request, so this defaults to off for anything whose
    # support we cannot assume, and the prompt alone carries the schema instead.
    structured_output: bool = False

    @property
    def label(self) -> str:
        """How a run reports which model it used."""
        return f"{self.name}:{self.default_model}"


ENDPOINTS: Mapping[str, Endpoint] = {
    "openai": Endpoint(
        name="openai",
        api_key_env="OPENAI_API_KEY",
        base_url="https://api.openai.com/v1",
        default_model="gpt-4o-mini",
        structured_output=True,
    ),
    # Verified against the endpoint's own catalogue: this model lists response_format and
    # structured_outputs, so the schema is enforced rather than hoped for.
    "openrouter": Endpoint(
        name="openrouter",
        api_key_env="OPENROUTER_API_KEY",
        base_url="https://openrouter.ai/api/v1",
        default_model="inference-net/schematron-v2-small",
        structured_output=True,
    ),
}

SYSTEM_PROMPT = "You propose actions for an email agent. You never authorize."


class OpenAICompatibleProvider:
    """A model behind an OpenAI-compatible API. Used only when a key is configured."""

    def __init__(
        self,
        endpoint: Endpoint,
        *,
        api_key: str,
        model: str | None = None,
        temperature: float = 0.0,
        structured_output: bool | None = None,
        client: Any | None = None,
    ) -> None:
        self.endpoint = endpoint
        self.name = endpoint.name
        self.api_key = api_key
        self.base_url = endpoint.base_url
        self.model = model or endpoint.default_model
        self.temperature = temperature
        # Whether the schema is sent. It is not a decision a run has to make twice: the
        # endpoint declares it once and every proposal goes through the same request.
        self.structured_output = (
            endpoint.structured_output if structured_output is None else structured_output
        )
        self._client = client

    @property
    def label(self) -> str:
        """Which model a run is actually talking to."""
        return f"{self.name}:{self.model}"

    def _connect(self):
        """A client for this endpoint. Imported here so offline runs need no SDK."""
        if self._client is not None:
            return self._client
        from openai import AsyncOpenAI

        return AsyncOpenAI(api_key=self.api_key, base_url=self.base_url)

    async def complete(self, request: ProposalRequest) -> str:
        """Ask the model for one proposal, off the event loop."""
        kwargs: dict[str, Any] = {
            "model": self.model,
            "temperature": self.temperature,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": request.as_prompt()},
            ],
        }
        if self.structured_output:
            kwargs["response_format"] = RESPONSE_FORMAT
        response = await self._connect().chat.completions.create(**kwargs)
        return response.choices[0].message.content or ""


def _persona_checked(proposal: Proposal, message: Message, hints: Triage) -> Proposal:
    """Raise a proposal to whatever the persona's hard rules demand, and say so.

    Every provider goes through this, which is the point: the rules belong to the mail,
    not to whoever answered. Raising to an escalation also drops the action, because an
    escalation that still carried a candidate action would be asking the floor to decide
    something the persona already refused.
    """
    demanded = persona_demanded_route(message, hints)
    if demanded is None:
        return proposal
    route = strictest(proposal.route, demanded)
    if route is proposal.route:
        return proposal
    reason = f"persona rule raised {proposal.route.value} to {route.value}"
    if route is Route.ESCALATE:
        return replace(
            proposal,
            route=route,
            action_id=None,
            tool_name=NO_ACTION_TOOL,
            params={},
            rationale=f"{proposal.rationale} | {reason}",
        )
    return replace(proposal, route=route, rationale=f"{proposal.rationale} | {reason}")


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
            return _persona_checked(parse_proposal(first, provider=self.provider.name), message, hints)
        except (ProposalError, TimeoutError) as first_error:
            self.repairs += 1
            repair = ProposalRequest(message=message, hints=hints, repair_note=str(first_error))
            try:
                second = await self._ask(repair)
                return _persona_checked(
                    parse_proposal(second, provider=self.provider.name), message, hints
                )
            except (ProposalError, TimeoutError) as second_error:
                self.failures += 1
                raise ProposalError(
                    f"{self.provider.name} proposed nothing usable after one repair: "
                    f"{second_error}"
                ) from second_error

    async def _ask(self, request: ProposalRequest) -> str:
        """Ask once. A provider that fails in any way is a failed proposal, not a crash.

        A network error, an auth error or a bug in a custom provider used to escape as
        itself, which meant one bad call killed the whole session instead of the one
        case. It becomes a ``ProposalError`` here so the caller can fail closed.
        """
        try:
            return await asyncio.wait_for(self.provider.complete(request), self.timeout)
        except (ProposalError, TimeoutError):
            raise
        except Exception as error:
            raise ProposalError(
                f"{self.provider.name} failed: {type(error).__name__}: {error}"
            ) from error


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
    if action_id is not None:
        if not isinstance(action_id, str) or not action_id.strip():
            raise ProposalError("action_id must be a non-empty string or null")
        action_id = action_id.strip()
    if route is Route.ESCALATE and action_id is not None:
        raise ProposalError("escalation carries no action")

    # The tool is derived, never asked for. A proposer answers in the action vocabulary
    # it can see, and one id resolves to one tool here, which is the same rule the
    # reference labels go through. An id no tool holds resolves to itself, so the
    # floor's unrecognized-tool rule escalates it rather than this parser rejecting a
    # proposal the dataset itself contains.
    tool_name = NO_ACTION_TOOL if action_id is None else tool_for_action(action_id)

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


def build_provider(
    name: str,
    *,
    model: str | None = None,
    structured_output: bool | None = None,
    client: Any | None = None,
) -> ProposalProvider:
    """Resolve a provider by name, refusing one that cannot run here.

    The model comes from the flag, then ``WAJO_MODEL``, then the endpoint's default, so a
    run can name its model without any code change.
    """
    if name == RuleProvider.name:
        return RuleProvider()
    endpoint = ENDPOINTS.get(name)
    if endpoint is None:
        known = ", ".join((RuleProvider.name, *ENDPOINTS))
        raise ProposalError(f"unknown provider {name!r}; known providers: {known}")
    api_key = os.environ.get(endpoint.api_key_env, "")
    if not api_key:
        raise ProposalError(
            f"{endpoint.api_key_env} is not set, so {name} cannot run; put it in .env at the "
            f"repository root or export it"
        )
    return OpenAICompatibleProvider(
        endpoint,
        api_key=api_key,
        model=model or os.environ.get("WAJO_MODEL") or None,
        structured_output=structured_output,
        client=client,
    )


__all__ = [
    "ACTION_BY_INTENT",
    "ACTION_VOCABULARY",
    "CREDENTIAL_ASKS",
    "ENDPOINTS",
    "ESCALATING_ASKS",
    "ESCALATING_INTENTS",
    "INTERNAL_RELATIONSHIPS",
    "NO_ACTION_TOOL",
    "PROPOSAL_EXAMPLE",
    "PROPOSAL_JSON_SCHEMA",
    "PROPOSAL_SCHEMA",
    "RESPONSE_FORMAT",
    "ROUTE_BY_RELATIONSHIP",
    "SYSTEM_PROMPT",
    "Endpoint",
    "OpenAICompatibleProvider",
    "Proposal",
    "ProposalError",
    "ProposalGateway",
    "ProposalProvider",
    "ProposalRequest",
    "RuleProvider",
    "build_provider",
    "parse_proposal",
    "persona_demanded_route",
]
