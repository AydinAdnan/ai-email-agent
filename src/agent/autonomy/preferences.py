from __future__ import annotations

import json

from agent.events import Message
from agent.gateway import NO_ACTION_TOOL, Proposal, ProposalProvider, ProposalRequest
from agent.memory.claims import Claim, ClaimStore
from agent.safety.floor import Route
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
        self.answered: set[str] = set()

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
        recalled = self.proposal_for(request.message, request.hints)
        if recalled is None:
            return await self.inner.complete(request)
        self.answered.add(request.message.message_id)
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

    def proposal_for(self, message: Message, hints: Triage) -> Proposal | None:
        """What the user's own words amount to for this mail, if anything."""
        sender = message.sender.email
        for claim in self.store.matching(
            sender=sender, domain=_domain(sender), intent=hints.intent
        ):
            proposal = proposal_from(claim)
            if proposal is not None:
                return proposal
        return None


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
