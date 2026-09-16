"""Safety Floor — Pure-function deterministic guardrails.

FLOOR_VERSION = "1.0"
Rule modifications must be code diffs, never learned.
Zero LLM dependence.
"""
from dataclasses import dataclass
from enum import Enum
import re
from typing import Any, Callable, Optional, Sequence

FLOOR_VERSION = "1.0"


class ActionClass(str, Enum):
    """Deterministic classification of proposed agent actions.
    
    Reference: ringg-takehome-design-plan (§5 Layer 1)
    - IRREVERSIBLE_EXTERNAL: Touch third parties or outer world (Max autonomy: ASK)
    - IRREVERSIBLE_INTERNAL: Irrevocable internal operations (NOTIFY minimum; ASK if low conf)
    - REVERSIBLE: Local operations easily undone (SILENT allowed)
    - READ_ONLY: Passive queries with zero side-effects (SILENT allowed)
    """
    IRREVERSIBLE_EXTERNAL = "IRREVERSIBLE_EXTERNAL"
    IRREVERSIBLE_INTERNAL = "IRREVERSIBLE_INTERNAL"
    REVERSIBLE = "REVERSIBLE"
    READ_ONLY = "READ_ONLY"


class VetoLevel(str, Enum):
    """Veto severity level returned by floor_check.
    
    When veto is True, router directly routes to veto_level:
    - NONE: No floor veto (router proceeds to uncertainty / bandit evaluation)
    - ASK: Requires explicit human approval (halts autonomous execution)
    - ESCALATE: Critical hazard or out-of-policy action; must not proceed autonomously
    """
    NONE = "NONE"
    ASK = "ASK"
    ESCALATE = "ESCALATE"


@dataclass(frozen=True)
class SafetyVerdict:
    """Immutable outcome of evaluating a proposed action against the safety floor."""
    veto: bool
    veto_level: VetoLevel
    reason: str
    rule_id: Optional[str] = None
    action_class: Optional[ActionClass] = None


@dataclass(frozen=True)
class ActionPayload:
    """Standardized representation of a candidate tool action."""
    tool_name: str
    params: dict[str, Any]


@dataclass(frozen=True)
class EmailContext:
    """Email metadata and body context passed into safety evaluations."""
    email_id: str
    sender: str
    recipients: Sequence[str]
    subject: str
    body: str
    user_domain: str = "example.com"


# Pattern definitions for financial and credential tripwires
_FINANCIAL_KEYWORD_PATTERN = re.compile(
    r"\b(wire|wire\s*transfer|bank\s*transfer|routing\s*number|account\s*number|iban|swift|swift\s*code|"
    r"invoice|payment|pay\s*out|payout|remittance|refund|credit\s*card|crypto|bitcoin|usdt|eth|wallet\s*address)\b|"
    r"[₹$€£]\s*[\d,]+(\.\d+)?|\b[\d,]+(\.\d+)?\s*(usd|inr|eur|gbp)\b",
    re.IGNORECASE,
)

_CREDENTIAL_PATTERN = re.compile(
    r"\b(password\s*reset|reset\s*password|api[_\s-]*key|access[_\s-]*token|oauth[_\s-]*token|secret[_\s-]*key|"
    r"private[_\s-]*key|ssh[_\s-]*key|credentials|auth[_\s-]*token)\b",
    re.IGNORECASE,
)

_KNOWN_TOOLS = {
    # Outbound communications
    "send_email",
    "forward",
    "forward_email",
    # Drafts (reversible)
    "draft_reply",
    "draft_email",
    "create_draft",
    # Mailbox organization (reversible)
    "archive",
    "archive_email",
    "label",
    "label_email",
    "add_label",
    "remove_label",
    "schedule",
    "schedule_email",
    # Deletions
    "delete_email",
    "delete",
    "trash_email",
    # Read-only
    "read_email",
    "search_emails",
    "search",
    "get_thread",
    "summarize",
}


def _extract_recipients(params: dict[str, Any]) -> list[str]:
    """Extract and normalize all recipient addresses from action parameters."""
    recipients: list[str] = []
    
    # Check common recipient fields
    for field in ("to", "cc", "bcc", "recipients", "recipient"):
        val = params.get(field)
        if isinstance(val, str):
            for addr in val.split(","):
                clean = addr.strip()
                if clean:
                    recipients.append(clean)
        elif isinstance(val, (list, tuple, set)):
            for item in val:
                if isinstance(item, str) and item.strip():
                    recipients.append(item.strip())
                    
    return recipients


