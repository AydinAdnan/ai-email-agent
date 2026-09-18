"""Decision sources for the simulator (Phase 3.4, router wired in at 6.5).

Two sources exist, and the difference between them is the point:

- ``ProposalPolicy`` is the pipeline. It reads the mail, has the triage step infer
  intent and relationship, gets a proposal (rules today, a model when one is
  configured), and hands the floor's ballot to the constrained router. It never reads
  the dataset's answer.
- ``GoldPolicy`` is the reference. It reads the dataset's route off the case and
  intersects it with the same floor mask, which is useful for reproducing the plan's
  checks and for scoring, and useless as a measure of the pipeline.

Both obey the same rule: the floor always wins. A masked route falls back to the
least autonomous route that survives, and a case the floor fences escalates no matter
what either source wanted. A caller with no router running gets that fallback alone,
which is the answer a probe wants: the floor's, without the learner's opinion.
"""
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from agent.autonomy.confidence import Bucket
from agent.autonomy.preferences import RememberedProvider
from agent.autonomy.router import Router, Routing, RoutingRequest, mail_risk
from agent.dataset import Case
from agent.drafts import DRAFTING_TOOLS, Drafting, Predraft, drafting_for
from agent.events import Message
from agent.gateway import (
    NO_ACTION_TOOL,
    Proposal,
    ProposalError,
    ProposalGateway,
    ProposalProvider,
    RuleProvider,
    persona_demanded_route,
)
from agent.safety.floor import (
    ALL_ROUTES,
    ActionClass,
    ActionPayload,
    EmailContext,
    Route,
    SafetyVerdict,
    floor_check,
)
from agent.tools.email_tools import tool_for_action
from agent.triage import Triage, triage

# The routes that stop the simulator and wait for the user.
INTERRUPTING_ROUTES: frozenset[Route] = frozenset(
    {Route.ASK_FIRST_WITH_PREDRAFT, Route.ESCALATE}
)


@dataclass(frozen=True)
class Decision:
    """What the simulator does with one arrival."""

    case_id: str
    route: Route
    action_id: str
    tool_name: str
    params: Mapping[str, Any]
    # The address the decision is about, so a correction saying "this sender" has
    # something to bind to.
    sender: str
    reason: str
    verdict: SafetyVerdict
    source: str
    hints: Triage | None = None
    # What the router considered, when one is running: the ballot, the posteriors, and the
    # cost of every alternative. None for a reference decision, which does not route.
    routing: Routing | None = None
    # The predraft this decision wrote, if its action is one that drafts: what it read,
    # what it says, and whether it may be shown. Kept even when it was withheld, so the
    # reason survives into the trace.
    drafting: Drafting | None = None

    @property
    def interrupts(self) -> bool:
        """Whether this route has to wait for the user."""
        return self.route in INTERRUPTING_ROUTES

    @property
    def predraft(self) -> Predraft | None:
        """The draft this ask shows, or None when it shows none."""
        if self.drafting is None or not self.drafting.ok:
            return None
        return self.drafting.draft if self.route is Route.ASK_FIRST_WITH_PREDRAFT else None


def email_context_for(case: Case) -> EmailContext:
    """Build the floor's view of a case from its canonical event."""
    message = case.event.message
    user_domain = message.recipients[0].split("@")[-1] if message.recipients else ""
    return EmailContext(
        email_id=case.case_id,
        sender=message.sender.email,
        recipients=message.recipients,
        subject=message.subject,
        body=message.body,
        display_name=message.sender.display_name,
        user_domain=user_domain,
    )


def floor_verdict_for(case: Case) -> tuple[SafetyVerdict, str, str]:
    """Return the floor verdict, the dataset action id and the tool name it mapped to."""
    action_id = str(case.row["canonical_candidate_action"]["action_id"])
    tool_name = tool_for_action(action_id)
    params = dict(case.row["canonical_candidate_action"].get("arguments") or {})
    action = ActionPayload(tool_name=tool_name, params=_params_with_case(params, case))
    return floor_check(action, email=email_context_for(case)), action_id, tool_name


