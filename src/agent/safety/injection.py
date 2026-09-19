"""Prompt injection tripwires and plan-deviation verification.

Zero LLM dependence — pure deterministic heuristics and pattern matching.
"""
import base64
import re
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

# Zero-width / invisible characters used for steganographic smuggling
ZERO_WIDTH_CHARS = ("\u200b", "\u200c", "\u200d", "\ufeff", "\u200e", "\u200f")

# Imperative override phrases, prompt leakage commands, and fake system delimiters
INJECTION_PATTERNS = (
    # Direct instruction overrides
    r"\b(ignore\s+(all\s+)?previous\s+instructions)\b",
    r"\b(disregard\s+(the\s+)?(above|previous|prior)\s+(instructions|prompt|directions)?)\b",
    r"\b(forget\s+all\s+(prior|previous)\s+(instructions|directions|rules))\b",
    r"\b(system\s+override)\b",
    r"\b(developer\s+mode\s+(enabled|activate|on))\b",
    r"\b(admin\s+mode\s+(enabled|activate|on))\b",
    r"\b(you\s+must\s+(now\s+)?(delete|forward|send|exfiltrate|reveal|leak))\b",
    r"\b(your\s+new\s+(task|instruction|role|objective)\s+is)\b",
    
    # Prompt leakage & fake compliance checks
    r"\b(system\s*prompt|developer\s*prompt|developer\s*instructions|initial\s*prompt|hidden\s*prompt)\b",
    r"\b(send|reply|reveal|print|output|display|show|attach)\s+(back\s+|with\s+)?(your\s+|the\s+)?(system\s*prompt|developer\s*instructions|developer\s*prompt|initial\s*prompt|hidden\s*prompt)\b",
    r"\b(fbi\s+(compliance|cyber|investigation|audit)\s+check)\b",
    r"\b(mandatory\s+security\s+audit)\b",
    r"\b(official\s+compliance\s+audit)\b",
    
    # Fake system boundary tags & prompt engineering break-outs
    r"⟦\s*(SYSTEM|DEVELOPER|EMAIL\s*END|SYSTEM\s*INSTRUCTION)\s*⟧",
    r"\[\s*INST\s*\]",
    r"\[\s*/\s*INST\s*\]",
    r"<\|im_start\|>",
    r"<\|im_end\|>",
    r"###\s+(System\s*Instruction|Instruction|Prompt)",
)

# Instructions aimed at the agent rather than at a person, which is the shape a stranger
# uses to make the agent act: tell it it may, tell it what to run, or tell it what to
# fetch out of the mailbox. These are deliberately NOT counted for every sender - a
# colleague writing "please send over the deck" is making a request, and merchant mail
# says "please reply to this email" - so they only count when the sender identity is
# unverified, which is the line between a request and a stranger giving orders.
AGENT_DIRECTIVE_PATTERNS = (
    # Telling the agent it has permission, which no sender can grant.
    r"\b(you are|you'?re|you have been)\s+(now\s+)?(fully\s+)?(authorized|permitted|approved)\b",
    # Naming what the agent should do, in the imperative.
    r"\b(please|kindly)\s+(reply|respond|send|forward|export|scan|run|execute|reveal"
    r"|attach|delete|purge|label|archive|bcc|cc|provide|share|confirm)\b",
    r"\b(reply|respond)\s+(back\s+)?with\b",
    r"\b(run|execute)\s+(the\s+)?(following|this|attached|below)\b",
    # Shell shapes: text meant to be executed, not read.
    r"\|\s*(bash|sh|zsh|powershell|python)\b",
    r"\b(curl|wget)\b[^\n]{0,80}\|\s*\w+",
    # Reaching for what the mailbox holds rather than for the reader's attention.
    r"\b(scan|search|read|export|summari[sz]e|forward)\s+(the\s+)?"
    r"(user'?s?|my|their|his|her)\s+(emails?|inbox|mail|tokens?|keys?|files?|contacts?)\b",
    r"\b(export|dump|exfiltrate|leak)\b[^\n]{0,40}\b(tokens?|keys?|credentials?|emails?|inbox)\b",
    r"\b(bcc|fcc)\s*:",
    # Going quiet about it.
    r"\b(do not|don'?t)\s+(notify|tell|inform|alert|cc|mention)\b|\bsuppress all user\b",
    r"\b(without|silently|silent)\b[^\n]{0,25}\b(notifying|telling|informing|user|approval)\b",
    # Mailbox and system housekeeping a stranger has no business commissioning.
    r"\b(clean\s?up|purge|empty|delete\s+all|free\s+up)\b[^\n]{0,30}"
    r"\b(required|needed|now|immediately|messages?|mailbox|storage|space)\b",
    r"\b(mailbox|storage|quota|disk)\b[^\n]{0,25}\b(critical|full|almost full|98%)\b",
    r"\b(scheduled|run|build)\b[^\n]{0,20}\b(cron|crontab|systemd|webhook|daemon|maintenance)\b",
)

