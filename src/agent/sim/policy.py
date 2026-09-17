"""Decision sources for the simulator (Phase 3.4).

The router does not exist until Commit 6.5, so something has to decide each arrival
for the run to block in the right places. Two sources exist, and the difference between
them is the point:

- ``ProposalPolicy`` is the pipeline. It reads the mail, has the triage step infer
  intent and relationship, gets a proposal (rules today, a model when one is
  configured), and intersects that proposal with the routes the safety floor left
  open. It never reads the dataset's answer.
- ``GoldPolicy`` is the reference. It reads the dataset's route off the case and
  intersects it with the same floor mask, which is useful for reproducing the plan's
  checks and for scoring, and useless as a measure of the pipeline.

Both obey the same rule: the floor always wins. A masked route falls back to the
least autonomous route that survives, and a case the floor fences escalates no matter
what either source wanted.
"""
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from agent.dataset import Case
from agent.gateway import NO_ACTION_TOOL, Proposal, ProposalError, ProposalGateway, RuleProvider
from agent.safety.floor import (
    ALL_ROUTES,
    ActionPayload,
    EmailContext,
    Route,
    SafetyVerdict,
    floor_check,
)
from agent.tools.email_tools import ACTION_TO_TOOL
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

    @property
    def interrupts(self) -> bool:
        """Whether this route has to wait for the user."""
        return self.route in INTERRUPTING_ROUTES


def tool_name_for(action_id: str) -> str:
    """Map a dataset action id to the floor's tool name, failing closed."""
    return ACTION_TO_TOOL.get(action_id, action_id)


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
    tool_name = tool_name_for(action_id)
    params = dict(case.row["canonical_candidate_action"].get("arguments") or {})
    action = ActionPayload(tool_name=tool_name, params=_params_with_case(params, case))
    return floor_check(action, email=email_context_for(case)), action_id, tool_name


def _params_with_case(params: dict[str, Any], case: Case) -> dict[str, Any]:
    """Give the action the ids the floor needs to resolve recipients and targets."""
    enriched = dict(params)
    enriched.setdefault("email_id", case.event.message.message_id)
    enriched.setdefault("thread_id", case.event.thread.thread_id)
    return enriched


def strictest_allowed(verdict: SafetyVerdict) -> Route:
    """The least autonomous route the floor left open, which is the fail-closed one."""
    allowed = [route for route in ALL_ROUTES if route in verdict.allowed_routes]
    return allowed[-1] if allowed else Route.ESCALATE


class ProposalPolicy:
    """Decide from the pipeline: mail in, triage, proposal, floor, route out."""

    source = "proposal"

    def __init__(
        self,
        gateway: ProposalGateway | None = None,
        *,
        known_senders: dict[str, str] | None = None,
    ) -> None:
        self.gateway = gateway if gateway is not None else ProposalGateway(RuleProvider())
        self.known_senders = known_senders or {}

    async def decide(self, case: Case) -> Decision:
        message = case.event.message
        hints = triage(message, known_senders=self.known_senders)
        try:
            proposal = await self.gateway.propose(message, hints)
        except ProposalError as error:
            # No usable proposal is not a licence to guess; it is a reason to escalate.
            return self._decision(case, hints, None, f"no usable proposal: {error}")
        return self._decision(case, hints, proposal, proposal.rationale)

    def _decision(
        self,
        case: Case,
        hints: Triage,
        proposal: Proposal | None,
        reason: str,
    ) -> Decision:
        tool_name = proposal.tool_name if proposal is not None else None
        payload = ActionPayload(
            tool_name=tool_name or NO_ACTION_TOOL,
            params=_params_with_case(dict(proposal.params) if proposal is not None else {}, case),
        )
        verdict = floor_check(payload, email=email_context_for(case))
        wanted = proposal.route if proposal is not None else Route.ESCALATE
        if wanted in verdict.allowed_routes:
            route = wanted
            if proposal is not None and verdict.rule_id is not None:
                reason = f"{reason}; floor allowed it ({verdict.rule_id})"
        else:
            route = strictest_allowed(verdict)
            reason = f"floor masked {wanted.value} ({verdict.rule_id}), falling back to {route.value}"
        return Decision(
            case_id=case.case_id,
            route=route,
            action_id=proposal.action_id if (proposal and proposal.action_id) else NO_ACTION_TOOL,
            tool_name=tool_name or NO_ACTION_TOOL,
            params=dict(proposal.params) if proposal is not None else {},
            sender=case.event.message.sender.email,
            reason=reason,
            verdict=verdict,
            source=self.source,
            hints=hints,
        )


class GoldPolicy:
    """Choose the dataset's route when the floor still allows it, else escalate.

    The reference, not the pipeline: read the labels a case carries, and use them for
    scoring and for reproducing the plan's checks.
    """

    source = "labels"

    async def decide(self, case: Case) -> Decision:
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
    "GoldPolicy",
    "ProposalPolicy",
    "email_context_for",
    "floor_verdict_for",
    "strictest_allowed",
    "tool_name_for",
]
