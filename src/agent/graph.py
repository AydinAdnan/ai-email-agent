"""The decision graph: one arrival walked from ingest to receipt, checkpointed per step."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field, replace
from typing import Any

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.types import Command, interrupt

from agent.autonomy.router import Router
from agent.dataset import Case, LaneView
from agent.events import Message
from agent.gateway import NO_ACTION_TOOL, ProposalError, ProposalGateway, RuleProvider
from agent.pii import mask_for_llm
from agent.replay import SeededClock
from agent.sim.policy import Decision, route_decision
from agent.sim.schedule import WINDOW_SIZE, schedule
from agent.state import (
    GraphState,
    draft_fields,
    hint_fields,
    message_digest,
    prepared_fields,
    receipt_fields,
    routing_fields,
    verdict_fields,
)
from agent.tools.email_tools import SimulatedMailbox, build_registry
from agent.tools.registry import (
    Approval,
    ApprovalRequired,
    Authorization,
    AuthorizationRefused,
    PreparedAction,
    Receipt,
    StaleApproval,
    ToolRegistry,
)
from agent.trace import TraceSink
from agent.triage import Triage, triage


class GraphError(RuntimeError):
    """The graph cannot continue, naming the case it stopped on."""


@dataclass
class GraphRuntime:
    """Working objects, kept out of the state so nothing here is checkpointed."""

    cases: Mapping[str, Case]
    gateway: ProposalGateway
    registry: ToolRegistry
    clock: SeededClock
    known_senders: Mapping[str, str] = field(default_factory=dict)
    # The stage the plan puts in front of the provider. Off measures the graph against
    # the simulator, which has never masked.
    mask: bool = True
    # The run's router when it has one - the simulator's, so earned trust carries into the
    # graph - and a cold one otherwise: the user's own rules, and no history behind them.
    router: Router = field(default_factory=Router)
    masked: dict[str, Message] = field(default_factory=dict)
    hints: dict[str, Triage] = field(default_factory=dict)
    decisions: dict[str, Decision] = field(default_factory=dict)
    prepared: dict[str, PreparedAction] = field(default_factory=dict)
    authorizations: dict[str, Authorization] = field(default_factory=dict)
    receipts: dict[str, Receipt] = field(default_factory=dict)


@dataclass
class GraphOutcome:
    """What a lane through the graph did."""

    processed: int = 0
    route_counts: dict[str, int] = field(default_factory=dict)
    receipts: list[Receipt] = field(default_factory=list)
    held: list[PreparedAction] = field(default_factory=list)
    interrupts: dict[str, str] = field(default_factory=dict)
    refusals: list[str] = field(default_factory=list)
    order: list[str] = field(default_factory=list)
    routes: dict[str, str] = field(default_factory=dict)
    nodes: dict[str, list[str]] = field(default_factory=dict)

    def effects(self, tool: str) -> int:
        """How many times a tool actually ran, counted from the receipts."""
        return sum(
            1 for receipt in self.receipts for effect in receipt.effects if effect.tool == tool
        )


def _case(state: GraphState, context: GraphRuntime) -> Case:
    """The case this decision is about, or a named failure rather than a KeyError."""
    case_id = state.get("case_id", "")
    if case_id not in context.cases:
        raise GraphError(f"the graph was handed case id {case_id!r}, which the lane does not hold")
    return context.cases[case_id]


def _note(state: GraphState, text: str) -> list[str]:
    return [*state.get("trace", []), text]


async def ingest(state: GraphState, context: GraphRuntime) -> GraphState:
    """Name the arrival: ids, delivered position, and a digest of the mail."""
    case = _case(state, context)
    email = case.event.message
    return {
        "case_id": case.case_id,
        "message_id": email.message_id,
        "thread_id": email.thread_id,
        "message_digest": message_digest(email),
        "node": "ingest",
    }


async def consent(state: GraphState, context: GraphRuntime) -> GraphState:
    """Nothing gates on consent yet: the store is Phase 4's, and a stub must not pretend."""
    return {"node": "consent", "trace": _note(state, "consent: no store yet")}


