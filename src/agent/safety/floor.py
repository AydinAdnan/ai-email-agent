"""Safety Floor — Pure-function deterministic guardrails.

FLOOR_VERSION = "1.0"
Rule modifications must be code diffs, never learned.
Zero LLM dependence.
"""
import re
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from src.agent.safety.injection import plan_deviation, scan

FLOOR_VERSION = "1.0"

# Identity domain assumed when the caller supplies no user context.
DEFAULT_USER_DOMAIN = "example.com"

# Sends above this recipient count count as mass sends.
MASS_SEND_THRESHOLD = 5


class ActionClass(StrEnum):
    """Deterministic classification of proposed agent actions.
    
    - IRREVERSIBLE_EXTERNAL: Touch third parties or outer world (max autonomy: ASK_FIRST_WITH_PREDRAFT)
    - IRREVERSIBLE_INTERNAL: Irrevocable internal operations (PROCEED_AND_NOTIFY minimum)
    - REVERSIBLE: Local operations easily undone (PROCEED_SILENTLY allowed)
    - READ_ONLY: Passive queries with zero side-effects (PROCEED_SILENTLY allowed)
    """
    IRREVERSIBLE_EXTERNAL = "IRREVERSIBLE_EXTERNAL"
    IRREVERSIBLE_INTERNAL = "IRREVERSIBLE_INTERNAL"
    REVERSIBLE = "REVERSIBLE"
    READ_ONLY = "READ_ONLY"


class VetoLevel(StrEnum):
    """Veto severity level returned by floor_check.
    
    When veto is True, router directly routes to veto_level:
    - NONE: No floor veto (router proceeds to uncertainty / bandit evaluation)
    - ASK: Requires explicit human approval (halts autonomous execution)
    - ESCALATE: Critical hazard or out-of-policy action; must not proceed autonomously
    """
    NONE = "NONE"
    ASK = "ASK"
    ESCALATE = "ESCALATE"


class Route(StrEnum):
    """The four autonomy outcomes a candidate action can be routed to.

    PROCEED_SILENTLY and PROCEED_AND_NOTIFY act without interrupting the user;
    ASK_FIRST_WITH_PREDRAFT interrupts with an exact draft; ESCALATE takes no
    action and hands the email to the user. Only the floor decides which of the
    four stay available.

    The values are the dataset's autonomy vocabulary verbatim, so events, gold
    labels and report lanes parse them without a translation table.
    """
    PROCEED_SILENTLY = "PROCEED_SILENTLY"
    PROCEED_AND_NOTIFY = "PROCEED_AND_NOTIFY"
    ASK_FIRST_WITH_PREDRAFT = "ASK_FIRST_WITH_PREDRAFT"
    ESCALATE = "ESCALATE"


ALL_ROUTES: tuple[Route, ...] = (
    Route.PROCEED_SILENTLY,
    Route.PROCEED_AND_NOTIFY,
    Route.ASK_FIRST_WITH_PREDRAFT,
    Route.ESCALATE,
)

# Highest-risk route each action class may reach, before vetoes narrow it further.
_CLASS_ROUTE_CEILING: dict[ActionClass, tuple[Route, ...]] = {
    ActionClass.READ_ONLY: ALL_ROUTES,
    ActionClass.REVERSIBLE: ALL_ROUTES,
    ActionClass.IRREVERSIBLE_INTERNAL: (
        Route.PROCEED_AND_NOTIFY,
        Route.ASK_FIRST_WITH_PREDRAFT,
        Route.ESCALATE,
    ),
    ActionClass.IRREVERSIBLE_EXTERNAL: (Route.ASK_FIRST_WITH_PREDRAFT, Route.ESCALATE),
}


@dataclass(frozen=True)
class SafetyVerdict:
    """Immutable outcome of evaluating a proposed action against the safety floor."""
    veto: bool
    veto_level: VetoLevel
    allowed_routes: tuple[Route, ...]
    reason: str
    rule_id: str | None = None
    action_class: ActionClass | None = None


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
    display_name: str = ""
    pre_committed_plan: Sequence[str] | None = None
    user_domain: str = DEFAULT_USER_DOMAIN


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

