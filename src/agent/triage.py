"""Deterministic pre-triage (plan Commit 5.2).

Cheap, pure-Python hints read from the mail alone: envelope sender, recipients,
subject, body, attachments. It never grants anything -- the floor is still the only
thing that can mask a route, and the model proposal is still the only thing that can
propose. What it buys is that the common mail resolves without a model call, and that
a model is handed hints rather than a blank slate.

The input is a ``Message``, not an ``EmailEvent``: intent and relationship class are
the dataset's answers about this mail, so they hang off the ``Case`` where a
classifier cannot reach them. Everything this module infers comes from the mail, plus
the standing configuration a mailbox actually has - the user's own domain and any
known senders.

The vocabulary is the dataset's, so a route proposal, a model proposal and a gold
label are all graded in the same words.
"""
import re
from collections.abc import Mapping
from dataclasses import dataclass

from agent.events import Message

# The dataset's intent vocabulary, most policy-relevant first.
INTENTS = (
    "account verification",
    "security alert",
    "financial request",
    "attachment/document request",
    "cloud/AWS bill",
    "newsletter",
    "receipt",
    "recruiter follow-up",
    "scheduling",
    "customer support",
    "unsubscribe/archive",
    "information request",
)

# The dataset's relationship vocabulary, most policy-relevant first.
RELATIONSHIP_CLASSES = (
    "spoofed/unverified",
    "self/system notification",
    "newsletter/marketing",
    "cloud/billing",
    "recruiter",
    "unknown",
    "colleague",
    "manager",
    "friend",
    "vendor",
)

# Ordered marker rules; the first match wins, so the shapes that demand care come
# first and the catch-all stays last.
_INTENT_MARKERS: tuple[tuple[str, str], ...] = (
    (
        "account verification",
        r"\bverify your (account|identity)\b|confirm (your )?identity|verification code"
        r"|authorization code|password reset|confirm .{0,20}password|admin access to",
    ),
    (
        "security alert",
        r"security alert|new login|login from|new sign-?in|sign-?in attempt|unusual activity"
        r"|password (was )?changed|suspicious|vulnerability|\busn-\d",
    ),
    (
        "cloud/AWS bill",
        r"amazon web services (invoice|bill)|\baws\b.{0,40}(invoice|bill|usage)\b"
        r"|\b(google )?cloud\b.{0,30}\binvoice\b|\bcloud (bill|usage)\b"
        r"|infrastructure (invoice|bill)|usage (charges|report)\b",
    ),
    (
        # After the cloud bills, because an invoice from a verified billing sender is a
        # bill; this is a stranger asking the user to move money.
        "financial request",
        r"\bwire\b|bank transfer|gift card|remit|payment (is )?due|past due|transfer funds"
        r"|outstanding (balance|invoice)|authorization token|access token|api key"
        r"|duplicate charge|re-?commit",
    ),
    (
        "attachment/document request",
        r"forward .{0,40}(deck|spreadsheet|file|document|statement|roadmap)"
        r"|send (me|us) (the )?(file|document|statement|spreadsheet|deck)"
        r"|\bshare\b.{0,30}(document|file|deck)|salary spreadsheet|confidential (roadmap|deck)"
        r"|\b(attached|attachment|attach)\b.{0,30}\b(file|document|resume|cv)\b"
        r"|my resume|resume submission",
    ),
    (
        "newsletter",
        r"unsubscribe|newsletter|\bpromotions?\b|\bissue #\d|digest #\d|\bdigest\b"
        r"|weekly (roundup|digest|issue)|\b\d+% (off|discount)|discount|webinar"
        r"|\bgrowth hacks?\b|last chance|release notes|\bpodcast\b|exclusive (offer|discount)",
    ),
    (
        "unsubscribe/archive",
        r"unsubscribe from all|\barchive\b|storage (critical|full)|clean ?up|\bquota\b",
    ),
    (
        "receipt",
        r"\breceipt\b|your (purchase|order)|order confirmation|booking confirmation"
        r"|transaction (id|date)|payment (method|received)|confirmation #\w",
    ),
    (
        "recruiter follow-up",
        r"\brecruit|\bcandidate\b|\bhiring\b|opportunit(y|ies)|my client|compensation"
        r"|\brole at\b|role - comp|principal architect",
    ),
    (
        "scheduling",
        r"\bmeeting\b|\bcalendar\b|reschedul|\bavailability\b|catch ?up|\bsync\b"
        r"|would you have time|lock in a time|planning session|this week|\bcall\b",
    ),
    (
        "customer support",
        r"\bsupport\b|\bticket\b|case #|your (recent )?order|refund|renewal"
        r"|\bsubscription\b|\blicense\b|expire",
    ),
    (
        "information request",
        r"\?|could you|can you|would you|\bneed\b|\bquestion\b|\bupdate\b|\breport\b",
    ),
)

