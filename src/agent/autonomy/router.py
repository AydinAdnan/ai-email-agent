from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from agent.autonomy.bandit import AUTONOMOUS_ROUTES, Learner, is_approving
from agent.autonomy.confidence import BetaStore, Bucket, Posterior
from agent.autonomy.loss import LOSS_V1, Costs, Loss, pick, score
from agent.events import FeedbackEvent, is_learnable
from agent.safety.floor import Route

# Silence needs a mean of 0.8 - the plan's pi_silent. Acting and then reporting needs less,
# because it keeps the user in the picture. tau_notify is not pinned by the plan; its worked
# example puts ASK at a mean of 0.40 and NOTIFY at 0.75, so 0.6 sits in that gap.
SILENT_CUTOFF = 0.8
NOTIFY_CUTOFF = 0.6

# An explicit approval relaxes a cutoff and a revert or rejection raises it, and the
# asymmetry is the point: trust is earned in small steps and spent in one. The floors are
# the calibration set's minimum, so no run can relax its way to "silence is always fine".
RELAX = 0.98
TIGHTEN = 0.15
MIN_SILENT = 0.55
MIN_NOTIFY = 0.35

# The outcomes a route produces by construction - it interrupts, it hands the work back, it
# reports - so only what the mail makes likely has to be estimated.
CERTAIN = ("interruption", "delay", "notified")


@dataclass(frozen=True)
class Cutoffs:
    """The posterior mean a route's bucket needs before the route may be considered."""

    silent: float = SILENT_CUTOFF
    notify: float = NOTIFY_CUTOFF

    def relax(self) -> Cutoffs:
        """After an approval: easier to earn, down to the calibration floor."""
        return Cutoffs(
            silent=max(MIN_SILENT, self.silent * RELAX),
            notify=max(MIN_NOTIFY, self.notify * RELAX),
        )

    def tighten(self) -> Cutoffs:
        """After a revert or a rejection: harder to earn, capped at certainty."""
        return Cutoffs(silent=min(1.0, self.silent + TIGHTEN), notify=min(1.0, self.notify + TIGHTEN))


class ThresholdStore:
    """Per-bucket cutoffs, adapted by explicit feedback (plan 4.3).

    Read through the same backoff chain the posteriors use, so a bucket nobody has said
    anything about inherits whatever a coarser context earned.

    ponytail: cutoffs last as long as the process and evidence does not age; the plan's
    0.99/day decay needs a clock here and a store that survives the run.
    """

    def __init__(self) -> None:
        self.cutoffs: dict[tuple[str, ...], Cutoffs] = {}

    def for_bucket(self, bucket: Bucket) -> Cutoffs:
        """The cutoffs this bucket is judged by, most specific first."""
        for level in bucket.levels():
            found = self.cutoffs.get(level)
            if found is not None:
                return found
        return Cutoffs()

    def adapt(self, bucket: Bucket, *, approved: bool) -> Cutoffs:
        """Move this bucket's cutoffs by one explicit decision."""
        level = bucket.levels()[0]
        current = self.cutoffs.get(level, Cutoffs())
        self.cutoffs[level] = current.relax() if approved else current.tighten()
        return self.cutoffs[level]


def mail_risk(*, confidence: float, addresses_others: bool, ignorable: bool) -> dict[str, float]:
    """What a mail makes likely, from signals the pipeline already computed.

    An unsure reading is likelier to be aimed wrongly. An effect that addresses somebody
    else is only reachable while acting when the action class says so - an internal send, or
    a deletion - because an external one is masked to ask or escalate. And silence withholds
    something, unless the user's own rules already classed this mail as needing no telling.
    """
    return {
        "wrong_action": max(0.0, min(1.0, 1.0 - confidence)),
        "wrong_audience": 1.0 if addresses_others else 0.0,
        "missed_notification": 0.0 if ignorable else 1.0,
    }


@dataclass(frozen=True)
class RoutingRequest:
    """Everything the router is allowed to consider for one arrival."""

    case_id: str
    allowed: tuple[Route, ...]
    bucket: Bucket
    risk: Mapping[str, float]
    # The route the user's own rules name for this mail. A model's answer is not a
    # preference, and telling them apart is what stops an untrusted proposal buying autonomy.
    named: Route | None = None


