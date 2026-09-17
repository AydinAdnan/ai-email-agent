from __future__ import annotations

import hashlib
from typing import Any, TypedDict

from agent.events import Message
from agent.safety.floor import SafetyVerdict
from agent.tools.registry import PreparedAction, Receipt
from agent.triage import Triage

STATE_SCHEMA_VERSION = "1"


class GraphState(TypedDict, total=False):
    """One decision, from arrival to receipt.

    Ids and hashes rather than the mail itself: the state is what a checkpoint and a trace
    hold, so nothing here may be text that arrived in an email. Values stay scalars,
    lists and mappings, because a tuple comes back from the checkpointer as a list.
    """

    case_id: str
    message_id: str
    thread_id: str
    lane: str
    sequence_index: int
    message_digest: str
    dataset_digest: str
    replay_seed: int
    replay_digest: str

    hints: dict[str, Any]
    proposal: dict[str, Any]
    floor: dict[str, Any]
    route: str
    action_id: str

    prepared: dict[str, Any]
    receipt: dict[str, Any]
    interrupt: dict[str, Any]

    feedback: list[str]
    claims: list[str]

    node: str
    trace: list[str]
    errors: list[str]


# The fields a trace may print, taken from the schema so the two cannot drift. An
# allowlist: a field added later is invisible in traces until it is named here, which is
# a small debuggability bug rather than a mail body in a shared artifact.
TRACE_KEYS: tuple[str, ...] = tuple(GraphState.__annotations__)


def digest_of(value: str) -> str:
    """A short stable digest of a text, for a field that must not hold the text."""
    return "sha256:" + hashlib.sha256(value.encode("utf-8")).hexdigest()[:16]


def message_digest(message: Message) -> str:
    """Identify a message by content, so a trace can name the mail it read."""
    return digest_of(f"{message.message_id}\n{message.subject}\n{message.body}")


def hint_fields(triage: Triage | None) -> dict[str, Any]:
    """The pre-triage reading, as traceable fields."""
    if triage is None:
        return {}
    return {
        "intent": triage.intent,
        "relationship_class": triage.relationship_class,
        "confidence": round(triage.confidence, 4),
        "needs_model": triage.needs_model,
        "signals": list(triage.signals),
    }


def verdict_fields(verdict: SafetyVerdict) -> dict[str, Any]:
    """The floor's verdict, as traceable fields."""
    return {
        "rule_id": verdict.rule_id or "",
        "veto": verdict.veto,
        "veto_level": _plain(verdict.veto_level),
        "action_class": _plain(verdict.action_class),
        "allowed_routes": [_plain(route) for route in verdict.allowed_routes],
        "reason": verdict.reason,
    }


def prepared_fields(prepared: PreparedAction | None) -> dict[str, Any]:
    """What would run. Step params are left out: a draft's body would be one of them,
    and the digest already identifies the exact plan."""
    if prepared is None:
        return {}
    return {
        "action_id": prepared.action_id,
        "digest": prepared.digest,
        "steps": [step.tool for step in prepared.steps],
        "blocked": list(prepared.blocked),
        "summary": prepared.summary(),
    }


def receipt_fields(receipt: Receipt | None) -> dict[str, Any]:
    """What was committed. Effect targets are scrubbed by the sink."""
    if receipt is None:
        return {}
    return {
        "receipt_id": receipt.receipt_id,
        "route": _plain(receipt.route),
        "action_id": receipt.action_id,
        "prepared_digest": receipt.prepared_digest,
        "effects": [
            {"tool": effect.tool, "target": effect.target, "detail": effect.detail}
            for effect in receipt.effects
        ],
        "blocked": list(receipt.blocked),
    }


def _plain(value: Any) -> Any:
    """An enum becomes its value, so a round trip through the checkpointer is exact."""
    return getattr(value, "value", value)