# Sends, including deferred ones: a scheduled send is an external send that
# happens later, so it is classified by the same recipient rules.
_SEND_TOOLS = {
    "send_email",
    "forward",
    "forward_email",
    "schedule",
    "schedule_email",
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
        if isinstance(v, (int, float)) and (
            "amount" in k.lower() or "price" in k.lower() or "cost" in k.lower()
        ):
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
    user_domain: str = DEFAULT_USER_DOMAIN,
) -> ActionClass:
    """Deterministically map tool name + parameters to an ActionClass."""
    # 1. Financial check: money manipulation is always highest-risk external
    if _has_financial_intent(tool_name, params):
        return ActionClass.IRREVERSIBLE_EXTERNAL

    # 2. Outbound sending tools, including deferred (scheduled) sends
    if tool_name in _SEND_TOOLS:
        recipients = _extract_recipients(params)

        # Unresolvable targets fail closed, as do mass sends
        if not recipients or len(recipients) > MASS_SEND_THRESHOLD:
            return ActionClass.IRREVERSIBLE_EXTERNAL

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
        [ActionPayload, ActionClass, EmailContext | None, str],
        tuple[VetoLevel, str] | None,
    ]


# Rule Evaluators
def _eval_injection_tripwires(
    action: ActionPayload,
    action_class: ActionClass,
    email: EmailContext | None,
    user_domain: str,
) -> tuple[VetoLevel, str] | None:
    """FLR-INJ-001: Prompt injection tripwires in email body or metadata must be escalated."""
    if email:
        scan_res = scan(
            text=f"{email.subject} {email.body}",
            sender=email.sender,
            display_name=email.display_name,
            user_domain=user_domain,
        )
        if scan_res.is_injected:
            return (VetoLevel.ESCALATE, f"Prompt injection tripwire detected: {scan_res.reason}")
    return None


def _eval_plan_deviation(
    action: ActionPayload,
    action_class: ActionClass,
    email: EmailContext | None,
    user_domain: str,
) -> tuple[VetoLevel, str] | None:
    """FLR-INJ-002: Actions deviating from pre-committed plan must be escalated."""
    if email and email.pre_committed_plan is not None:
        deviated, reason = plan_deviation(
            action_tool=action.tool_name,
            action_params=action.params,
            pre_committed_plan=email.pre_committed_plan,
            untrusted_body=email.body,
        )
        if deviated:
            return (VetoLevel.ESCALATE, f"Plan deviation detected: {reason}")
    return None


def _eval_money_movement(
    action: ActionPayload,
    action_class: ActionClass,
    email: EmailContext | None,
    user_domain: str,
) -> tuple[VetoLevel, str] | None:
    """FLR-001: Autonomous money movement or financial transactions are prohibited."""
    if _has_financial_intent(action.tool_name, action.params):
        return (VetoLevel.ESCALATE, "Financial transaction or money movement detected in action parameters")
    if (
        email
        and _FINANCIAL_KEYWORD_PATTERN.search(f"{email.subject} {email.body}")
        and action_class in {ActionClass.IRREVERSIBLE_EXTERNAL, ActionClass.IRREVERSIBLE_INTERNAL}
    ):
        return (
            VetoLevel.ESCALATE,
            "Financial context detected in email for non-reversible action; autonomous execution prohibited",
        )
    return None


def _eval_credential_security(
    action: ActionPayload,
    action_class: ActionClass,
    email: EmailContext | None,
    user_domain: str,
) -> tuple[VetoLevel, str] | None:
    """FLR-002: Credential or account security tampering is prohibited."""
    if _has_credential_intent(action.tool_name, action.params):
        return (VetoLevel.ESCALATE, "Credential or account modification detected")
    return None


def _eval_unknown_tool(
    action: ActionPayload,
    action_class: ActionClass,
    email: EmailContext | None,
    user_domain: str,
) -> tuple[VetoLevel, str] | None:
    """FLR-003: Unrecognized tool calls must not execute autonomously."""
    if action.tool_name not in _KNOWN_TOOLS:
        return (VetoLevel.ESCALATE, f"Unrecognized tool '{action.tool_name}' blocked by safety floor")
    return None


