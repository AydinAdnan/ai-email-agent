from __future__ import annotations

from agent.autonomy.confidence import REVERT_WEIGHT, BetaStore, Bucket
from agent.events import FeedbackEvent, FeedbackKind, is_learnable
from agent.memory.claims import Claim, ClaimScope
from agent.safety.floor import Route

# A route that leaves the user out of it is a vote for the agent handling mail like this on
# its own; a route that keeps them in it is a vote against. So the direction a reading counts
# in comes from the route it chose rather than from the words that chose it - "never tell me
# about these" reads like a refusal and is an approval of the work it names.
AUTONOMOUS_ROUTES = frozenset({Route.PROCEED_SILENTLY, Route.PROCEED_AND_NOTIFY})

# How each kind of explicit feedback points when the reading named no route at all.
APPROVING_KINDS = frozenset(
    {FeedbackKind.APPROVE, FeedbackKind.ALWAYS_DO_THIS, FeedbackKind.EDIT_DRAFT}
)

# Undoing the agent's work points against it whatever route that work was, so these kinds
# decide the direction on their own and a named route does not flip them.
DISAPPROVING_KINDS = frozenset({FeedbackKind.REJECT, FeedbackKind.REVERT})


def is_approving(event: FeedbackEvent) -> bool:
    """Whether this reading is a vote for the agent acting on its own.

    The route a reading names is the route the agent had chosen, so the direction comes
    from what the user did to it: an approval keeps that work, and a revert or a
    rejection undoes it. A revert of an autonomous action is therefore a vote against
    autonomy, which is the reading it would get backwards if the kind were ignored.

    Shared with the router, which adapts a bucket's cutoffs on the same reading rather than
    deciding a second time what the user meant.
    """
    if event.kind in DISAPPROVING_KINDS:
        return False
    if event.chosen_route is not None:
        return event.chosen_route in AUTONOMOUS_ROUTES
    return event.kind in APPROVING_KINDS


class Learner:
    """Counts what the user said into posteriors, once per event, never from silence.

    Every update is keyed by the feedback event's id, so a replayed run - or a resumed
    decision delivering the same approval twice - changes nothing the second time. Silence
    and the user's own replies are not decisions and never reach here: the event schema
    marks them unlearnable, and this refuses them again rather than trusting the caller.

    A reading that named a route counts by that route. One that named only work blocks that
    arm outright, which is a rule the router has to obey rather than a count it weighs.
    """

    def __init__(self, store: BetaStore | None = None) -> None:
        self.store = store if store is not None else BetaStore()
        # The arms a confirmed rule has refused, keyed by the claim that refused them.
        self.blocks: dict[str, tuple[ClaimScope, str]] = {}
        self.seen: set[str] = set()
        self.applied = 0
        self.ignored = 0

    def observe(
        self, event: FeedbackEvent, bucket: Bucket, *, claim: Claim | None = None
    ) -> bool:
        """Count one explicit decision about one bucket, at most once. False if uncounted."""
        if event.event_id in self.seen or not is_learnable(event.kind):
            self.ignored += 1
            return False
        self.seen.add(event.event_id)
        if event.kind is FeedbackKind.NEVER_DO_THIS and event.chosen_route is None:
            # A refusal of the work rather than a choice about telling: "never archive my
            # receipts" names no route, so there is nothing to count and an arm to refuse.
            self._refuse(event, bucket, claim)
        else:
            self.store.record(
                bucket,
                approved=self._approved(event),
                weight=REVERT_WEIGHT if event.kind is FeedbackKind.REVERT else 1.0,
            )
        self.applied += 1
        return True

    def refuses(self, bucket: Bucket) -> str:
        """The confirmed rule that refused this arm, or '' when the user has not refused it.

        A rule scoped to a sender refuses the arm for that sender; one scoped to an intent
        refuses it for every mail of that intent, which is the difference between "never
        archive these" said about one correspondent and said about a class of mail.
        """
        domain = bucket.sender.rsplit("@", 1)[-1].lower() if "@" in bucket.sender else ""
        for claim_id, (scope, action) in self.blocks.items():
            if action and action != bucket.action:
                continue
            if scope.sender and scope.sender.lower() != bucket.sender.lower():
                continue
            if scope.domain and scope.domain.lower() != domain:
                continue
            if scope.intent and scope.intent.lower() != bucket.intent.lower():
                continue
            return claim_id
        return ""

    @property
    def updates(self) -> int:
        """How many explicit decisions have been counted into a posterior."""
        return self.applied

    @property
    def refusals(self) -> int:
        """How many arms the user has refused outright."""
        return len(self.blocks)

    def _approved(self, event: FeedbackEvent) -> bool:
        """Whether this reading is a vote for the agent acting on its own."""
        return is_approving(event)

    def _refuse(self, event: FeedbackEvent, bucket: Bucket, claim: Claim | None) -> None:
        """Keep the refusal, with the scope the rule was confirmed for rather than this mail's."""
        if not event.chosen_action_id:
            return
        scope = claim.scope if claim is not None else ClaimScope(
            sender=bucket.sender, intent=bucket.intent
        )
        name = claim.claim_id if claim is not None else f"never {event.chosen_action_id}"
        self.blocks[name] = (scope, event.chosen_action_id)


__all__ = [
    "APPROVING_KINDS",
    "AUTONOMOUS_ROUTES",
    "DISAPPROVING_KINDS",
    "Learner",
    "is_approving",
]
