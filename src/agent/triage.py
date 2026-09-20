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
        r"|password (was )?changed|suspicious|vulnerability|\busn-\d"
        # What a monitoring or identity address sends when something is failing, leaking
        # or being locked, which is a security notice before it is a report.
        r"|\bfatal\b|\bexception\b|\boutofmemory\b|\bcrash(ed)?\b|\b(alert|alarm)s?\b"
        r"|secret scanning|\bleak(ed)?\b|\bbreach\b|revoked?|suspended|terminated"
        r"|\bencryption key\b",
    ),
    (
        "cloud/AWS bill",
        # A cloud provider's own invoicing, named or not. It takes a billing word as well
        # as a provider name, so a usage summary that asks for nothing stays what it is.
        r"amazon web services (invoice|bill)|\baws\b.{0,60}(invoice|bill|balance|usage)"
        r"|\b(azure|microsoft azure|google cloud|\bgcp\b|datadog|cloudwatch|cloud service)\b"
        r".{0,60}\b(invoice|bill|billing statement|statement|charges|balance|amount due|"
        r"past due)\b|\bcloud (bill|invoice|statement|charges|usage)\b"
        r"|infrastructure (invoice|bill)",
    ),
    (
        # After the cloud bills, because an invoice from a verified billing sender is a
        # bill. This is a demand to move money - who to pay, where to send it - and an
        # ask for a token or a key is a security matter, not a payment one.
        "financial request",
        r"\bwire\b|wire transfer|bank transfer|routing number|account number|\biban\b|\bswift\b"
        r"|gift card|\bremit\b|\bremittances?\b|\bsort code\b|\bbeneficiary\b|\bbank details\b"
        r"|transfer funds|duplicate charge|re-?commit"
        # Asking *the reader* to change where money goes. A vendor's "update payment
        # details" in a renewal notice is customer support, and it is possessive-marked
        # so the two do not look alike.
        r"|(update|change|send)\s+(your|the)\s+(bank|payment|billing|card)\s"
        r"(details|information|account|number)\b"
        # 'Payment is due' is deliberately absent: an invoice says exactly that, and an
        # invoice is a receipt for money already owed, not a demand to move it.
        r"|past due",
    ),
    (
        "attachment/document request",
        r"forward .{0,40}(deck|spreadsheet|file|document|statement|roadmap)"
        r"|send (me|us) (the )?(file|document|statement|spreadsheet|deck)"
        r"|\bshare\b.{0,30}(document|file|deck)|salary spreadsheet|confidential (roadmap|deck)"
        # A request to be *sent* a document counts whatever the document is called: 'please
        # send me the disaster recovery runbook' asks for a file. The verb is what carries
        # the request, so a bare 'Runbook: https://...' in an alert is not one.
        r"|(send|share|forward)\b.{0,60}\b(runbook|playbook|diagram|schematic|notes|deck)\b"
        r"|\b(attached|attachment|attach)\b.{0,30}\b(file|document|resume|cv)\b"
        r"|my resume|resume submission",
    ),
    (
        "newsletter",
        # Bulk mail a reader did not ask for. A bare 'digest' is deliberately not here:
        # a weekly metrics digest from a monitoring address is a report, not a publication.
        r"unsubscribe|newsletter|\bpromotions?\b|\bissue #\d|digest #\d"
        r"|weekly (roundup|digest|issue)|\b\d+% (off|discount)|discount|webinar"
        r"|\bgrowth hacks?\b|last chance|release notes|\bpodcast\b|exclusive (offer|discount)",
    ),
    (
        "unsubscribe/archive",
        # The mailbox itself is what is being talked about, never the word alone: a colleague
        # asking about "the cleanup" or naming a folder "archive" is asking a question, and a
        # report that says "archive" is not an instruction to tidy anything up.
        r"unsubscribe from all|storage (critical|full)|mail ?box .{0,20}\b(over|full|quota|capacity)"
        r"|free up space|\bquota\b",
    ),
    (
        "receipt",
        # What a merchant sends once money has already moved: an amount, and no request.
        r"\breceipt\b|your (purchase|order)|order confirmation|booking confirmation"
        r"|flight confirmation|transaction (id|date)|payment (method|received)|confirmation #\w"
        r"|thank you for your (payment|purchase|order)|\b(invoice|folio|statement)\b"
        r".{0,60}(paid|\$\s?[\d,]+|\bpayment\b)",
    ),
    (
        "recruiter follow-up",
        # Solicitation, not the word 'hiring': a colleague asking for a headcount
        # estimate is asking for information.
        r"\brecruit|\bcandidate\b|opportunit(y|ies)|my client|compensation"
        r"|\brole at\b|role - comp|principal architect",
    ),
    (
        "scheduling",
        # A time with the reader, not a word that happens to appear in a report: a
        # metrics digest says 'this week', a call for proposals says 'call'.
        r"\bmeeting\b|\bcalendar\b|reschedul|\bavailability\b|catch ?up|would you have time"
        r"|lock in a time|planning session|\bdeadline\b|\bpriorit(y|ies)\b|\bmeetup\b"
        r"|\bjoin us\b|next week",
    ),
    (
        "customer support",
        # A ticket is a support ticket when it has a number on it. The bare word is a noun
        # a colleague's question uses too - "there's no linked ticket" - and that question
        # is not customer support.
        r"\bsupport (team|ticket|request|plan|desk)\b|ticket\s*(#|number|id|ref)\b|case #"
        r"|your (recent )?order"
        r"|refund|renewal|\bsubscription\b|\blicense\b|expire|\bdeliverables?\b",
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
# Addresses that send *publications*: bulk mail a reader did not ask for. A monitoring
# or reporting address is not one of them, which is what keeps a metrics digest a report.
_MARKETING_LOCAL_PARTS = frozenset(
    {
        "news", "newsletter", "marketing", "promo", "offers", "info", "community",
        "updates", "tips", "growth", "insights", "outreach", "sales", "digest",
        "weekly", "editorial", "blog", "campaigns", "hello", "team",
    }
)
_RECRUITER_MARKERS = re.compile(r"recruit|talent|careers|hiring|jobs", re.IGNORECASE)
_BILLING_MARKERS = re.compile(r"billing|invoice|cloud|aws|payments", re.IGNORECASE)
_AUTHORITY_NAMES = re.compile(
    r"\b(it support|help ?desk|security team|administrator|admin|billing department|payroll"
    r"|audit department|compliance|internal check|external desk|auth-help)\b",
    re.IGNORECASE,
)

# Addresses that send *machine mail*: a build result, a pull request opening, a widget
# publishing a new version. A reader cannot answer any of it, so where such a mail asks
# nothing it is bulk mail and gets filed, not a question that earns a drafted reply. A
# notice that reports a fault is not bulk - it asks the reader to know something - which
# is what keeps a production alert a notification.
_MACHINE_LOCAL_PARTS = frozenset(
    {
        "notifications", "notification", "notify", "alerts", "alert", "builds", "build",
        "ci", "no-reply", "noreply", "donotreply", "do-not-reply", "bot", "monitoring",
        "status", "ping",
    }
)
_FAULT_WORDS = re.compile(
    r"\bfatal\b|\bcritical\b|\bexception\b|\boutofmemory\b|\bcrash(ed|es|ing)?\b"
    r"|\bincident\b|\boutage\b|\bdegraded\b|\bbreach\b|\bvulnerab\w*\b|\badvisor(?:y|ies)\b"
    r"|\bsuspend(?:ed|ing)?\b|\brevok\w*\b|\balarms?\b|\balerts?\b|\bfail(?:ed|ure|ing|s)?\b"
    # "no action required" is the phrase a green build ends with, so the one fault phrase that
    # negates itself is read only where it is not negated: a build notice is not an alert.
    r"|\bspike\b|\bexpir\w*\b|(?<!\bno )\baction required\b|\bunusual\b|\bwarning\b|\boverdue\b",
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
    intent = _first_intent(text, signals, local_part)
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


def _first_intent(text: str, signals: list[str], local_part: str = "") -> str:
    """The intent this mail's words point at, with the sender's shape as the tiebreak.

    Words first: what a mail says beats who sent it. The fallback is the exception. A
    mail with no marketing word in it at all - "Top Hacker News Stories of the Week" -
    is still bulk mail when it arrives from a publisher's address, and the same shape
    from a monitoring address is the report the fallback already names.
    """
    found = "information request"
    for intent, pattern in _INTENT_MARKERS:
        if re.search(pattern, text, re.IGNORECASE):
            signals.append(f"intent marker matched for '{intent}'")
            found = intent
            break
    else:
        signals.append("no intent marker matched; read as an information request")
    if found == "information request" and local_part:
        if _marketing_sender(local_part):
            signals.append(
                f"publisher sender shape '{local_part}' and no marketing words; read as bulk mail"
            )
            return "newsletter"
        if _machine_sender(local_part) and not _FAULT_WORDS.search(text):
            signals.append(
                f"machine sender shape '{local_part}' reporting no fault; read as bulk mail "
                "the reader cannot answer"
            )
            return "newsletter"
    return found


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


def _machine_sender(local_part: str) -> bool:
    """Whether an address's local part reads as a machine that sends notifications."""
    parts = {local_part, *local_part.split(".")}
    return bool(_MACHINE_LOCAL_PARTS & parts)


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
