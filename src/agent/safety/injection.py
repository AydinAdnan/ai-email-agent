"""Prompt injection tripwires and plan-deviation verification.

Zero LLM dependence — pure deterministic heuristics and pattern matching.
"""
import base64
from dataclasses import dataclass
import re
from typing import Any, Optional, Sequence

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

_COMPILED_INJECTION_RE = re.compile(
    "|".join(INJECTION_PATTERNS),
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


def _check_base64_injection(text: str) -> Optional[str]:
    """Inspect text for embedded base64 payloads that decode into control instructions."""
    candidates = _BASE64_CANDIDATE_RE.findall(text)
    for cand in candidates:
        try:
            decoded_bytes = base64.b64decode(cand, validate=True)
            decoded_text = decoded_bytes.decode("utf-8", errors="ignore").strip()
            if len(decoded_text) >= 8 and _COMPILED_INJECTION_RE.search(decoded_text):
                return f"Base64 encoded instruction detected ('{decoded_text[:40]}...')"
        except Exception:
            continue
    return None


def _check_zero_width_chars(text: str) -> Optional[str]:
    """Detect presence of invisible zero-width characters used for steganography."""
    count = sum(text.count(ch) for ch in ZERO_WIDTH_CHARS)
    if count > 0:
        return f"Zero-width character steganography detected ({count} invisible characters)"
    return None


def _check_authority_spoofing(
    sender: str,
    display_name: str,
    user_domain: str
) -> Optional[str]:
    """Flag if an external sender claims sensitive internal authority in display name."""
    if not display_name or not sender:
        return None
        
    sender_domain = sender.split("@")[-1].strip().lower() if "@" in sender else ""
    if sender_domain and sender_domain != user_domain.strip().lower():
        if _AUTHORITY_ROLE_PATTERNS.search(display_name):
            return (
                f"Authority claim mismatch: external sender '{sender}' "
                f"claims internal role '{display_name}'"
            )
    return None


def scan(
    text: str,
    sender: str = "",
    display_name: str = "",
    user_domain: str = "example.com"
) -> InjectionScanResult:
    """Scan untrusted email content and headers for prompt injection indicators."""
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

    # 4. Check for display-name vs domain authority spoofing
    spoof_signal = _check_authority_spoofing(sender, display_name, user_domain)
    if spoof_signal:
        signals.append(spoof_signal)

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
    pre_committed_plan: Optional[Sequence[str]] = None,
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
