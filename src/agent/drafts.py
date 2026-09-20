"""Predrafts for the ASK route (Phase 7).

An ask is only worth the interruption if the reply is already written, so this module
does the three things a draft needs, in the order it needs them:

- ``retrieve_style`` picks a few consented sent examples - same person first, then same
  intent, then the rest - under a count cap and a token cap.
- ``draft_reply`` writes the reply out of what the mail and its thread actually say, and
  keeps a receipt: which statement came from where, and which question the draft could
  not answer.
- ``validate_draft`` decides whether the draft may be *shown*: addressed to whoever
  wrote, every date and amount traceable to the source, and no masking token left in
  text a human is about to approve.

Nothing here sends and nothing here picks a route. A predraft asks for the user's
attention; it is not permission to act.
"""
from __future__ import annotations

import re
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from enum import StrEnum
from math import ceil
from typing import Any

from agent.dataset import Case
from agent.safety.injection import scan
from agent.triage import MONEY

# A few examples and not many tokens of them: style is guidance for one short reply, and a
# mailbox that hands over twenty old emails is a prompt nobody can afford.
MAX_STYLE_EXAMPLES = 5
STYLE_TOKEN_BUDGET = 300
# ponytail: four characters to a token is the usual rough guess. The cap is a budget, not
# a bill; a real tokenizer earns its place only when a provider bills per draft.
CHARS_PER_TOKEN = 4

# How many questions a draft quotes back. Past three it is a summary, not a reply.
QUESTION_LIMIT = 3

# The tools whose output is text a human reads before it goes anywhere. An archive or a
# label has nothing to say, so only these get a predraft.
DRAFTING_TOOLS = frozenset({"create_draft", "draft_reply", "draft_email", "send_email"})

# The masker's own token shape, so a placeholder cannot survive into a draft that a human
# is about to approve as if it were the reply.
MASK_TOKEN = re.compile(r"<[A-Z][A-Z0-9_]*_\d+>")

# A date the draft may only state if the source states it too: ISO, month-day, numeric, or
# a bare ordinal day. The last one catches "the 14th", which is how a fabricated date is
# most likely to read; refusing a draft over "the 1st option" is the safe direction.
DATE = re.compile(
    r"(?:\d{4}-\d{2}-\d{2}"
    r"|(?:january|february|march|april|may|june|july|august|september|october|november"
    r"|december)\.?\s+\d{1,2}(?:st|nd|rd|th)?(?:,?\s*\d{4})?"
    r"|\d{1,2}/\d{1,2}(?:/\d{2,4})?"
    r"|\b\d{1,2}(?:st|nd|rd|th)\b)",
    re.IGNORECASE,
)

_SENTENCE = re.compile(r"(?<=[.?!])\s+")
_ORDINAL = re.compile(r"(?<=\d)(st|nd|rd|th)\b", re.IGNORECASE)
_SALUTATIONS = frozenset({"hi", "hey", "hello", "dear"})

# What a gap looks like in the body, so it cannot be approved blind.
UNANSWERED = "[needs your answer: {label}]"
# What is written instead of a question that is really an instruction. The text stays in
# the original mail; a draft does not repeat it in the user's voice.
UNREPEATED = "[needs your answer: {label}] - read the request in the original mail"


@dataclass(frozen=True)
class SentExample:
    """One reply the user actually sent, consented for style."""

    source_message_id: str
    recipient: str
    intent: str
    text: str
    sent_at: str = ""

    @classmethod
    def from_row(cls, row: Mapping[str, Any]) -> SentExample:
        """Read one example from the shape a mailbox hands over."""
        return cls(
            source_message_id=str(row.get("source_message_id", "")),
            recipient=str(row.get("recipient", "")).strip().lower(),
            intent=str(row.get("intent", "")),
            text=str(row.get("sent_text", "")),
            sent_at=str(row.get("timestamp", "")),
        )


def examples_from_row(row: Mapping[str, Any]) -> tuple[SentExample, ...]:
    """The consented sent examples a case carries, if the mailbox offered any.

    Not the dataset's answer: these are the user's own sent mail, the same rows a real
    adapter would read out of the sent folder.
    """
    raw = row.get("eligible_style_examples")
    if not isinstance(raw, Sequence) or isinstance(raw, (str, bytes)):
        return ()
    return tuple(SentExample.from_row(item) for item in raw if isinstance(item, Mapping))