# Sender shapes that identify a relationship on their own.
_SERVICE_LOCAL_PARTS = frozenset(
    {
        "alerts", "alert", "notifications", "notification", "no-reply", "noreply",
        "donotreply", "do-not-reply", "monitoring", "status", "billing", "receipts",
        "reports", "security-noreply", "support",
    }
)
_MARKETING_LOCAL_PARTS = frozenset({"news", "newsletter", "marketing", "promo", "offers", "info", "community"})
_RECRUITER_MARKERS = re.compile(r"recruit|talent|careers|hiring|jobs", re.IGNORECASE)
_BILLING_MARKERS = re.compile(r"billing|invoice|cloud|aws|payments", re.IGNORECASE)
_AUTHORITY_NAMES = re.compile(
    r"\b(it support|help ?desk|security team|administrator|admin|billing department|payroll"
    r"|audit department|compliance|internal check|external desk|auth-help)\b",
    re.IGNORECASE,
)

MONEY = re.compile(r"\$\s?([0-9][0-9,]*(?:\.[0-9]{1,2})?)")
# The persona policy's synthetic threshold: receipts at or below it need no
# notification. It is config, not a label, and Commit 3.x keeps it in one place.
RECEIPT_SILENT_THRESHOLD = 50.0


@dataclass(frozen=True)
class Triage:
    """What can be said about a message before any model is called."""

    intent: str
    relationship_class: str
    signals: tuple[str, ...]
    confidence: float
    needs_model: bool

    def __post_init__(self) -> None:
        if self.intent not in INTENTS:
            raise ValueError(f"unknown intent {self.intent!r}")
        if self.relationship_class not in RELATIONSHIP_CLASSES:
            raise ValueError(f"unknown relationship class {self.relationship_class!r}")


def amount_in(text: str) -> float | None:
    """The largest amount mentioned in a text, as a float."""
    found = [float(match.replace(",", "")) for match in MONEY.findall(text)]
    return max(found) if found else None


def user_domain(message: Message) -> str:
    """The mailbox's own domain, taken from where the message was addressed."""
    for address in (*message.recipients, *message.cc):
        if "@" in address:
            return address.rsplit("@", 1)[1].lower()
    return ""


def triage(
    message: Message,
    *,
    known_senders: Mapping[str, str] | None = None,
    domain: str | None = None,
) -> Triage:
    """Infer intent and relationship class from the mail, deterministically."""
    known = {address.lower(): klass for address, klass in (known_senders or {}).items()}
    address = message.sender.email.lower()
    sender_domain = address.rsplit("@", 1)[1] if "@" in address else ""
    local_part = address.split("@", 1)[0]
    ours = (domain if domain is not None else user_domain(message)).lower()

    text = " ".join((message.subject, message.body)).strip()
    signals: list[str] = []
    intent = _first_intent(text, signals)
    relationship, confidence = _relationship(
        message, known, address, sender_domain, local_part, ours, intent, signals
    )
    return Triage(
        intent=intent,
        relationship_class=relationship,
        signals=tuple(signals),
        confidence=confidence,
        needs_model=confidence < 0.9,
    )