def _params_with_case(params: dict[str, Any], case: Case) -> dict[str, Any]:
    """Give the action the ids the floor needs to resolve recipients and targets."""
    enriched = dict(params)
    enriched.setdefault("email_id", case.event.message.message_id)
    enriched.setdefault("thread_id", case.event.thread.thread_id)
    return enriched


def quietenable(case: Case) -> bool:
    """Whether a rule the user could state would take this mail off their screen.

    Asked by putting the quietest proposal a rule can amount to - silently archive this
    mail - through the same persona rules and floor a real proposal goes through. A mail
    the persona has already demanded escalation for is not one any rule can quieten, and
    saying so at the prompt is what stops a user from typing rules that cannot help.
    """
    message = case.event.message
    hints = triage(message)
    if persona_demanded_route(message, hints) is Route.ESCALATE:
        return False
    proposal = Proposal(
        route=Route.PROCEED_SILENTLY,
        action_id="email.archive",
        tool_name=tool_for_action("email.archive"),
        params={},
        rationale="",
        confidence=1.0,
    )
    return not route_decision(case, hints, proposal, "", source="probe").interrupts


def named_route(provider: ProposalProvider, message: Message, hints: Triage) -> Route | None:
    """The route the user's own rules name for this mail, if any.

    Two sources count: a confirmed claim the memory layer answered from, which is the
    user's own words, and the reference persona's standing rules, which is what they said
    before any claim existed. A model's answer is neither - it is the thing the router is
    there to test - so an untrusted proposal buys no autonomy on its own.
    """
    if isinstance(provider, RememberedProvider):
        remembered = provider.proposal_for(message, hints)
        if remembered is not None:
            return remembered.route
    standing = RuleProvider().build(message, hints)
    value = standing.get("route")
    return Route(value) if value else None


def routing_request(
    case: Case,
    hints: Triage,
    proposal: Proposal | None,
    verdict: SafetyVerdict,
    *,
    named: Route | None,
) -> RoutingRequest:
    """Everything the router may consider about one arrival, and nothing else."""
    message = case.event.message
    proposed = proposal.action_id if proposal is not None and proposal.action_id else None
    return RoutingRequest(
        case_id=case.case_id,
        allowed=tuple(verdict.allowed_routes),
        bucket=Bucket(
            sender=message.sender.email,
            intent=hints.intent,
            action=proposed or NO_ACTION_TOOL,
        ),
        risk=mail_risk(
            confidence=hints.confidence,
            # Acting at somebody else is only reachable where the action class says the
            # effect addresses a third party at all - an internal send, or a deletion.
            addresses_others=verdict.action_class is ActionClass.IRREVERSIBLE_INTERNAL,
            ignorable=named is Route.PROCEED_SILENTLY,
        ),
        named=named,
    )


def strictest_allowed(verdict: SafetyVerdict) -> Route:
    """The least autonomous route the floor left open, which is the fail-closed one."""
    allowed = [route for route in ALL_ROUTES if route in verdict.allowed_routes]
    return allowed[-1] if allowed else Route.ESCALATE