def style_limit(row: Mapping[str, Any], *, default: int = MAX_STYLE_EXAMPLES) -> int:
    """How many examples this case allows.

    The row's ``needs_draft`` is deliberately not read: it mirrors the gold route, and a
    budget derived from the answer key is the answer key.
    """
    hint = row.get("token_budget_hint")
    if not isinstance(hint, Mapping):
        return default
    limit = hint.get("max_style_examples")
    return int(limit) if isinstance(limit, int) and limit > 0 else default


def estimate_tokens(text: str) -> int:
    """A rough token count for a budget decision, not for a bill."""
    return ceil(len(text) / CHARS_PER_TOKEN)


@dataclass(frozen=True)
class Picked:
    """One example that fits the budget, and why it was the one kept."""

    example: SentExample
    reason: str


@dataclass(frozen=True)
class Style:
    """What style the draft may borrow, and how the archive was narrowed to it."""

    picked: tuple[Picked, ...] = ()
    considered: int = 0
    dropped: int = 0

    @property
    def examples(self) -> tuple[SentExample, ...]:
        return tuple(item.example for item in self.picked)

    @property
    def tokens(self) -> int:
        """What the kept examples cost, in the same rough unit as the cap."""
        return sum(estimate_tokens(item.example.text) for item in self.picked)

    def describe(self) -> str:
        """One line naming what was kept and why, for a transcript."""
        if not self.picked:
            return "none (no consented sent examples for this mail)"
        kept = "; ".join(
            f"{item.reason}: {item.example.source_message_id}" for item in self.picked
        )
        line = f"{len(self.picked)} of {self.considered} ({self.tokens} tokens): {kept}"
        if self.dropped:
            line += f"; {self.dropped} left out over the cap"
        return line


def retrieve_style(
    examples: Iterable[SentExample],
    *,
    sender: str,
    intent: str,
    limit: int = MAX_STYLE_EXAMPLES,
    token_budget: int = STYLE_TOKEN_BUDGET,
) -> Style:
    """The few sent replies a draft may learn from: same person, then same intent, then rest.

    Ranked by recency inside each group, capped by count and by tokens. An example that
    does not fit the budget is left out rather than truncated: half of somebody's sentence
    is not their style.
    """
    ordered = sorted(examples, key=lambda item: item.sent_at, reverse=True)
    who = sender.strip().lower()
    groups = (
        ("same person", [item for item in ordered if item.recipient == who]),
        (
            "same intent",
            [item for item in ordered if item.recipient != who and item.intent == intent],
        ),
        (
            "fallback",
            [item for item in ordered if item.recipient != who and item.intent != intent],
        ),
    )

    picked: list[Picked] = []
    spent = 0
    dropped = 0
    for reason, group in groups:
        for item in group:
            cost = estimate_tokens(item.text)
            if len(picked) >= limit or spent + cost > token_budget:
                dropped += 1
                continue
            picked.append(Picked(example=item, reason=reason))
            spent += cost
    return Style(picked=tuple(picked), considered=len(ordered), dropped=dropped)


@dataclass(frozen=True)
class FactSource:
    """One thing the draft says, and where it came from.

    ``label`` and ``origin`` are the part a trace keeps; ``detail`` is the text itself,
    which belongs on the user's screen and nowhere else.
    """

    label: str
    origin: str
    detail: str = ""


@dataclass(frozen=True)
class Predraft:
    """A reply, written but not sent, with its facts and its gaps.

    The case id rides along because a draft is read next to a transcript of a dozen mails:
    the reply has to say which one it answers, both for a person and for a page that has to
    put it inside the right message.
    """

    recipient: str
    subject: str
    body: str
    case_id: str = ""
    facts: tuple[FactSource, ...] = ()
    unresolved: tuple[str, ...] = ()
    no_send: bool = True

    def params(self) -> dict[str, Any]:
        """The tool arguments that carry this draft. It is addressed to whoever wrote."""
        return {"to": (self.recipient,), "subject": self.subject, "body": self.body}

    def lines(self) -> tuple[str, ...]:
        """The draft as a human should see it before approving anything."""
        head = (
            f"draft for {self.case_id} -> {self.recipient} "
            "(nothing is sent: approving saves it to drafts)"
        )
        shown = [head, f"    Subject: {self.subject}"]
        shown += [f"    {line}" if line else "" for line in self.body.splitlines()]
        if self.facts:
            shown.append(
                "    facts: " + "; ".join(f"{fact.label} <- {fact.origin}" for fact in self.facts)
            )
        if self.unresolved:
            shown.append(f"    gaps ({len(self.unresolved)}):")
            shown += [f"      {gap}" for gap in self.unresolved]
        return tuple(shown)


