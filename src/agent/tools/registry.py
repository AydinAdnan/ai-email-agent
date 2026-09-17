"""The tool registry and the prepare/authorize/commit contract (Phase 3.3).

Every action the agent can take goes through three calls, and a real Gmail adapter
will implement the same three:

- ``prepare`` works out the steps that would run and validates their parameters. It
  mutates nothing, so a route that is never authorized leaves the mailbox exactly as
  it was.
- ``authorize`` decides whether those steps may run. It is the only gate, it reads the
  safety floor's route rather than trusting the caller, and it binds an approval to the
  *prepared action's digest* so an approval cannot be replayed onto different work.
- ``commit`` is the only thing that changes state, and it writes one receipt per
  committed action, which is what the learner and the eval will attribute feedback to.

A tool is deliberately small: ``check`` refuses parameters it cannot act on (so a bad
proposal fails before anyone is asked to approve it) and ``apply`` does the work.
"""
import hashlib
import json
from abc import ABC, abstractmethod
from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, ClassVar

from agent.safety.floor import Route

# Routes that may run without a human. Everything else has to wait.
AUTONOMOUS_ROUTES = frozenset({Route.PROCEED_SILENTLY, Route.PROCEED_AND_NOTIFY})


class ToolError(ValueError):
    """Raised when a tool is asked for something it cannot do."""


class UnknownTool(ToolError):
    """Raised when a step names a tool the registry does not hold."""


class AuthorizationRefused(RuntimeError):
    """Raised when a prepared action may not run. Carries a machine-readable code."""

    code = "AUTHORIZATION_REFUSED"


class ApprovalRequired(AuthorizationRefused):
    """Raised when the route has to wait for the user before anything is committed."""

    code = "APPROVAL_REQUIRED"


class StaleApproval(AuthorizationRefused):
    """Raised when an approval refers to different work than the action prepared."""

    code = "APPROVAL_STALE"


@dataclass(frozen=True)
class Step:
    """One tool call inside a prepared action."""

    tool: str
    params: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Effect:
    """What a committed step actually did, in one line a receipt can carry."""

    tool: str
    target: str
    detail: str


@dataclass(frozen=True)
class PreparedAction:
    """What would run, worked out without touching anything.

    ``blocked`` names steps the pipeline wanted but could not build - a draft with no
    body yet, a tool nobody holds. They are not silently dropped: the complaint travels
    on the prepared action and on the receipt, so an incomplete pipeline is visible in
    the run's own output instead of looking like a decision not to act.
    """

    case_id: str
    message_id: str
    route: Route
    action_id: str
    steps: tuple[Step, ...]
    digest: str
    blocked: tuple[str, ...] = ()

    def summary(self) -> str:
        """A short description of the steps, for a transcript or an interrupt."""
        described = "; ".join(
            f"{step.tool}({_params_brief(step.params)})" for step in self.steps
        ) or "no steps"
        if self.blocked:
            described += f"; blocked: {'; '.join(self.blocked)}"
        return described


@dataclass(frozen=True)
class Approval:
    """A user's yes, bound to the work they were shown."""

    prepared_digest: str
    approved_by: str = "user"


@dataclass(frozen=True)
class Authorization:
    """Permission for one prepared action to run, and why it was granted."""

    prepared_digest: str
    route: Route
    approved_by: str
    reason: str


@dataclass(frozen=True)
class Receipt:
    """The record of one committed action: the only thing a learner may attribute to."""

    receipt_id: str
    case_id: str
    message_id: str
    route: Route
    action_id: str
    prepared_digest: str
    effects: tuple[Effect, ...]
    committed_at: datetime
    blocked: tuple[str, ...] = ()

    def summary(self) -> str:
        """One line naming every effect, for a transcript or a summary count."""
        described = ", ".join(
            f"{effect.tool}:{effect.detail}" for effect in self.effects
        ) or "no effect"
        if self.blocked:
            described += f" | blocked: {'; '.join(self.blocked)}"
        return described