async def minimize(state: GraphState, context: GraphRuntime) -> GraphState:
    """Mask the mail for the provider. The reverse map stays in the masker's registry.

    Only the provider sees this. Triage and the floor read the mail as it arrived,
    because the floor's money, credential and injection tripwires are meant to fire on
    what the sender actually wrote - a masked body would hide the wire request they
    exist to catch.
    """
    email = _case(state, context).event.message
    if not context.mask:
        return {"node": "minimize", "pii": {"redactions": 0, "masked_digest": ""}}
    subject, body = mask_for_llm(email.subject, email.body, thread_id=email.thread_id)
    masked = replace(email, subject=subject, body=body)
    context.masked[state["case_id"]] = masked
    return {
        "node": "minimize",
        "pii": {
            "redactions": int(subject != email.subject) + int(body != email.body),
            "masked_digest": message_digest(masked),
        },
    }


async def pre_triage(state: GraphState, context: GraphRuntime) -> GraphState:
    """The deterministic first reading, from the mail as it arrived."""
    hints = triage(_case(state, context).event.message, known_senders=dict(context.known_senders))
    context.hints[state["case_id"]] = hints
    return {"node": "pre_triage", "hints": hint_fields(hints)}


async def proposal(state: GraphState, context: GraphRuntime) -> GraphState:
    """Ask the provider. What it is shown is the masked message, never the raw one."""
    case_id = state["case_id"]
    case = context.cases[case_id]
    hints = context.hints[case_id]
    email = context.masked.get(case_id) or case.event.message
    try:
        answer = await context.gateway.propose(email, hints)
    except ProposalError as error:
        # No usable proposal is not a licence to guess; it is a reason to escalate.
        message = f"no usable proposal: {error}"
        context.decisions[case_id] = route_decision(
            case,
            hints,
            None,
            message,
            source="graph",
            router=context.router,
            provider=context.gateway.provider,
        )
        return {
            "node": "proposal",
            "proposal": {"source": "graph", "error": str(error)},
            "errors": [*state.get("errors", []), str(error)],
        }
    context.decisions[case_id] = route_decision(
        case,
        hints,
        answer,
        answer.rationale,
        source="graph",
        router=context.router,
        provider=context.gateway.provider,
    )
    return {
        "node": "proposal",
        "proposal": {
            "source": "graph",
            "route": answer.route.value,
            "action_id": answer.action_id or "",
            "rationale": answer.rationale,
        },
    }


async def route(state: GraphState, context: GraphRuntime) -> GraphState:
    """Record the route the router chose, which is what authorization checks."""
    decision = context.decisions[state["case_id"]]
    return {
        "node": "route",
        "route": decision.route.value,
        "action_id": decision.action_id,
        "floor": verdict_fields(decision.verdict),
        "routing": routing_fields(decision.routing),
        "draft": draft_fields(
            decision.drafting, sender=_case(state, context).event.message.sender.email
        ),
    }


async def prepare(state: GraphState, context: GraphRuntime) -> GraphState:
    """Build the action without touching anything, so a refusal leaves the world as it is."""
    decision = context.decisions[state["case_id"]]
    case = context.cases[state["case_id"]]
    prepared = context.registry.prepare(
        case_id=decision.case_id,
        message_id=case.event.message.message_id,
        route=decision.route,
        action_id=decision.action_id,
        tool_name=None if decision.tool_name == NO_ACTION_TOOL else decision.tool_name,
        params=decision.params,
    )
    context.prepared[state["case_id"]] = prepared
    return {"node": "prepare", "prepared": prepared_fields(prepared)}


async def authorize(state: GraphState, context: GraphRuntime) -> GraphState:
    """Ask the registry whether this exact work may run, and record why if it may not."""
    case_id = state["case_id"]
    decision = context.decisions[case_id]
    prepared = context.prepared[case_id]
    try:
        context.authorizations[case_id] = context.registry.authorize(
            prepared, verdict_routes=decision.verdict.allowed_routes
        )
    except (ApprovalRequired, AuthorizationRefused) as held:
        return {
            "node": "authorize",
            "interrupt": {"code": held.code, "prepared_digest": prepared.digest},
        }
    return {"node": "authorize", "interrupt": {}}