def intents_matching(text: str) -> tuple[str, ...]:
    """Which intents this text's words point at, most policy-relevant first.

    Exposed for the feedback parser: a person saying "promotions" or "cron status" is
    naming a class of mail, and the words that decide a class should be the ones the
    classifier already reads rather than a second list kept in step by hand.
    """
    return tuple(
        intent for intent, pattern in _INTENT_MARKERS if re.search(pattern, text, re.IGNORECASE)
    )


def _first_intent(text: str, signals: list[str]) -> str:
    for intent, pattern in _INTENT_MARKERS:
        if re.search(pattern, text, re.IGNORECASE):
            signals.append(f"intent marker matched for '{intent}'")
            return intent
    signals.append("no intent marker matched; read as an information request")
    return "information request"


def _relationship(
    message: Message,
    known: Mapping[str, str],
    address: str,
    sender_domain: str,
    local_part: str,
    ours: str,
    intent: str,
    signals: list[str],
) -> tuple[str, float]:
    if address in known:
        signals.append("sender is on the known-senders list")
        return known[address], 1.0

    if not message.sender.verified_identity:
        asks_for_trouble = intent in {
            "account verification",
            "financial request",
            "attachment/document request",
        }
        # The display name and the address only: searching the subject as well read
        # 'auth' or 'verification' in honest mail as an impersonation attempt.
        claims_authority = bool(
            _AUTHORITY_NAMES.search(message.sender.display_name)
            or _AUTHORITY_NAMES.search(local_part)
        )
        if claims_authority or asks_for_trouble:
            signals.append("unverified sender claiming authority or asking for access")
            return "spoofed/unverified", 0.95
        signals.append("sender identity is not verified")
        return "unknown", 0.7

    if ours and sender_domain == ours:
        signals.append("sender is inside the mailbox's own domain")
        return "colleague", 0.8

    # What the mail is beats how the address looks: a Cloud invoice from a marketing-
    # looking address is still a bill.
    if intent == "cloud/AWS bill":
        signals.append("verified sender with a cloud bill")
        return "cloud/billing", 0.85
    if intent == "recruiter follow-up":
        signals.append("verified sender with recruiting mail")
        return "recruiter", 0.85
    if intent == "newsletter":
        signals.append("verified sender with bulk mail")
        return "newsletter/marketing", 0.9
    if intent in {"receipt", "customer support"}:
        signals.append(f"merchant mail that reads as a '{intent}'")
        return "vendor", 0.7
    if intent == "security alert":
        signals.append("verified sender with a security notice")
        return "self/system notification", 0.7

    if _marketing_sender(local_part):
        signals.append("marketing sender shape")
        return "newsletter/marketing", 0.8
    if _BILLING_MARKERS.search(sender_domain):
        signals.append("billing sender shape")
        return "cloud/billing", 0.8
    if _RECRUITER_MARKERS.search(sender_domain):
        signals.append("recruiting sender shape")
        return "recruiter", 0.8
    if local_part in _SERVICE_LOCAL_PARTS:
        signals.append("service sender shape")
        return "self/system notification", 0.7

    if intent in {"scheduling", "financial request", "attachment/document request"}:
        signals.append(f"verified external sender with a '{intent}' intent")
        return "vendor", 0.6

    signals.append("verified external sender with no distinguishing marker")
    return "vendor", 0.5


def _marketing_sender(local_part: str) -> bool:
    """Whether an address's local part reads as a bulk marketing sender."""
    parts = {local_part, *local_part.split(".")}
    return bool(_MARKETING_LOCAL_PARTS & parts)


__all__ = [
    "INTENTS",
    "RECEIPT_SILENT_THRESHOLD",
    "RELATIONSHIP_CLASSES",
    "Triage",
    "amount_in",
    "intents_matching",
    "triage",
    "user_domain",
]