_COMPILED_INJECTION_RE = re.compile(
    "|".join(INJECTION_PATTERNS),
    re.IGNORECASE,
)

_COMPILED_DIRECTIVE_RE = re.compile(
    "|".join(AGENT_DIRECTIVE_PATTERNS),
    re.IGNORECASE,
)

# Sensitive authority display-name claims
_AUTHORITY_ROLE_PATTERNS = re.compile(
    r"\b(fbi|cia|police|it\s*support|it\s*helpdesk|security\s*operations|security\s*team|"
    r"ceo\s*office|executive\s*board|compliance\s*officer|system\s*administrator|hr\s*department)\b",
    re.IGNORECASE,
)

# Candidate base64 regex (matches base64 alphanumeric chunks >= 20 chars ending with optional ==)
_BASE64_CANDIDATE_RE = re.compile(r"\b[A-Za-z0-9+/]{20,}={0,2}\b")


@dataclass(frozen=True)
class InjectionScanResult:
    """Outcome of scanning text and metadata for prompt injection signals."""
    is_injected: bool
    signals: tuple[str, ...]
    reason: str


def _decode_base64_candidate(candidate: str) -> str | None:
    """Return the decoded text of a base64 candidate, or None when it is not valid base64."""
    try:
        decoded = base64.b64decode(candidate, validate=True)
    except ValueError:
        return None
    return decoded.decode("utf-8", errors="ignore").strip() or None


def _check_base64_injection(text: str) -> str | None:
    """Inspect text for embedded base64 payloads that decode into control instructions."""
    for candidate in _BASE64_CANDIDATE_RE.findall(text):
        decoded_text = _decode_base64_candidate(candidate)
        if decoded_text and len(decoded_text) >= 8 and _COMPILED_INJECTION_RE.search(decoded_text):
            return f"Base64 encoded instruction detected ('{decoded_text[:40]}...')"
    return None


def _check_zero_width_chars(text: str) -> str | None:
    """Detect presence of invisible zero-width characters used for steganography."""
    count = sum(text.count(ch) for ch in ZERO_WIDTH_CHARS)
    if count > 0:
        return f"Zero-width character steganography detected ({count} invisible characters)"
    return None


def _names_its_own_domain(sender: str, display_name: str) -> bool:
    """Whether a display name names the domain it was sent from.

    A firm describing itself - 'Ubuntu Security Team' from ubuntu.example - is not
    claiming a role inside our organization, and reading it as one vetoed honest vendor
    mail. Impersonation looks different: 'Google Workspace Security Team' from an
    address that is not google.com is naming an organization it cannot prove.
    """
    domain = sender.split("@")[-1].strip().lower() if "@" in sender else ""
    label = domain.split(".")[0]
    if not label:
        return False
    return bool(re.search(rf"\b{re.escape(label)}\b", display_name, re.IGNORECASE))