def route_decision(
    case: Case,
    hints: Triage,
    proposal: Proposal | None,
    reason: str,
    *,
    source: str,
    router: Router | None = None,
    provider: ProposalProvider | None = None,
) -> Decision:
    """Apply the floor to a proposal, then the router where a run is learning.

    One implementation for every caller: the reference policy here, the graph's nodes and
    the simulator. ``router=None`` answers the floor's question alone - what a probe such
    as ``quietenable`` is asking - and skips the learner's opinion entirely.
    """
    tool_name = proposal.tool_name if proposal is not None else None
    params = dict(proposal.params) if proposal is not None else {}
    payload = ActionPayload(
        tool_name=tool_name or NO_ACTION_TOOL,
        params=_params_with_case(params, case),
    )
    # The floor judges the action as proposed. The predraft is the *content* of an ask, so
    # its own words stay out of this payload: a draft quoting an invoice would otherwise
    # change the action's class and escalate the very mail it was written to answer.
    verdict = floor_check(payload, email=email_context_for(case))
    drafting = drafting_for(case, intent=hints.intent) if tool_name in DRAFTING_TOOLS else None
    routing: Routing | None = None
    if router is not None:
        named = named_route(provider, case.event.message, hints) if provider is not None else None
        routing = router.route(routing_request(case, hints, proposal, verdict, named=named))
        route = routing.route
        reason = f"{reason} | {routing.describe()}"
    else:
        wanted = proposal.route if proposal is not None else Route.ESCALATE
        if wanted in verdict.allowed_routes:
            route = wanted
            if proposal is not None and verdict.rule_id is not None:
                reason = f"{reason}; floor allowed it ({verdict.rule_id})"
        else:
            route = strictest_allowed(verdict)
            reason = f"floor masked {wanted.value} ({verdict.rule_id}), falling back to {route.value}"
    if route is Route.ASK_FIRST_WITH_PREDRAFT and drafting is not None:
        if drafting.ok:
            # The ask carries the draft: same action, with the reply already written and
            # addressed to whoever wrote.
            params = {**params, **drafting.draft.params()}
        else:
            # Nothing to ask with is not a licence to ask anyway: a reply the user cannot
            # trust is worse than a mail handed back, which is what escalating is.
            route = Route.ESCALATE
            reason = f"{reason}; {drafting.validation.code}: {drafting.validation.detail}"
    return Decision(
        case_id=case.case_id,
        route=route,
        action_id=proposal.action_id if (proposal and proposal.action_id) else NO_ACTION_TOOL,
        tool_name=tool_name or NO_ACTION_TOOL,
        params=params,
        sender=case.event.message.sender.email,
        reason=reason,
        verdict=verdict,
        source=source,
        hints=hints,
        routing=routing,
        drafting=drafting,
    )


class ProposalPolicy:
    """Decide from the pipeline: mail in, triage, proposal, floor, router, route out."""

    source = "proposal"

    def __init__(
        self,
        gateway: ProposalGateway | None = None,
        *,
        known_senders: dict[str, str] | None = None,
        router: Router | None = None,
    ) -> None:
        self.gateway = gateway if gateway is not None else ProposalGateway(RuleProvider())
        self.known_senders = known_senders or {}
        self.router = router

    async def decide(self, case: Case, *, router: Router | None = None) -> Decision:
        running = router if router is not None else self.router
        message = case.event.message
        hints = triage(message, known_senders=self.known_senders)
        try:
            proposal = await self.gateway.propose(message, hints)
        except ProposalError as error:
            # No usable proposal is not a licence to guess; it is a reason to escalate.
            return self._decision(case, hints, None, f"no usable proposal: {error}", running)
        return self._decision(case, hints, proposal, proposal.rationale, running)

    def _decision(
        self,
        case: Case,
        hints: Triage,
        proposal: Proposal | None,
        reason: str,
        router: Router | None,
    ) -> Decision:
        return route_decision(
            case,
            hints,
            proposal,
            reason,
            source=self.source,
            router=router,
            provider=self.gateway.provider,
        )


class GoldPolicy:
    """Choose the dataset's route when the floor still allows it, else escalate.

    The reference, not the pipeline: read the labels a case carries, and use them for
    scoring and for reproducing the plan's checks.
    """

    source = "labels"

    async def decide(self, case: Case, *, router: Router | None = None) -> Decision:
        # The reference predates the router and is not routed by it: it reads the answer off
        # the case, which is the point of keeping it as a measure of the pipeline.
        del router
        verdict, action_id, tool_name = floor_verdict_for(case)
        gold = Route(case.labels.autonomy_outcome)

        if gold in verdict.allowed_routes:
            route = gold
            reason = f"gold route survives the floor ({verdict.rule_id or 'no rule fired'})"
        else:
            route = Route.ESCALATE
            reason = f"floor masked the gold route ({verdict.rule_id})"

        return Decision(
            case_id=case.case_id,
            route=route,
            action_id=action_id,
            tool_name=tool_name,
            params=dict(case.row["canonical_candidate_action"].get("arguments") or {}),
            sender=case.event.message.sender.email,
            reason=reason,
            verdict=verdict,
            source=self.source,
        )


__all__ = [
    "INTERRUPTING_ROUTES",
    "Decision",
    "Drafting",
    "GoldPolicy",
    "ProposalPolicy",
    "email_context_for",
    "floor_verdict_for",
    "named_route",
    "quietenable",
    "route_decision",
    "routing_request",
    "strictest_allowed",
]