async def hold(state: GraphState, context: GraphRuntime) -> GraphState:
    """Hold here until a human answers, and treat a yes about other work as stale.

    The pause is the framework's interrupt: the decision stays on its thread, so a resume
    continues from this checkpoint instead of walking the lane again. The digest the
    answer carries is checked here against the one that was shown, and again by the
    registry against the action that is about to run.
    """
    held = state.get("interrupt") or {}
    if not held:
        return {"node": "interrupt"}

    digest = str(held.get("prepared_digest", ""))
    answer = interrupt(
        {
            "case_id": state.get("case_id", ""),
            "route": state.get("route", ""),
            "code": held.get("code", ""),
            "prepared_digest": digest,
            "summary": state.get("prepared", {}).get("summary", ""),
        }
    )
    if not isinstance(answer, Mapping) or not answer.get("approved_by"):
        return {
            "node": "interrupt",
            "interrupt": {"code": "REJECTED", "prepared_digest": digest},
            "approval": {},
            "trace": _note(state, "rejected"),
        }
    if str(answer.get("prepared_digest", "")) != digest:
        return {
            "node": "interrupt",
            "interrupt": {"code": StaleApproval.code, "prepared_digest": digest},
            "approval": {},
            "trace": _note(state, "stale approval"),
        }
    return {
        "node": "interrupt",
        "interrupt": {},
        "approval": {
            "approved_by": str(answer["approved_by"]),
            "prepared_digest": digest,
        },
        "trace": _note(state, f"approved by {answer['approved_by']}"),
    }


async def commit(state: GraphState, context: GraphRuntime) -> GraphState:
    """The only node that changes anything, and it only ever sees authorized work."""
    case_id = state["case_id"]
    prepared = context.prepared.get(case_id)
    if prepared is None:
        raise GraphError(f"case {case_id} reached commit with nothing prepared")
    authorization = context.authorizations.get(case_id) or _authorized_settled(
        context, state, case_id, prepared
    )
    receipt = context.registry.commit(prepared, authorization, at=context.clock.now())
    context.receipts[case_id] = receipt
    return {"node": "commit", "receipt": receipt_fields(receipt)}


async def receipt(state: GraphState, context: GraphRuntime) -> GraphState:
    """The terminal record: one decision, closed."""
    return {"node": "receipt", "trace": _note(state, "closed")}


def _authorized_settled(
    context: GraphRuntime, state: GraphState, case_id: str, prepared: PreparedAction
) -> Authorization:
    """Authorize from the state alone, so a decision approved before a crash still runs."""
    approval = state.get("approval") or {}
    if not approval:
        raise GraphError(f"case {case_id} reached commit with no authorization")
    decision = context.decisions[case_id]
    return context.registry.authorize(
        prepared,
        approval=Approval(
            prepared_digest=str(approval["prepared_digest"]),
            approved_by=str(approval["approved_by"]),
        ),
        verdict_routes=decision.verdict.allowed_routes,
    )


def _next_after_interrupt(state: GraphState) -> str:
    """Where a decision goes: the commit node, or the end of the line."""
    return "commit" if not state.get("interrupt") else END


def build_graph(context: GraphRuntime, *, checkpointer: Any | None = None) -> CompiledStateGraph:
    """Compile the node graph. The checkpointer is injectable for tests and for 5.5."""
    builder = StateGraph(GraphState)
    for name, node in (
        ("ingest", ingest),
        ("consent", consent),
        ("minimize", minimize),
        ("pre_triage", pre_triage),
        ("proposal", proposal),
        ("route", route),
        ("prepare", prepare),
        ("authorize", authorize),
        ("interrupt", hold),
        ("commit", commit),
        ("receipt", receipt),
    ):
        builder.add_node(name, _bound(node, context))

    builder.add_edge(START, "ingest")
    builder.add_edge("ingest", "consent")
    builder.add_edge("consent", "minimize")
    builder.add_edge("minimize", "pre_triage")
    builder.add_edge("pre_triage", "proposal")
    builder.add_edge("proposal", "route")
    builder.add_edge("route", "prepare")
    builder.add_edge("prepare", "authorize")
    builder.add_edge("authorize", "interrupt")
    builder.add_conditional_edges("interrupt", _next_after_interrupt, ["commit", END])
    builder.add_edge("commit", "receipt")
    builder.add_edge("receipt", END)
    return builder.compile(checkpointer=checkpointer or InMemorySaver())


def _bound(node: Any, context: GraphRuntime) -> Any:
    """Hand a node its runtime. The graph only ever sees the state."""

    async def bound(state: GraphState) -> GraphState:
        return await node(state, context)

    bound.__name__ = getattr(node, "__name__", "node")
    return bound


@dataclass
class ResumeResult:
    """What resuming a held decision did, or why the answer could not be used."""

    status: str
    case_id: str
    receipt: Receipt | None = None
    reason: str = ""

    @property
    def committed(self) -> bool:
        return self.status == "committed"