def _is_external_address(email_address: str, user_domain: str) -> bool:
    """Return True if email_address domain does not match user_domain."""
    if "@" not in email_address:
        return True
    domain = email_address.split("@")[-1].strip().lower()
    return domain != user_domain.strip().lower()


def _has_financial_intent(tool_name: str, params: dict[str, Any]) -> bool:
    """Check if tool name or any parameter value contains financial keywords."""
    if _FINANCIAL_KEYWORD_PATTERN.search(tool_name):
        return True
        
    for k, v in params.items():
        if _FINANCIAL_KEYWORD_PATTERN.search(str(k)):
            return True
        if isinstance(v, str) and _FINANCIAL_KEYWORD_PATTERN.search(v):
            return True
        elif isinstance(v, (int, float)) and ("amount" in k.lower() or "price" in k.lower() or "cost" in k.lower()):
            return True
            
    return False


def _has_credential_intent(tool_name: str, params: dict[str, Any]) -> bool:
    """Check if tool name or parameters contain credential manipulation keywords."""
    if _CREDENTIAL_PATTERN.search(tool_name):
        return True
    for k, v in params.items():
        if _CREDENTIAL_PATTERN.search(str(k)) or (isinstance(v, str) and _CREDENTIAL_PATTERN.search(v)):
            return True
    return False


def classify_action(
    tool_name: str,
    params: dict[str, Any],
    user_domain: str = "example.com"
) -> ActionClass:
    """Deterministically map tool name + parameters to an ActionClass.
    
    Evaluation precedence:
    1. Financial indicators -> IRREVERSIBLE_EXTERNAL
    2. Outbound sending (send_email / forward):
       - > 5 recipients -> IRREVERSIBLE_EXTERNAL (mass send)
       - Any recipient outside user_domain -> IRREVERSIBLE_EXTERNAL
       - All recipients within user_domain -> IRREVERSIBLE_INTERNAL
    3. Deletion (delete_email / delete / trash_email):
       - permanent=True / purge=True -> IRREVERSIBLE_INTERNAL
       - soft delete / trash -> REVERSIBLE
    4. Reversible operations (drafts, archive, label, schedule) -> REVERSIBLE
    5. Read-only queries (read, search, summarize) -> READ_ONLY
    6. Unrecognized tools -> IRREVERSIBLE_EXTERNAL (safe fallback)
    """
    # 1. Financial check: money manipulation is always highest-risk external
    if _has_financial_intent(tool_name, params):
        return ActionClass.IRREVERSIBLE_EXTERNAL

    # 2. Outbound sending tools
    if tool_name in {"send_email", "forward", "forward_email"}:
        recipients = _extract_recipients(params)
        
        # Mass send threshold (>5 recipients)
        if len(recipients) > 5:
            return ActionClass.IRREVERSIBLE_EXTERNAL
            
        # External domain recipient check
        if any(_is_external_address(r, user_domain) for r in recipients):
            return ActionClass.IRREVERSIBLE_EXTERNAL
            
        return ActionClass.IRREVERSIBLE_INTERNAL

    # 3. Mailbox deletion tools
    if tool_name in {"delete_email", "delete", "trash_email"}:
        if params.get("permanent", False) or params.get("purge", False):
            return ActionClass.IRREVERSIBLE_INTERNAL
        return ActionClass.REVERSIBLE

    # 4. Reversible tools
    if tool_name in {
        "draft_reply",
        "draft_email",
        "create_draft",
        "archive",
        "archive_email",
        "label",
        "label_email",
        "add_label",
        "remove_label",
        "schedule",
        "schedule_email",
    }:
        return ActionClass.REVERSIBLE

    # 5. Read-only inspection tools
    if tool_name in {"read_email", "search_emails", "search", "get_thread", "summarize"}:
        return ActionClass.READ_ONLY

    # 6. Unrecognized tool safe fallback
    return ActionClass.IRREVERSIBLE_EXTERNAL


@dataclass(frozen=True)
class FloorRule:
    """Representation of an audited, immutable safety floor rule."""
    rule_id: str
    description: str
    evaluator: Callable[
        [ActionPayload, ActionClass, Optional[EmailContext], str],
        Optional[tuple[VetoLevel, str]],
    ]


# Rule Evaluators
def _eval_money_movement(
    action: ActionPayload,
    action_class: ActionClass,
    email: Optional[EmailContext],
    user_domain: str,
) -> Optional[tuple[VetoLevel, str]]:
    """FLR-001: Autonomous money movement or financial transactions are prohibited."""
    if _has_financial_intent(action.tool_name, action.params):
        return (VetoLevel.ESCALATE, "Financial transaction or money movement detected in action parameters")
    if email and _FINANCIAL_KEYWORD_PATTERN.search(f"{email.subject} {email.body}"):
        if action_class in {ActionClass.IRREVERSIBLE_EXTERNAL, ActionClass.IRREVERSIBLE_INTERNAL}:
            return (
                VetoLevel.ESCALATE,
                "Financial context detected in email for non-reversible action; autonomous execution prohibited",
            )
    return None


