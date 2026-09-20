"""Constrained feedback parser and scope echo (plan Commit 3.6, plan section 4.6).

A typed line is evidence, not an instruction. This module extracts a typed candidate
claim from what the user said plus the decision they were looking at, echoes one plain
line naming the action, the scope and the start point, and stores nothing until the user
confirms. It is a parser, not an authority: it cannot grant anything, and the safety
floor still decides what may run, so a confirmed claim is a preference the learner may
act on later and never a permission.

The plan's five steps are the shape of this file: extract a candidate under a strict
schema (an action no tool holds is refused, not recorded), resolve scope from nouns -
an address the line names, a class word the classifier already reads, a topic word from
the mail itself, a deictic word, and only then the active item - echo the reading, ask
one bounded question when a load-bearing slot is unresolved, and store on confirmation.

Nothing is inferred about the user: scope comes from what they said and which mail they
were looking at, never from who they appear to be, which is what keeps inferred sensitive
attributes out of memory by construction rather than by a filter.

What a reading is worth keeping is not decided here: a confirmed claim goes to
``agent.memory``, which carries the schema it has to satisfy and the consent it needs
before anything is kept at all.
"""
import re
from dataclasses import dataclass, replace
from datetime import UTC, datetime
from typing import Any

from agent.events import FeedbackKind, is_learnable
from agent.memory.claims import Claim, ClaimScope, ClaimType, ScopeAnchor, claim_id_for
from agent.safety.floor import Route
from agent.tools.email_tools import ACTION_TO_TOOL
from agent.triage import intents_matching


@dataclass(frozen=True)
class FeedbackContext:
    """The decision the user was looking at. The mail, never the dataset's labels."""

    case_id: str
    sender: str
    intent: str
    relationship_class: str
    route: Route
    action_id: str
    subject: str = ""
    # The source a claim has to be able to name. A rule typed with no mail in front of
    # the user has no source, and the schema will not keep it.
    message_id: str = ""

    @property
    def domain(self) -> str:
        """The sender's domain, which is the widest sender-shaped scope."""
        return self.sender.rsplit("@", 1)[1].lower() if "@" in self.sender else ""


@dataclass(frozen=True)
class Reading:
    """What one typed line means, and the one line the user is asked back."""

    kind: FeedbackKind
    echo: str
    claim: Claim | None = None
    prompt: str | None = None

    @property
    def explicit_for_learning(self) -> bool:
        """Whether a learner may use this, which is the kind's own rule."""
        return is_learnable(self.kind)

    @property
    def stores(self) -> bool:
        """Whether this reading would put a claim in memory once confirmed."""
        return self.claim is not None


# ---------------------------------------------------------------- how the user talks

# A policy statement, as opposed to a decision about the mail in front of them. Checked
# first: "no, don't ever notify me about promotions" is a rule, not a rejection.
_POLICY = re.compile(
    r"\b(never|always|whenever|from now on|every time|ignore|stop (sending|telling|notifying)"
    r"|no (more )?notifications?|don'?t (ever )?(notify|tell|show|send)|unsubscribe me from)\b",
    re.IGNORECASE,
)
_CORRECTION = re.compile(
    r"\b(actually|instead|rather than|that'?s wrong|should (be|have been)|mis-?read|"
    r"not .{0,25} but )\b",
    re.IGNORECASE,
)
_APPROVE = re.compile(
    r"^(yes|y|yep|yeah|ok|okay|sure|right|correct|confirm(ed)?|approve[d]?|go ahead|do it"
    r"|send it|that'?s right|sounds good)\b",
    re.IGNORECASE,
)
_REJECT = re.compile(r"^(no|nope|nah|reject(ed)?|cancel|hold off|don'?t|do not|stop)\b", re.IGNORECASE)
_NEVER = re.compile(r"\b(never|ignore|stop|don'?t|no (more )?)\b", re.IGNORECASE)