class GraphSession:
    """One lane, one compiled graph, one checkpoint thread per decision.

    Holding the session is what makes an interrupt resumable: a paused decision lives on
    its thread, so resuming continues from that checkpoint instead of walking the lane
    again. The lane itself is the other half - a resume re-derives the decision from it
    and will not honour an answer whose work has moved since it was asked for.
    """

    def __init__(
        self,
        view: LaneView,
        *,
        seed: int = 7,
        gateway: ProposalGateway | None = None,
        registry: ToolRegistry | None = None,
        mailbox: SimulatedMailbox | None = None,
        mask: bool = True,
        known_senders: Mapping[str, str] | None = None,
        window: int = WINDOW_SIZE,
        trace: TraceSink | None = None,
        checkpointer: Any | None = None,
        router: Router | None = None,
    ) -> None:
        self.view = view
        self.seed = seed
        self.trace = trace
        self.deliveries = tuple(
            case for item in schedule(view.cases, window=window, seed=seed) for case in item.cases
        )
        self.context = GraphRuntime(
            cases={case.case_id: case for case in view.cases},
            gateway=gateway if gateway is not None else ProposalGateway(RuleProvider()),
            registry=(
                registry if registry is not None else build_registry(mailbox or SimulatedMailbox())
            ),
            clock=SeededClock(seed=seed),
            known_senders=dict(known_senders or {}),
            mask=mask,
            router=router,
        )
        self.app = build_graph(self.context, checkpointer=checkpointer)
        self.outcome = GraphOutcome()

    def thread_for(self, case_id: str) -> str:
        return f"{self.seed}:{case_id}"

    def _initial(self, case_id: str) -> GraphState:
        delivered = [case.case_id for case in self.deliveries].index(case_id) + 1
        return {
            "case_id": case_id,
            "lane": self.view.lane.value,
            "sequence_index": delivered,
        }

    async def run(self) -> GraphOutcome:
        """Walk the lane, holding at every decision that needs a human."""
        for index, case in enumerate(self.deliveries, start=1):
            config = {"configurable": {"thread_id": self.thread_for(case.case_id)}}
            state: GraphState = {}
            try:
                state = await self.app.ainvoke(self._initial(case.case_id), config)
            except GraphError:
                raise
            except Exception as error:
                raise GraphError(
                    f"case {case.case_id} failed in {state.get('node') or 'the graph'}: "
                    f"{type(error).__name__}: {error}"
                ) from error
            self._tally(case.case_id, state, index)
        return self.outcome

    async def resume(self, case_id: str, answer: Mapping[str, Any] | None) -> ResumeResult:
        """Answer a held decision, or refuse the answer because the work has moved.

        A resume is only as good as what it is resuming: the same lane re-derives the
        same decision, and both recorded digests - the mail it saw and the action it
        prepared - are held against a fresh derivation before anything is committed.
        """
        config = {"configurable": {"thread_id": self.thread_for(case_id)}}
        values = await self._checkpointed(config)
        if values.get("receipt"):
            return ResumeResult("NOT_WAITING", case_id, reason="this decision was committed")

        held = dict(values.get("interrupt") or {})
        settled = dict(values.get("approval") or {})
        if held.get("code") == AuthorizationRefused.code and not settled:
            return ResumeResult(
                AuthorizationRefused.code,
                case_id,
                reason="a human decides this one: nothing was prepared to approve",
            )
        # What the answer has to refer to: the work that was shown, the work that was
        # already approved when its commit died, or the work a crash never committed.
        recorded = str(
            held.get("prepared_digest")
            or settled.get("prepared_digest")
            or (values.get("prepared") or {}).get("digest", "")
        )
        if not recorded:
            return ResumeResult("NOT_WAITING", case_id, reason="this decision never reached one")

        stale = await self._moved_since(case_id, values, recorded)
        if stale:
            return ResumeResult(StaleApproval.code, case_id, reason=stale)
        if not held.get("prepared_digest"):
            # Decided, and approved or auto-authorized, but never committed: the crash
            # left the work pending, so there is nothing to ask and nothing to re-decide.
            return await self._invoke(case_id, config, None)
        if not answer or not answer.get("approved_by"):
            return ResumeResult("REJECTED", case_id, reason="nothing was approved")
        return await self._invoke(case_id, config, Command(resume=dict(answer)))

    async def _checkpointed(self, config: Mapping[str, Any]) -> GraphState:
        snapshot = await self.app.aget_state(config)
        if snapshot is None or not snapshot.values:
            raise GraphError("there is no checkpoint for this decision: nothing to resume")
        return dict(snapshot.values)

    async def _invoke(
        self, case_id: str, config: Mapping[str, Any], payload: Command | None
    ) -> ResumeResult:
        """Carry a thread past its interrupt, or past the point a crash cut it off at."""
        try:
            state = await self.app.ainvoke(payload, config)
        except StaleApproval as error:
            return ResumeResult(StaleApproval.code, case_id, reason=str(error))
        except GraphError:
            raise
        except Exception as error:
            raise GraphError(
                f"case {case_id} could not be resumed: {type(error).__name__}: {error}"
            ) from error
        self._tally(case_id, state, self._initial(case_id)["sequence_index"])
        receipt = self.context.receipts.get(case_id)
        if receipt is not None:
            return ResumeResult("committed", case_id, receipt=receipt)
        code = str((state.get("interrupt") or {}).get("code", ""))
        return ResumeResult(code or "NOT_RUN", case_id, reason="nothing was committed")

    async def _moved_since(self, case_id: str, values: GraphState, recorded: str) -> str:
        """Re-derive the decision and say what changed, or '' when nothing did."""
        try:
            fresh = await self.app.ainvoke(
                self._initial(case_id),
                {"configurable": {"thread_id": f"{self.thread_for(case_id)}:rederive"}},
            )
        except Exception as error:  # noqa: BLE001 - anything that stops the re-derivation
            # reads the same way here: the answer cannot be honoured, so nothing commits.
            return f"the decision could not be re-derived: {type(error).__name__}: {error}"
        if fresh.get("message_digest") != values.get("message_digest"):
            return "the mail changed since this decision was made"
        rederived = str((fresh.get("prepared") or {}).get("digest", ""))
        if rederived != recorded:
            return (
                f"the work changed: asked about {recorded[:12]}, "
                f"it is now {rederived[:12] or 'nothing'}"
            )
        return ""

    def _tally(self, case_id: str, state: GraphState, delivered: int) -> None:
        """Record an arrival once, whether it ran or was resumed."""
        if case_id not in self.outcome.order:
            self.outcome.order.append(case_id)
        self.outcome.nodes[case_id] = list(state.get("trace", []))
        route_value = state.get("route", "")
        self.outcome.routes[case_id] = route_value
        # Counted from the routes rather than accumulated: a resumed decision is tallied
        # twice, and a route may not be counted twice. ponytail: O(cases) per arrival.
        counts: dict[str, int] = {}
        for decided in self.outcome.routes.values():
            counts[decided] = counts.get(decided, 0) + 1
        self.outcome.route_counts = counts
        self.outcome.interrupts.pop(case_id, None)
        self.outcome.held = [item for item in self.outcome.held if item.case_id != case_id]
        self.outcome.refusals = [item for item in self.outcome.refusals if case_id not in item]
        self.outcome.receipts = [item for item in self.outcome.receipts if item.case_id != case_id]
        self.outcome.processed = len(self.outcome.order)

        if receipt := self.context.receipts.get(case_id):
            self.outcome.receipts.append(receipt)
        elif interrupt := state.get("interrupt"):
            code = str(interrupt.get("code", ""))
            self.outcome.interrupts[case_id] = code
            prepared = self.context.prepared.get(case_id)
            if prepared is not None and code == ApprovalRequired.code:
                self.outcome.held.append(prepared)
            else:
                self.outcome.refusals.append(f"{case_id}: {code}")
        if self.trace is not None:
            self.trace.write("decision", state, at=self.context.clock.now())


async def run_graph(
    view: LaneView,
    *,
    seed: int = 7,
    gateway: ProposalGateway | None = None,
    registry: ToolRegistry | None = None,
    mailbox: SimulatedMailbox | None = None,
    mask: bool = True,
    known_senders: Mapping[str, str] | None = None,
    window: int = WINDOW_SIZE,
    trace: TraceSink | None = None,
    checkpointer: Any | None = None,
    router: Router | None = None,
) -> GraphOutcome:
    """Walk a lane through the graph, one decision per checkpoint thread."""
    session = GraphSession(
        view,
        seed=seed,
        gateway=gateway,
        registry=registry,
        mailbox=mailbox,
        mask=mask,
        known_senders=known_senders,
        window=window,
        trace=trace,
        checkpointer=checkpointer,
        router=router,
    )
    return await session.run()


__all__ = [
    "GraphError",
    "GraphOutcome",
    "GraphRuntime",
    "GraphSession",
    "ResumeResult",
    "build_graph",
    "run_graph",
]