def _eval_credential_security(
    action: ActionPayload,
    action_class: ActionClass,
    email: Optional[EmailContext],
    user_domain: str,
) -> Optional[tuple[VetoLevel, str]]:
    """FLR-002: Credential or account security tampering is prohibited."""
    if _has_credential_intent(action.tool_name, action.params):
        return (VetoLevel.ESCALATE, "Credential or account modification detected")
    return None


def _eval_unknown_tool(
    action: ActionPayload,
    action_class: ActionClass,
    email: Optional[EmailContext],
    user_domain: str,
) -> Optional[tuple[VetoLevel, str]]:
    """FLR-003: Unrecognized tool calls must not execute autonomously."""
    if action.tool_name not in _KNOWN_TOOLS:
        return (VetoLevel.ESCALATE, f"Unrecognized tool '{action.tool_name}' blocked by safety floor")
    return None


def _eval_irreversible_external(
    action: ActionPayload,
    action_class: ActionClass,
    email: Optional[EmailContext],
    user_domain: str,
) -> Optional[tuple[VetoLevel, str]]:
    """FLR-004: Irreversible external actions require explicit human confirmation (max autonomy: ASK)."""
    if action_class == ActionClass.IRREVERSIBLE_EXTERNAL:
        return (VetoLevel.ASK, "Irreversible external action requires explicit human confirmation")
    return None


def _eval_mass_send(
    action: ActionPayload,
    action_class: ActionClass,
    email: Optional[EmailContext],
    user_domain: str,
) -> Optional[tuple[VetoLevel, str]]:
    """FLR-005: Outbound messages with >5 recipients require human approval."""
    recipients = _extract_recipients(action.params)
    if len(recipients) > 5:
        return (VetoLevel.ASK, "Mass recipient send (>5 recipients) requires explicit user approval")
    return None


def _eval_permanent_deletion(
    action: ActionPayload,
    action_class: ActionClass,
    email: Optional[EmailContext],
    user_domain: str,
) -> Optional[tuple[VetoLevel, str]]:
    """FLR-006: Permanent deletion of mailbox items cannot be executed autonomously."""
    if action.tool_name in {"delete_email", "delete", "trash_email"}:
        if action.params.get("permanent", False) or action.params.get("purge", False):
            return (VetoLevel.ASK, "Permanent mailbox item deletion requires human confirmation")
    return None


# Versioned, immutable rule table (evaluated in strict top-down precedence)
FLOOR_RULES: tuple[FloorRule, ...] = (
    FloorRule("FLR-001", "Money movement hard block", _eval_money_movement),
    FloorRule("FLR-002", "Credential/account security guard", _eval_credential_security),
    FloorRule("FLR-003", "Unrecognized tool guard", _eval_unknown_tool),
    FloorRule("FLR-004", "Irreversible external send requires approval", _eval_irreversible_external),
    FloorRule("FLR-005", "Mass send threshold requires approval", _eval_mass_send),
    FloorRule("FLR-006", "Permanent deletion requires approval", _eval_permanent_deletion),
)


def floor_check(
    action: ActionPayload,
    email: Optional[EmailContext] = None,
    user_domain: str = "example.com",
) -> SafetyVerdict:
    """Evaluate a proposed action against the deterministic safety floor.
    
    Returns SafetyVerdict with:
    - veto: bool indicating whether autonomous execution is prevented
    - veto_level: VetoLevel (NONE, ASK, or ESCALATE)
    - reason: Human-auditable explanation
    - rule_id: ID of the triggering rule (or None if permitted)
    - action_class: Evaluated ActionClass
    """
    action_class = classify_action(action.tool_name, action.params, user_domain=user_domain)

    for rule in FLOOR_RULES:
        result = rule.evaluator(action, action_class, email, user_domain)
        if result is not None:
            veto_level, reason = result
            return SafetyVerdict(
                veto=True,
                veto_level=veto_level,
                reason=reason,
                rule_id=rule.rule_id,
                action_class=action_class,
            )

    return SafetyVerdict(
        veto=False,
        veto_level=VetoLevel.NONE,
        reason="Action permitted under safety floor rules",
        rule_id=None,
        action_class=action_class,
    )