class Tool(ABC):
    """One capability. Small on purpose: check refuses, apply acts."""

    name: ClassVar[str]
    # The dataset's dotted action ids that mean this tool, the first being the one a
    # proposal is told about. The registry owns the mapping so a proposal, a reference
    # label and a real adapter all speak one vocabulary.
    action_ids: ClassVar[tuple[str, ...]] = ()
    # The arguments a proposer has to supply, as the prompt shows them. Message ids are
    # filled in by the registry, so they are not the proposer's to guess. It lives here
    # so what a model is told and what ``check`` enforces cannot drift apart.
    proposal_params: ClassVar[str] = "required: none"
    # Notifications are local to the user's own assistant; a send leaves the mailbox.
    leaves_the_mailbox: ClassVar[bool] = False

    @abstractmethod
    def check(self, params: Mapping[str, Any]) -> None:
        """Refuse parameters this tool cannot act on. Called at prepare time."""

    @abstractmethod
    def apply(self, params: Mapping[str, Any]) -> tuple[Effect, ...]:
        """Do the work and say what changed. Only ever called by a commit."""


class ToolRegistry:
    """Every tool the agent may hold, plus the three calls that gate one."""

    def __init__(self, tools: Iterable[Tool]) -> None:
        self._tools: dict[str, Tool] = {}
        for tool in tools:
            if tool.name in self._tools:
                raise ToolError(f"two tools are named {tool.name!r}")
            self._tools[tool.name] = tool

    def tool(self, name: str) -> Tool:
        """One tool by name, or a refusal naming what does exist."""
        try:
            return self._tools[name]
        except KeyError as error:
            raise UnknownTool(
                f"no tool named {name!r}; the registry holds "
                f"{', '.join(sorted(self._tools)) or 'nothing'}"
            ) from error

    @property
    def tool_names(self) -> tuple[str, ...]:
        return tuple(sorted(self._tools))

    def tool_for_action(self, action_id: str) -> str | None:
        """The tool a dataset-style action id means, or None when nothing implements it."""
        for name, tool in self._tools.items():
            if action_id in tool.action_ids:
                return name
        return None

    def prepare(
        self,
        *,
        case_id: str,
        message_id: str,
        route: Route,
        action_id: str = "unsupported",
        tool_name: str | None = None,
        params: Mapping[str, Any] | None = None,
    ) -> PreparedAction:
        """Work out the steps for a decision, validating every one, mutating nothing."""
        steps: list[Step] = []
        blocked: list[str] = []
        if route is not Route.ESCALATE and tool_name:
            # Validate the same enriched params the commit will run: checking one copy
            # and committing another is how a step passes prepare and fails at commit.
            willing = _with_context(params or {}, case_id, message_id)
            step = self._willing(tool_name, willing, blocked)
            if step is not None:
                steps.append(step)

        if route is Route.PROCEED_AND_NOTIFY and not any(
            step.tool == "notify" for step in steps
        ):
            notify_params = _with_context({"text": _notify_text(action_id)}, case_id, message_id)
            notify_step = self._willing("notify", notify_params, blocked)
            if notify_step is not None:
                steps.append(notify_step)

        frozen = tuple(steps)
        return PreparedAction(
            case_id=case_id,
            message_id=message_id,
            route=route,
            action_id=action_id,
            steps=frozen,
            digest=_digest(case_id, message_id, route, action_id, frozen, tuple(blocked)),
            blocked=tuple(blocked),
        )

    def _willing(
        self, tool_name: str, params: Mapping[str, Any], blocked: list[str]
    ) -> Step | None:
        """A step that validated, or a recorded complaint about why it could not."""
        try:
            tool = self.tool(tool_name)
            tool.check(params)
        except ToolError as error:
            blocked.append(f"{tool_name}: {error}")
            return None
        return Step(tool=tool.name, params=params)

    def authorize(
        self,
        prepared: PreparedAction,
        *,
        approval: Approval | None = None,
        verdict_routes: Iterable[Route] | None = None,
    ) -> Authorization:
        """Decide whether a prepared action may run. Refusals carry a code."""
        if verdict_routes is not None and prepared.route not in set(verdict_routes):
            raise AuthorizationRefused(
                f"the safety floor does not allow {prepared.route.value} for case "
                f"{prepared.case_id}"
            )

        if prepared.route is Route.ESCALATE:
            raise AuthorizationRefused(
                f"case {prepared.case_id} escalates: a human decides, nothing commits"
            )

        if prepared.route not in AUTONOMOUS_ROUTES:
            if approval is None:
                raise ApprovalRequired(
                    f"case {prepared.case_id} is {prepared.route.value}: "
                    "commit waits for an explicit approval"
                )
            if approval.prepared_digest != prepared.digest:
                raise StaleApproval(
                    f"approval was for {approval.prepared_digest[:12]}, the prepared action "
                    f"is {prepared.digest[:12]}"
                )
            return Authorization(
                prepared_digest=prepared.digest,
                route=prepared.route,
                approved_by=approval.approved_by,
                reason=f"approved by {approval.approved_by}",
            )

        return Authorization(
            prepared_digest=prepared.digest,
            route=prepared.route,
            approved_by="auto",
            reason=f"{prepared.route.value} needs no approval",
        )

    def commit(
        self,
        prepared: PreparedAction,
        authorization: Authorization,
        *,
        at: datetime,
    ) -> Receipt:
        """Run every step and write the one receipt for this action.

        ponytail: the steps run in order with no rollback, so a tool that raises
        half-way leaves the earlier steps applied. The simulated mailbox cannot lose
        data this way; real tools need the atomic write and crash recovery that plan
        Commit 5.5 builds.
        """
        if authorization.prepared_digest != prepared.digest:
            raise StaleApproval(
                f"authorization was for {authorization.prepared_digest[:12]}, the prepared "
                f"action is {prepared.digest[:12]}"
            )

        effects: list[Effect] = []
        for step in prepared.steps:
            effects.extend(self.tool(step.tool).apply(step.params))

        return Receipt(
            receipt_id=f"rcpt-{prepared.digest[:12]}",
            blocked=prepared.blocked,
            case_id=prepared.case_id,
            message_id=prepared.message_id,
            route=prepared.route,
            action_id=prepared.action_id,
            prepared_digest=prepared.digest,
            effects=tuple(effects),
            committed_at=at,
        )