# What to do about the mail, in the pipeline's own action vocabulary. A request for an
# action nothing implements is refused below rather than recorded as a preference.
_SILENCE = re.compile(
    r"\b(ignore|silently|silence|suppress|quiet|no notifications?|don'?t notify|do not notify"
    r"|stop (telling|notifying|sending)|not (tell|notify) me)\b",
    re.IGNORECASE,
)
_NOTIFY = re.compile(r"\b(notify me|tell me|let me know|alert me|ping me|keep me posted)\b", re.IGNORECASE)
_ASK = re.compile(
    r"\b(ask me first|check with me|draft (a )?(reply|response)|prepare (a )?(reply|draft)"
    r"|pre-?draft)\b",
    re.IGNORECASE,
)
_ESCALATE = re.compile(
    r"\b(escalate|leave (it|them) (to|for) me|hand (it|them) (to|over to) me|always ask)\b",
    re.IGNORECASE,
)
# "ignore these" is both: the user does not want to see them and does not want them in
# the way, which is the reading the plan's own worked echo uses. "don't notify me" is
# only the first half - the mail is still handled, just not announced.
_IGNORE = re.compile(r"\b(ignore|ignored|bin|trash|get rid of|out of the way)\b", re.IGNORECASE)
_ARCHIVE = re.compile(r"\b(archive|archived|file (it|them|away))\b", re.IGNORECASE)
_LABEL_AS = re.compile(
    r"\b(?:label|tag|file)\b[^.]*?\b(?:as|into|under)\s+[\"']?([^\"'\n,.;]{2,40})", re.IGNORECASE
)
# Actions a well-meaning sentence asks for that no tool holds. §4.6 rejects these
# rather than recording a preference the agent cannot keep.
_UNSUPPORTED = re.compile(
    r"\b(delete|erase|purge|pay|wire|transfer|forward (it|them|this)|disclose|share the key)\b",
    re.IGNORECASE,
)

# Scope words: an address or a topic the mail itself mentions narrows without a guess.
_ADDRESS = re.compile(r"\b[\w.+-]+@[\w.-]+\.[a-z]{2,}\b", re.IGNORECASE)
_DEICTIC = re.compile(r"\b(this|that|these|those|it|them|the sender)\b", re.IGNORECASE)
_EVERYTHING = re.compile(r"\b(everything|anything|all mail|all of it|every arrival|the whole inbox)\b", re.IGNORECASE)
_GLOBAL_ANSWER = re.compile(
    r"\b(whole inbox|everything|all (of it|mail|future mail|future arrivals)|every future arrival)\b",
    re.IGNORECASE,
)
_LOCAL_ANSWER = re.compile(r"\b(just|only) (this|that|these|the sender)\b|\bthis (sender|one)\b", re.IGNORECASE)
# The user naming the sender rather than the class of mail. Scope is matched closest
# first, so this is the only path that pins a rule to one address on the mail's behalf.
_SENDER_DEICTIC = re.compile(
    r"\b(this|that|the) sender\b|\bfrom (this|that|them|him|her|these people)\b",
    re.IGNORECASE,
)

_WORD = re.compile(r"[a-z][a-z0-9/-]{2,}")
_STOP = frozenset(
    {
        "about", "always", "again", "also", "archive", "because", "being", "could", "email",
        "emails", "every", "from", "future", "have", "into", "just", "keep", "know", "label",
        "like", "mail", "mails", "make", "more", "never", "notify", "only", "please", "should",
        "stop", "sure", "that", "their", "them", "then", "there", "these", "they", "this",
        "those", "want", "well", "what", "when", "will", "with", "would", "your",
    }
)


def read_feedback(
    text: str,
    *,
    context: FeedbackContext | None = None,
    recorded_at: datetime | None = None,
) -> Reading:
    """Read one typed line against the decision it followed. Store nothing."""
    quote = " ".join(text.split())
    if not quote:
        return _nothing("I did not catch that; nothing was stored.")

    refused = _UNSUPPORTED.search(quote)
    if refused:
        return _nothing(
            f"I cannot do that: '{refused.group(0)}' is not an action I hold, so nothing "
            f"was stored. What I can do is label, archive, draft, notify or read."
        )

    # A correction is checked before a policy statement: "actually that sender is a
    # spoof, always escalate them" is the user fixing a reading, and the rule it states
    # is part of that correction rather than a fresh preference.
    if _CORRECTION.search(quote):
        return _claim_reading(quote, context, recorded_at, kind_hint=False, corrected=True)
    if _POLICY.search(quote):
        return _claim_reading(quote, context, recorded_at, kind_hint=_NEVER.search(quote) is not None)
    if _APPROVE.match(quote):
        return _decision_reading(FeedbackKind.APPROVE, quote, context)
    if _REJECT.match(quote):
        return _decision_reading(FeedbackKind.REJECT, quote, context)

    return _nothing(f"I did not understand {quote!r}; nothing was stored.")


