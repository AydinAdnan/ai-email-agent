from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from agent.safety.floor import ALL_ROUTES, Route

# Every cost below is in the same unit: one handoff, meaning the user reads the mail,
# decides what to do, and does the work themselves. ESCALATE's own cost is the unit, so
# the table reads as "what this route costs relative to handing the mail over".
UNIT = "one handoff (the user reads the mail, decides, and does the work)"


@dataclass(frozen=True)
class Costs:
    """Versioned outcome costs, in handoffs. Changing a number means a new version.

    The outcome names are the field names on purpose: a route's outcomes are looked up on
    this table by name, so the vocabulary of outcomes and the vocabulary of costs cannot
    drift apart.
    """

    version: str
    # An effect aimed wrongly at a class the floor still allows - reversible work, undone
    # by the receipt the user reads.
    wrong_action: float
    # An effect that reached somebody it did not concern. Costs more than a wrong action,
    # because the user cannot fully undo who saw it.
    wrong_audience: float
    # The user never learned what they needed to. The largest cost here, and the whole
    # reason a verified invoice is not handled silently: the awareness has value.
    missed_notification: float
    # One bounded question, with the work already done and waiting on a yes.
    interruption: float
    # The work left the agent's queue and is waiting on the user's own.
    delay: float
    # A notification the user reads but need not answer.
    notified: float


LOSS_V1 = Costs(
    version="loss-v1",
    wrong_action=0.6,
    wrong_audience=2.0,
    missed_notification=1.4,
    interruption=0.5,
    delay=0.2,
    notified=0.1,
)

# What each route can actually produce. Silence cannot inform, so a route that reports
# nothing cannot be credited with the user knowing; and only a handoff returns the work to
# the user's own queue, which is what delay is charged for. A bounded question keeps the
# work with the agent, waiting on an answer rather than on the user's afternoon.
ROUTE_OUTCOMES: Mapping[Route, tuple[str, ...]] = {
    Route.PROCEED_SILENTLY: ("wrong_action", "wrong_audience", "missed_notification"),
    Route.PROCEED_AND_NOTIFY: ("wrong_action", "wrong_audience", "notified"),
    Route.ASK_FIRST_WITH_PREDRAFT: ("interruption",),
    Route.ESCALATE: ("interruption", "delay"),
}

# Safety is not a term in this table. Money, credentials, external sends, destructive
# deletions and injection are removed by the floor's arm masking before any arithmetic
# runs, so no cost here can promote a fenced action: the router scores only the routes the
# floor left standing.


@dataclass(frozen=True)
class Loss:
    """One route's expected loss, and the workings, which are what a receipt records."""

    route: Route
    value: float
    # (outcome, probability, cost) in the table's order, so two runs print the same line.
    terms: tuple[tuple[str, float, float], ...]

    def describe(self) -> str:
        workings = " ".join(f"{outcome} {p:.2f}x{cost:g}" for outcome, p, cost in self.terms)
        return f"{self.route} {self.value:.2f} [{workings}]"


def route_loss(route: Route, risk: Mapping[str, float], costs: Costs = LOSS_V1) -> Loss:
    """The expected loss of one route for one mail.

    ``risk`` holds the probability of each outcome the mail makes likely, so an outcome
    that is certain carries 1.0. A route reads only the outcomes it can produce, and a
    key it does not read is a probability of zero.
    """
    terms = tuple(
        (outcome, float(risk.get(outcome, 0.0)), getattr(costs, outcome))
        for outcome in ROUTE_OUTCOMES[route]
    )
    return Loss(route=route, value=sum(p * cost for _, p, cost in terms), terms=terms)


def score(
    routes: Sequence[Route], risk: Mapping[str, float], costs: Costs = LOSS_V1
) -> tuple[Loss, ...]:
    """Score the routes the floor left available, in the order the floor gave them."""
    return tuple(route_loss(route, risk, costs) for route in routes)


def pick(losses: Sequence[Loss]) -> Loss:
    """The cheapest route. Ties go to the more cautious one, so a tie never buys autonomy."""
    if not losses:
        raise ValueError("no route to choose from")
    return min(losses, key=lambda loss: (loss.value, -ALL_ROUTES.index(loss.route)))


__all__ = [
    "LOSS_V1",
    "ROUTE_OUTCOMES",
    "UNIT",
    "Costs",
    "Loss",
    "pick",
    "route_loss",
    "score",
]