def _with_context(params: Mapping[str, Any], case_id: str, message_id: str) -> dict[str, Any]:
    """Every step carries the ids, so one receipt can name the case it came from."""
    enriched = dict(params)
    enriched.setdefault("case_id", case_id)
    enriched.setdefault("email_id", message_id)
    return enriched


def _notify_text(action_id: str) -> str:
    """What the user is told when a route promises a notification."""
    if action_id in {"", "unsupported"}:
        return "Handled an email; nothing was changed."
    return f"Handled an email with {action_id}."


def _params_brief(params: Mapping[str, Any]) -> str:
    shown = {key: value for key, value in params.items() if key not in {"case_id", "email_id"}}
    return ", ".join(f"{key}={value!r}" for key, value in sorted(shown.items()))


def _digest(
    case_id: str,
    message_id: str,
    route: Route,
    action_id: str,
    steps: tuple[Step, ...],
    blocked: tuple[str, ...] = (),
) -> str:
    """A stable hash of the work, so an approval can only ever mean this exact action."""
    payload = {
        "case_id": case_id,
        "message_id": message_id,
        "route": route.value,
        "action_id": action_id,
        "steps": [
            {"tool": step.tool, "params": dict(sorted(step.params.items()))}
            for step in steps
        ],
        "blocked": list(blocked),
    }
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, default=str).encode("utf-8")
    ).hexdigest()


__all__ = [
    "AUTONOMOUS_ROUTES",
    "Approval",
    "ApprovalRequired",
    "Authorization",
    "AuthorizationRefused",
    "Effect",
    "PreparedAction",
    "Receipt",
    "StaleApproval",
    "Step",
    "Tool",
    "ToolError",
    "ToolRegistry",
    "UnknownTool",
]