@dataclass(frozen=True)
class Routing:
    """The route chosen, and everything that was ruled out on the way."""

    case_id: str
    route: Route
    allowed: tuple[Route, ...]
    eligible: tuple[Route, ...]
    # Every eligible route with its workings, so a decision can be read back rather than
    # re-derived. This is the cost receipt the plan asks the run to persist.
    alternatives: tuple[Loss, ...]
    posterior: Posterior
    basis: str
    named: Route | None = None
    refused_by: str = ""

    @property
    def value(self) -> float:
        """The chosen route's expected loss, in handoffs."""
        return next((loss.value for loss in self.alternatives if loss.route is self.route), 0.0)

    def describe(self) -> str:
        """One line for a transcript or a reason.

        Deliberately terse: a trace digests a value of more than eight words, and the
        posteriors and the workings belong in the structured block beside this one.
        """
        return f"{self.route.value} {self.value:.2f} ({self.basis})"


class Router:
    """The constrained argmin, in the plan's fixed order.

    Floor mask, then claims, then trust, then cost: each step may only narrow the ballot, so
    the cheapest surviving route is never one the floor forbade. The route the user's own
    rules name is on the ballot before trust is earned, because they already said it;
    anybody else's answer has to wait for the posterior.
    """

    def __init__(
        self,
        learner: Learner | None = None,
        *,
        costs: Costs = LOSS_V1,
        thresholds: ThresholdStore | None = None,
    ) -> None:
        self.learner = learner
        self.store: BetaStore = learner.store if learner is not None else BetaStore()
        self.costs = costs
        self.thresholds = thresholds if thresholds is not None else ThresholdStore()
        self.routings = 0

    def route(self, request: RoutingRequest) -> Routing:
        """Choose one route for one arrival."""
        # 1. The floor's ballot. A fenced action arrives as ESCALATE alone, so this is
        #    never empty in practice; a caller that passed nothing gets the safe answer.
        allowed = request.allowed or (Route.ESCALATE,)
        basis = f"floor left {len(allowed)}/4, trust {len(allowed)}"
        refused_by = self.learner.refuses(request.bucket) if self.learner is not None else ""
        if refused_by:
            # 2. A confirmed refusal is obeyed rather than weighed: no posterior outvotes
            #    the user saying never about this arm.
            allowed = tuple(route for route in allowed if route not in AUTONOMOUS_ROUTES)
            allowed = allowed or (Route.ESCALATE,)
            basis = f"refused arm {refused_by}"
        # 3. Trust. Silence and acting without asking are earned, or named by the user.
        posterior = self.store.posterior(request.bucket)
        cutoffs = self.thresholds.for_bucket(request.bucket)
        eligible = tuple(
            route for route in allowed if self._permits(route, request, posterior, cutoffs)
        )
        if not eligible:
            # Only reachable when the claims removed everything the floor had left.
            eligible = (allowed[-1],)
            basis = "nothing left standing"
        # 4. Expected loss, in one unit, with the workings kept.
        risk = {**dict.fromkeys(CERTAIN, 1.0), **request.risk}
        losses = score(eligible, risk, self.costs)
        self.routings += 1
        return Routing(
            case_id=request.case_id,
            route=pick(losses).route,
            allowed=allowed,
            eligible=eligible,
            alternatives=losses,
            posterior=posterior,
            basis=basis if refused_by else f"floor left {len(allowed)}/4, trust {len(eligible)}",
            named=request.named,
            refused_by=refused_by,
        )

    def observe(self, event: FeedbackEvent, bucket: Bucket) -> bool:
        """Adapt one bucket's cutoffs from one explicit decision, called once per decision.

        Silence teaches nothing here either, which is why the caller only reports decisions
        the learner already counted.
        """
        if not is_learnable(event.kind):
            return False
        self.thresholds.adapt(bucket, approved=is_approving(event))
        return True

    def _permits(
        self,
        route: Route,
        request: RoutingRequest,
        posterior: Posterior,
        cutoffs: Cutoffs,
    ) -> bool:
        """Whether this route is on the ballot at all: the cautious ones always are."""
        if route not in AUTONOMOUS_ROUTES:
            return True
        if request.named is route:
            return True
        needed = cutoffs.silent if route is Route.PROCEED_SILENTLY else cutoffs.notify
        return posterior.mean >= needed


__all__ = [
    "CERTAIN",
    "MIN_NOTIFY",
    "MIN_SILENT",
    "NOTIFY_CUTOFF",
    "RELAX",
    "SILENT_CUTOFF",
    "TIGHTEN",
    "Cutoffs",
    "Router",
    "Routing",
    "RoutingRequest",
    "ThresholdStore",
    "mail_risk",
]