def _reply_subject(subject: str) -> str:
    """The subject a reply carries, without stacking a second Re: on it."""
    bare = re.sub(r"^\s*(re|fwd|fw)\s*:\s*", "", subject, flags=re.IGNORECASE).strip()
    return f"Re: {bare}" if bare else "Re: your message"


def _first_name(display_name: str, address: str) -> str:
    """Who the reply greets: the display name's first word, else the address's local part."""
    words = display_name.strip().split()
    if words:
        return words[0]
    local = address.split("@")[0].replace(".", " ").strip()
    return local.split()[0].title() if local else "there"


def _salutation(style: Style) -> tuple[str, SentExample | None]:
    """The word the user opens with, borrowed from the best example and cited as such."""
    if style.examples:
        opening = style.examples[0].text.strip().splitlines()[0].strip()
        word = opening.split()[0].rstrip(",").strip() if opening else ""
        if word.lower() in _SALUTATIONS:
            return word.capitalize(), style.examples[0]
    return "Hi", None


def _signature(case: Case) -> str:
    """How the user signs off: their own address is the only name the mailbox holds."""
    recipients = case.event.message.recipients
    local = recipients[0].split("@")[0].replace(".", " ").strip() if recipients else ""
    return local.title() if local else ""


def open_questions(body: str, *, limit: int = QUESTION_LIMIT) -> tuple[str, ...]:
    """Every question the mail asks, capped: these are the gaps a draft cannot fill."""
    asked = [part.strip() for part in _SENTENCE.split(body) if part.strip().endswith("?")]
    return tuple(question for question in asked[:limit] if question)


def carried_instruction(text: str, case: Case) -> str:
    """An imperative-override phrase this text repeats from the mail, or the empty string.

    The scanner is the project's one scanner, but only its override shapes count here: a
    colleague writing "please send me the deck" is asking a person for something, and a
    draft quoting it is doing its job. "Ignore all previous instructions" is not a
    question to answer, and it must not reach a body a human may approve as the reply.
    """
    message = case.event.message
    found = scan(
        text,
        sender=message.sender.email,
        display_name=message.sender.display_name,
        # Judged as text a person might approve rather than as mail: the question is
        # whether the draft carries the instruction, not whether the sender was trusted.
        sender_verified=False,
    )
    return next(
        (signal for signal in found.signals if signal.startswith("Imperative control")), ""
    )


def _short(text: str, width: int = 96) -> str:
    """One line of a question, for a gap list nobody should have to scroll."""
    collapsed = " ".join(text.split())
    return collapsed if len(collapsed) <= width else f"{collapsed[: width - 1]}…"


def draft_reply(case: Case, style: Style) -> Predraft:
    """Write the reply the user would approve, and mark every gap it cannot fill.

    The body quotes the questions rather than answering them, because the answers are the
    user's: a draft that invents a date is the failure this route exists to prevent. Each
    question is marked in place, so a gap cannot be approved blind.

    ponytail: a question is treated as open unless the thread already carries a reply to
    it. Matching a question to an earlier answer needs retrieval this does not have yet,
    and the conservative direction is the safe one - it moves work to the user, not off them.
    """
    message = case.event.message
    salutation, borrowed = _salutation(style)
    recipient = message.sender.email
    questions = open_questions(message.body)

    facts = [
        FactSource("subject", "mail", _reply_subject(message.subject)),
        FactSource("sender", "mail", f"{message.sender.display_name} <{recipient}>"),
    ]
    if borrowed is not None:
        facts.append(
            FactSource(
                f"style {borrowed.source_message_id}",
                "style",
                f"the {salutation.lower()} you open {borrowed.intent} replies with",
            )
        )
    for earlier in case.event.thread.messages_before:
        facts.append(FactSource(f"thread {earlier.message_id}", "thread", earlier.subject))

    lines = [f"{salutation} {_first_name(message.sender.display_name, recipient)},", ""]
    lines.append("Thanks for the note.")
    unresolved: list[str] = []
    for index, question in enumerate(questions, start=1):
        label = f"question {index}"
        if carried_instruction(question, case):
            # The mail's "question" is an instruction aimed at the assistant. Repeating it
            # would put that instruction in the draft's own voice, in a body the user may
            # approve without reading the original, so the gap is named and nothing else.
            lines += ["", UNREPEATED.format(label=label)]
            unresolved.append(
                f"{label}: the mail asks for an action rather than an answer, so the "
                "draft does not repeat it"
            )
            continue
        lines += ["", f"You asked: {question}", UNANSWERED.format(label=label)]
        facts.append(FactSource(label, "mail", question))
        unresolved.append(f"{label}: {_short(question)}")
    lines += ["", "Best,", _signature(case)]

    return Predraft(
        case_id=case.case_id,
        recipient=recipient,
        subject=_reply_subject(message.subject),
        body="\n".join(lines),
        facts=tuple(facts),
        unresolved=tuple(unresolved),
    )


