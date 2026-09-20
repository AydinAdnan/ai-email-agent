from __future__ import annotations

import json
from dataclasses import replace

from agent.events import Message
from agent.gateway import (
    NO_ACTION_TOOL,
    Proposal,
    ProposalError,
    ProposalProvider,
    ProposalRequest,
    parse_proposal,
)
from agent.memory.claims import Claim, ClaimStore
from agent.safety.floor import ALL_ROUTES, Route
from agent.tools.email_tools import tool_for_action
from agent.triage import Triage


class RememberedProvider:
    """The user's own words, consulted before the provider.

    Wraps another provider: where a confirmed claim bears on a mail, this answers with
    the claim rendered in the proposal schema, so the answer is parsed, mail-ruled and
    floor-checked exactly like a model's. Where no claim bears, the inner provider
    answers as it always did.

    A claim that names no route decides nothing here. It is something to remember, not
    something to do, and the honest place for it is the store rather than a route.
    """

    def __init__(self, store: ClaimStore, inner: ProposalProvider) -> None:
        self.store = store
        self.inner = inner
        # Which mail a rule answered, and which rule: a report has to be able to say what
        # was recalled, not only how many. Keyed by message id, valued by claim id.
        self.answered: dict[str, str] = {}

    @property
    def name(self) -> str:
        """The pair's name, so a run says where a proposal could have come from."""
        return f"{self.inner.name}+memory"

    @property
    def label(self) -> str:
        """Whichever provider actually answers, named the way a run names it."""
        return str(getattr(self.inner, "label", None) or self.inner.name)

    @property
    def recalled(self) -> int:
        """How many arrivals a confirmed claim answered."""
        return len(self.answered)

    async def complete(self, request: ProposalRequest) -> str:
        """Answer from a claim where one bears on this mail, otherwise ask the inner one."""
        claim = self.claim_for(request.message, request.hints)
        recalled = proposal_from(claim) if claim is not None else None
        if claim is None or recalled is None:
            return await self.inner.complete(request)
        if recalled.action_id is None and recalled.route is not Route.ESCALATE:
            # The rule says how much autonomy, not what the work is: the inner provider
            # still chooses the work and the claim decides who is asked about it. Without
            # this a rule that names only silence arrives at the floor as an unrecognized
            # tool, which escalates the very mail the user asked to stop hearing about.
            recalled = _with_inner_action(recalled, await self.inner.complete(request))
        self.answered[request.message.message_id] = claim.claim_id
        return json.dumps(
            {
                "route": recalled.route.value,
                "action_id": recalled.action_id,
                "params": dict(recalled.params),
                "rationale": recalled.rationale,
                "confidence": recalled.confidence,
            },
            sort_keys=True,
        )

    def claim_for(self, message: Message, hints: Triage) -> Claim | None:
        """The confirmed claim that bears on this mail and names a route, if one does.

        The narrowest one wins, and the newest one at that width: a rule about one sender
        is what the user said about that sender, so a later rule about a whole class does
        not quietly overwrite it. Among rules of the same width the newest wins, because
        that is how a person changes their mind, and two that share a moment are settled
        the cautious way, which is what the rest of the pipeline does when sources disagree.
        """
        sender = message.sender.email
        bearing = [
            claim
            for claim in self.store.matching(
                sender=sender, domain=_domain(sender), intent=hints.intent
            )
            if claim.route is not None
        ]
        if not bearing:
            return None
        width = len(bearing[0].scope.as_key())
        same_width = [claim for claim in bearing if len(claim.scope.as_key()) == width]
        return max(
            same_width, key=lambda claim: (claim.recorded_at, ALL_ROUTES.index(claim.route))
        )

    def proposal_for(self, message: Message, hints: Triage) -> Proposal | None:
        """What the user's own words amount to for this mail, if anything."""
        claim = self.claim_for(message, hints)
        return proposal_from(claim) if claim is not None else None


def _with_inner_action(recalled: Proposal, answer: str) -> Proposal:
    """The claim's route, with whatever work the inner provider chose for the mail.

    An answer that cannot be parsed, or one that names no action either, leaves the claim
    as it was: the floor then handles the actionless proposal the way it always has, which
    is to refuse it rather than to guess.
    """
    try:
        inner = parse_proposal(answer, provider="inner")
    except ProposalError:
        return recalled
    if inner.action_id is None:
        return recalled
    return replace(
        recalled,
        action_id=inner.action_id,
        tool_name=inner.tool_name,
        params=dict(inner.params),
        confidence=max(recalled.confidence, inner.confidence),
    )


def proposal_from(claim: Claim) -> Proposal | None:
    """One claim as a proposal, or None when the claim names no route."""
    if claim.route is None:
        return None
    # An escalation carries no action, and the proposal parser refuses one that does.
    action_id = None if claim.route is Route.ESCALATE else claim.action_id
    return Proposal(
        route=claim.route,
        action_id=action_id,
        tool_name=tool_for_action(action_id) if action_id else NO_ACTION_TOOL,
        params=dict(claim.params) if action_id else {},
        rationale=f"what you asked for: {claim.quote}",
        confidence=claim.confidence,
        provider="memory",
    )


def _domain(email: str) -> str:
    return email.rsplit("@", 1)[-1].lower()


__all__ = ["RememberedProvider", "proposal_from"]