def confirm_claim(
    claim: Claim | None,
    answer: str,
    *,
    context: FeedbackContext | None = None,
    recorded_at: datetime | None = None,
) -> Claim | None:
    """Read the user's answer to the scope echo: the claim to store, or None for no."""
    if claim is None:
        return None
    reply = " ".join(answer.split())
    if not reply:
        return None
    if _GLOBAL_ANSWER.search(reply):
        # The user chose the whole mailbox. That is the one reading the parser will not
        # assume, so it is only ever stored because it was said out loud.
        return replace(
            claim,
            scope=ClaimScope(),
            scope_anchor=ScopeAnchor.GLOBAL,
            confidence=1.0,
            quote=f"{claim.quote} | {reply}",
        )
    if _LOCAL_ANSWER.search(reply):
        return replace(claim, quote=f"{claim.quote} | {reply}")
    verdict = confirm_words(reply)
    if verdict is True:
        return claim
    if verdict is False:
        return None
    return _narrowed(claim, reply, context)


def _narrowed(
    claim: Claim, reply: str, context: FeedbackContext | None
) -> Claim | None:
    """The claim with the scope the answer named, or None when it named none."""
    scope, anchor, confidence = _scope_for(reply, context)
    if not scope.resolved:
        return None
    return replace(
        claim,
        scope=scope,
        scope_anchor=anchor,
        confidence=min(confidence, 0.9),
        quote=f"{claim.quote} | {reply}",
    )


def confirm_words(text: str) -> bool | None:
    """Whether a line confirms (True), refuses (False), or says something else (None)."""
    reply = " ".join(text.split())
    if not reply:
        return None
    if _REJECT.match(reply):
        return False
    if _APPROVE.match(reply):
        return True
    return None


# ---------------------------------------------------------------- the five steps


def _claim_reading(
    quote: str,
    context: FeedbackContext | None,
    recorded_at: datetime | None,
    *,
    kind_hint: bool,
    corrected: bool = False,
) -> Reading:
    """Extract a candidate claim, echo it, and ask the one bounded question."""
    route, action_id, params, unheld = _action_for(quote, context)
    scope, anchor, confident = _scope_for(quote, context)
    unresolved = route is None and action_id is None

    if unheld is not None:
        return _nothing(
            f"I cannot do that: {unheld} is not an action I hold, so nothing was stored."
        )

    if context is None or not context.message_id:
        # A rule has to be able to name the mail it came from, so a line typed with no
        # decision in front of the user is heard and not kept.
        return _nothing(f"Noted: {quote!r}. Nothing was stored: a rule needs the mail it came from.")

    if not scope.resolved:
        # The line names an action and no scope at all. The narrow reading tied to the mail
        # in front of the user is offered - at the confidence that makes the echo ask
        # whether it was meant more widely - and stored only once that is confirmed. It is
        # never assumed: the schema refuses a rule about the whole mailbox nobody said.
        narrow = _from_context(context)
        if not narrow.resolved:
            return _nothing(
                f"Noted: {quote!r}. Nothing was stored: which mail this applies to is not "
                "settled yet."
            )
        scope, anchor, confident = narrow, ScopeAnchor.CONTEXT, 0.6

    claim = Claim(
        claim_id=claim_id_for(quote, route, action_id, params, scope),
        type=ClaimType.CORRECTION
        if corrected
        else (ClaimType.BOUNDARY if kind_hint else ClaimType.PREFERENCE),
        quote=quote,
        scope=scope,
        scope_anchor=anchor,
        route=route,
        action_id=action_id,
        params=params,
        source_case_id=context.case_id,
        source_message_id=context.message_id,
        starts_after_case_id=context.case_id,
        recorded_at=recorded_at or datetime.now(UTC),
        confidence=confident if not unresolved else min(confident, 0.3),
    )
    kind = (
        FeedbackKind.CHANGE_TIER
        if corrected
        else (FeedbackKind.NEVER_DO_THIS if kind_hint else FeedbackKind.ALWAYS_DO_THIS)
    )
    return Reading(
        kind=kind,
        echo=f"Got it: {claim.describe()}",
        claim=claim,
        prompt=_question(claim, unresolved=unresolved),
    )


def _decision_reading(kind: FeedbackKind, quote: str, context: FeedbackContext | None) -> Reading:
    """A plain yes or no about the decision that was waiting. No claim, no scope."""
    what = context.case_id if context else "that decision"
    said = "you approved" if kind is FeedbackKind.APPROVE else "you rejected"
    return Reading(kind=kind, echo=f"Noted: {said} {what}. Nothing was stored as a rule.")


def _nothing(echo: str) -> Reading:
    """A line that teaches nothing, recorded as such."""
    return Reading(kind=FeedbackKind.NONE, echo=echo)