class DraftCode(StrEnum):
    """Why a draft may not be shown, as a code a test and a transcript can name."""

    WRONG_RECIPIENT = "WRONG_RECIPIENT"
    MASK_LEFTOVER = "MASK_LEFTOVER"
    LIFTED_INSTRUCTION = "LIFTED_INSTRUCTION"
    UNSOURCED_DATE = "UNSOURCED_DATE"
    UNSOURCED_AMOUNT = "UNSOURCED_AMOUNT"


@dataclass(frozen=True)
class Validation:
    """Whether a draft may be shown, and the first reason it may not."""

    ok: bool = True
    code: str = ""
    detail: str = ""

    def describe(self) -> str:
        return "may be shown" if self.ok else f"withheld ({self.code}: {self.detail})"


def source_text(case: Case) -> str:
    """Everything the draft may state without inventing it: the mail, and its thread."""
    message = case.event.message
    parts = [message.subject, message.body]
    for earlier in case.event.thread.messages_before:
        parts += [earlier.subject, earlier.body]
    return "\n".join(parts)


def _flatten(text: str) -> str:
    """Lower case, punctuation-free, ordinals dropped: "August 20th" and "august 20" match."""
    without_ordinals = _ORDINAL.sub("", text)
    return re.sub(r"[^a-z0-9]+", " ", without_ordinals.lower()).strip()


def validate_draft(draft: Predraft, case: Case) -> Validation:
    """Whether this draft may be shown. Fixed order, and the first refusal is the answer."""
    sender = case.event.message.sender.email.strip().lower()
    if draft.recipient.strip().lower() != sender:
        return Validation(
            ok=False,
            code=DraftCode.WRONG_RECIPIENT,
            detail=f"addressed to {draft.recipient}; the mail came from {sender}",
        )

    text = f"{draft.subject}\n{draft.body}"
    token = MASK_TOKEN.search(text)
    if token is not None:
        return Validation(
            ok=False,
            code=DraftCode.MASK_LEFTOVER,
            detail=f"{token.group(0)} survived into the draft",
        )

    # The subject is inherited from the mail, so it is the one field outside a quotation
    # where the mail's own words reach a body a human may approve.
    carried = carried_instruction(draft.subject, case)
    if carried:
        return Validation(
            ok=False,
            code=DraftCode.LIFTED_INSTRUCTION,
            detail=f"the subject repeats an instruction from the mail ({carried})",
        )

    source = _flatten(source_text(case))
    for stated in DATE.findall(text):
        if _flatten(stated) not in source:
            return Validation(
                ok=False,
                code=DraftCode.UNSOURCED_DATE,
                detail=f"the draft states {stated!r}, which the mail does not",
            )
    for amount in MONEY.findall(text):
        if _flatten(amount) not in source:
            return Validation(
                ok=False,
                code=DraftCode.UNSOURCED_AMOUNT,
                detail=f"the draft states {amount!r}, which the mail does not",
            )
    return Validation()


@dataclass(frozen=True)
class Drafting:
    """A draft, what it read, and whether it may be shown."""

    draft: Predraft
    validation: Validation
    style: Style = field(default_factory=Style)

    @property
    def ok(self) -> bool:
        return self.validation.ok

    def describe(self) -> str:
        return f"style: {self.style.describe()} | {self.validation.describe()}"


def drafting_for(case: Case, *, intent: str) -> Drafting:
    """Retrieve, write and check one draft for one mail."""
    style = retrieve_style(
        examples_from_row(case.row),
        sender=case.event.message.sender.email,
        intent=intent,
        limit=style_limit(case.row),
    )
    draft = draft_reply(case, style)
    return Drafting(draft=draft, validation=validate_draft(draft, case), style=style)


__all__ = [
    "CHARS_PER_TOKEN",
    "DATE",
    "DRAFTING_TOOLS",
    "MASK_TOKEN",
    "MAX_STYLE_EXAMPLES",
    "QUESTION_LIMIT",
    "STYLE_TOKEN_BUDGET",
    "UNANSWERED",
    "DraftCode",
    "Drafting",
    "FactSource",
    "Picked",
    "Predraft",
    "SentExample",
    "Style",
    "Validation",
    "draft_reply",
    "drafting_for",
    "estimate_tokens",
    "examples_from_row",
    "open_questions",
    "retrieve_style",
    "source_text",
    "style_limit",
    "validate_draft",
]