def _check_authority_claims(
    sender: str,
    display_name: str,
    user_domain: str,
) -> str | None:
    """Flag authority claims whose backing identity is external or unverifiable.

    A display name is not authority. When an email claims an internal role we can
    only accept it if the sender address proves the same domain; an external
    domain is a spoof and a missing or unparseable sender is unresolved. An external
    name that names its own domain is asking for nothing, so it is left alone.
    """
    if not display_name or not _AUTHORITY_ROLE_PATTERNS.search(display_name):
        return None

    sender_domain = sender.split("@")[-1].strip().lower() if "@" in sender else ""
    if not sender_domain:
        return (
            f"Unresolved authority: display name '{display_name}' claims an internal role "
            "but the sender identity cannot be verified"
        )
    if sender_domain != user_domain.strip().lower() and not _names_its_own_domain(
        sender, display_name
    ):
        return (
            f"Authority claim mismatch: external sender '{sender}' "
            f"claims internal role '{display_name}'"
        )
    return None


def scan(
    text: str,
    sender: str = "",
    display_name: str = "",
    user_domain: str = "example.com",
    sender_verified: bool = True,
) -> InjectionScanResult:
    """Scan untrusted email content and headers for prompt injection indicators.

    ``sender_verified`` defaults to True, so a caller that knows nothing about the sender
    gets the behaviour of a sender whose identity holds up: the directive patterns below
    are for strangers, and assuming otherwise would veto ordinary mail that happens to
    say "please reply". The floor passes the message's real verification state.
    """
    signals: list[str] = []

    # 1. Check for zero-width steganography
    zw_signal = _check_zero_width_chars(text)
    if zw_signal:
        signals.append(zw_signal)

    # 2. Check for all imperative and prompt leakage patterns
    matched_phrases = set()
    for m in _COMPILED_INJECTION_RE.finditer(text):
        matched_phrases.add(m.group(0))
    for phrase in sorted(matched_phrases):
        signals.append(f"Imperative control / leakage phrase detected: '{phrase}'")

    # 3. Check for base64 encoded injection commands
    b64_signal = _check_base64_injection(text)
    if b64_signal:
        signals.append(b64_signal)

    # 4. Check for display-name vs domain authority claims
    spoof_signal = _check_authority_claims(sender, display_name, user_domain)
    if spoof_signal:
        signals.append(spoof_signal)

    # 5. Check for instructions addressed to the agent, which only count from a sender
    # whose identity the mailbox cannot vouch for.
    if not sender_verified:
        directives = {m.group(0).strip() for m in _COMPILED_DIRECTIVE_RE.finditer(text)}
        for directive in sorted(directives):
            signals.append(
                f"Agent-directed instruction from an unverified sender: '{directive}'"
            )

    if signals:
        return InjectionScanResult(
            is_injected=True,
            signals=tuple(signals),
            reason="; ".join(signals),
        )

    return InjectionScanResult(
        is_injected=False,
        signals=(),
        reason="Clean scan: no prompt injection signals detected",
    )


def plan_deviation(
    action_tool: str,
    action_params: dict[str, Any],
    pre_committed_plan: Sequence[str] | None = None,
    untrusted_body: str = "",
) -> tuple[bool, str]:
    """Verify that a proposed tool action conforms to the pre-committed triage plan.
    
    Email content is data, never authorization.
    Any tool call whose target or parameters deviate from the pre-committed plan
    triggers an immediate veto.
    """
    if not pre_committed_plan:
        return False, "No pre-committed plan specified"

    # 1. Action tool must be authorized in pre-committed plan
    if action_tool not in pre_committed_plan:
        return (
            True,
            f"Action tool '{action_tool}' was not authorized in pre-committed plan {list(pre_committed_plan)}",
        )

    # 2. Check if untrusted email body smuggled an unapproved recipient
    if action_tool in {"send_email", "forward", "forward_email"} and untrusted_body:
        recipients = action_params.get("to") or action_params.get("recipients") or []
        if isinstance(recipients, str):
            recipients = [r.strip() for r in recipients.split(",") if r.strip()]
            
        for recipient in recipients:
            if recipient.lower() in untrusted_body.lower() and recipient not in pre_committed_plan:
                plan_addresses = [p for p in pre_committed_plan if "@" in p]
                if plan_addresses and recipient not in plan_addresses:
                    return (
                        True,
                        f"Smuggled recipient '{recipient}' extracted from untrusted email body was not in plan",
                    )

    return False, "Action conforms to pre-committed plan"