def _action_for(
    quote: str, context: FeedbackContext | None
) -> tuple[Route | None, str | None, dict[str, Any], str | None]:
    """The route and action the user asked for, or nothing when they named neither."""
    label = _LABEL_AS.search(quote)
    if label:
        name = _clean_label(label.group(1))
        if name:
            action_id = "email.apply_label"
            if ACTION_TO_TOOL.get(action_id) is None:
                return None, None, {}, action_id
            return Route.PROCEED_AND_NOTIFY, action_id, {"label": name}, None

    ignored = bool(_IGNORE.search(quote))
    action_id = "email.archive" if (ignored or _ARCHIVE.search(quote)) else None
    if action_id is not None and ACTION_TO_TOOL.get(action_id) is None:
        return None, None, {}, action_id

    if _ESCALATE.search(quote):
        return Route.ESCALATE, None, {}, None
    if _ASK.search(quote):
        # Asking first means a draft to ask about - that is the route's own name, and what
        # its echo already promises - so a reading that names no action still names the work.
        # A claim left actionless arrives at the floor as an unrecognized tool, which
        # escalates the very mail the user asked to see drafted.
        return Route.ASK_FIRST_WITH_PREDRAFT, action_id or "email.create_draft", {}, None
    if _SILENCE.search(quote) or ignored:
        return Route.PROCEED_SILENTLY, action_id, {}, None
    if _NOTIFY.search(quote):
        return Route.PROCEED_AND_NOTIFY, action_id, {}, None
    # An action with no route word is a claim about the work, not about telling.
    return None, action_id, {}, None


def _clean_label(candidate: str) -> str:
    """A folder name as the user wrote it, without the sentence around it."""
    name = candidate.strip().strip("\"',.;")
    return " ".join(name.split())[:60]


def _scope_for(
    quote: str, context: FeedbackContext | None
) -> tuple[ClaimScope, ScopeAnchor, float]:
    """Resolve the scope from nouns first, and only then from the active item."""
    address = _ADDRESS.search(quote)
    if address:
        return ClaimScope(sender=address.group(0).lower()), ScopeAnchor.EXPLICIT, 1.0

    named = intents_matching(quote)
    if len(named) == 1:
        return ClaimScope(intent=named[0]), ScopeAnchor.INTENT, 0.9
    if len(named) > 1:
        # Several classes matched, so the narrower reading is one of them and the echo
        # has to be confirmed before any of them is a rule.
        return ClaimScope(intent=named[0]), ScopeAnchor.INTENT, 0.6

    if context is not None and _SENDER_DEICTIC.search(quote):
        return ClaimScope(sender=context.sender), ScopeAnchor.CONTEXT, 0.9

    if context is not None:
        topic = _topic_overlap(quote, context.subject)
        if topic:
            return _from_context(context), ScopeAnchor.CONTEXT, 0.8
        if _DEICTIC.search(quote):
            return _from_context(context), ScopeAnchor.CONTEXT, 0.9

    if context is not None and _EVERYTHING.search(quote):
        # The plan's worked example: "everything" is ambiguous, so the narrow reading
        # tied to the active item is offered - and asked about - rather than stored.
        return _from_context(context), ScopeAnchor.CONTEXT, 0.6

    return ClaimScope(), ScopeAnchor.UNRESOLVED, 0.3


def _from_context(context: FeedbackContext) -> ClaimScope:
    """The narrow reading tied to the mail in front of the user.

    The class of mail, not the address that sent it: a person correcting one mail means
    "mail like this", and a rule that carries the address covers that one address and
    nothing else, which is how one correction about a recruiter failed to cover the next
    recruiter. The address is kept only when the mail's class is unknown, where there is
    nothing wider to name.
    """
    if context.intent:
        return ClaimScope(intent=context.intent)
    return ClaimScope(sender=context.sender)


def _topic_overlap(quote: str, subject: str) -> set[str]:
    """Words the user used that also appear in the mail they were looking at."""
    return set(_words(quote)) & set(_words(subject))


def _words(text: str) -> tuple[str, ...]:
    return tuple(word for word in _WORD.findall(text.lower()) if word not in _STOP)


def _question(claim: Claim, *, unresolved: bool) -> str:
    """The one bounded question: about the slot that is missing, never about everything."""
    if unresolved:
        return (
            "What should I do with them: archive them, or leave them and stop telling you? "
            "(say 'archive' or 'stop telling me')"
        )
    if not claim.scope.resolved:
        return (
            "Which mail did you mean: everything from now on, or one sender or class? "
            "(say 'the whole inbox' or name one)"
        )
    if claim.scope_anchor is ScopeAnchor.CONTEXT and claim.confidence < 0.8:
        return "Is that what you meant, or is it every future arrival? (yes / the whole inbox)"
    return "Storing that as a rule - is it right? (yes / no)"


__all__ = [
    "FeedbackContext",
    "Reading",
    "confirm_claim",
    "confirm_words",
    "read_feedback",
]