def _eval_irreversible_external(
    action: ActionPayload,
    action_class: ActionClass,
    email: EmailContext | None,
    user_domain: str,
) -> tuple[VetoLevel, str] | None:
    """FLR-004: Irreversible external actions require explicit human confirmation (max autonomy: ASK)."""
    if action_class == ActionClass.IRREVERSIBLE_EXTERNAL:
        return (VetoLevel.ASK, "Irreversible external action requires explicit human confirmation")
    return None


def _eval_mass_send(
    action: ActionPayload,
    action_class: ActionClass,
    email: EmailContext | None,
    user_domain: str,
) -> tuple[VetoLevel, str] | None:
    """FLR-005: Outbound messages above the mass-send threshold require approval."""
    recipients = _extract_recipients(action.params)
    if len(recipients) > MASS_SEND_THRESHOLD:
        return (
            VetoLevel.ASK,
            f"Mass recipient send (>{MASS_SEND_THRESHOLD} recipients) requires explicit user approval",
        )
    return None


def _eval_permanent_deletion(
    action: ActionPayload,
    action_class: ActionClass,
    email: EmailContext | None,
    user_domain: str,
) -> tuple[VetoLevel, str] | None:
    """FLR-006: Permanent deletion of mailbox items cannot be executed autonomously."""
    if action.tool_name in {"delete_email", "delete", "trash_email"} and (
        action.params.get("permanent", False) or action.params.get("purge", False)
    ):
        return (VetoLevel.ASK, "Permanent mailbox item deletion requires human confirmation")
    return None


# Versioned, immutable rule table (evaluated in strict top-down precedence)
FLOOR_RULES: tuple[FloorRule, ...] = (
    FloorRule("FLR-INJ-001", "Prompt injection tripwire scanner", _eval_injection_tripwires),
    FloorRule("FLR-INJ-002", "Plan deviation check", _eval_plan_deviation),
    FloorRule("FLR-001", "Money movement hard block", _eval_money_movement),
    FloorRule("FLR-002", "Credential/account security guard", _eval_credential_security),
    FloorRule("FLR-003", "Unrecognized tool guard", _eval_unknown_tool),
    FloorRule("FLR-005", "Mass send threshold requires approval", _eval_mass_send),
    FloorRule("FLR-004", "Irreversible external send requires approval", _eval_irreversible_external),
    FloorRule("FLR-006", "Permanent deletion requires approval", _eval_permanent_deletion),
)


def _mask_routes(action_class: ActionClass, veto_level: VetoLevel) -> tuple[Route, ...]:
    """Drop every route the floor forbade, so the learner never sees them as options."""
    allowed = _CLASS_ROUTE_CEILING[action_class]
    if veto_level is VetoLevel.ESCALATE:
        return (Route.ESCALATE,)
    if veto_level is VetoLevel.ASK:
        # A rule that demands approval also removes acting-then-notifying
        return tuple(
            route for route in allowed if route in (Route.ASK_FIRST_WITH_PREDRAFT, Route.ESCALATE)
        )
    return allowed


def floor_check(
    action: ActionPayload,
    email: EmailContext | None = None,
    user_domain: str | None = None,
) -> SafetyVerdict:
    """Evaluate a proposed action against the deterministic safety floor.

    Returns the surviving routes as well as the veto: an action class that may
    never be silent keeps PROCEED_AND_NOTIFY, ASK_FIRST_WITH_PREDRAFT and
    ESCALATE, a fenced action keeps ESCALATE alone. ``user_domain`` falls back to the domain carried
    by the email, then to DEFAULT_USER_DOMAIN.
    """
    effective_domain = user_domain or (email.user_domain if email else DEFAULT_USER_DOMAIN)
    action_class = classify_action(action.tool_name, action.params, user_domain=effective_domain)

    for rule in FLOOR_RULES:
        result = rule.evaluator(action, action_class, email, effective_domain)
        if result is not None:
            veto_level, reason = result
            return SafetyVerdict(
                veto=True,
                veto_level=veto_level,
                allowed_routes=_mask_routes(action_class, veto_level),
                reason=reason,
                rule_id=rule.rule_id,
                action_class=action_class,
            )

    return SafetyVerdict(
        veto=False,
        veto_level=VetoLevel.NONE,
        allowed_routes=_mask_routes(action_class, VetoLevel.NONE),
        reason="Action permitted under safety floor rules",
        rule_id=None,
        action_class=action_class,
    )
