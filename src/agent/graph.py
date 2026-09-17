"""The decision graph: one arrival walked from ingest to receipt, checkpointed per step."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field, replace
from typing import Any

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from agent.dataset import Case, LaneView
from agent.events import Message
from agent.gateway import NO_ACTION_TOOL, ProposalError, ProposalGateway, RuleProvider
from agent.pii import mask_for_llm
from agent.replay import SeededClock
from agent.sim.policy import Decision, route_decision
from agent.sim.schedule import WINDOW_SIZE, schedule
from agent.state import (
    GraphState,
    hint_fields,
    message_digest,
    prepared_fields,
    receipt_fields,
    verdict_fields,
)
from agent.tools.email_tools import SimulatedMailbox, build_registry
from agent.tools.registry import (
    ApprovalRequired,
    Authorization,
    AuthorizationRefused,
    PreparedAction,
    Receipt,
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
        context.decisions[case_id] = route_decision(case, hints, None, message, source="graph")
        return {
            "node": "proposal",
            "proposal": {"source": "graph", "error": str(error)},
            "errors": [*state.get("errors", []), str(error)],
        }
    context.decisions[case_id] = route_decision(case, hints, answer, answer.rationale, source="graph")
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
    """Record the route the floor left standing, which is what authorization checks."""
    decision = context.decisions[state["case_id"]]
    return {
        "node": "route",
        "route": decision.route.value,
        "action_id": decision.action_id,
        "floor": verdict_fields(decision.verdict),
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


async def interrupt(state: GraphState, context: GraphRuntime) -> GraphState:
    """Hold here: the action is prepared and nothing has run. Resume is 5.5's."""
    code = state.get("interrupt", {}).get("code", "")
    return {"node": "interrupt", "trace": _note(state, f"held ({code})")}


async def commit(state: GraphState, context: GraphRuntime) -> GraphState:
    """The only node that changes anything, and it only ever sees authorized work."""
    case_id = state["case_id"]
    receipt = context.registry.commit(
        context.prepared[case_id],
        context.authorizations[case_id],
        at=context.clock.now(),
    )
    context.receipts[case_id] = receipt
    return {"node": "commit", "receipt": receipt_fields(receipt)}


async def receipt(state: GraphState, context: GraphRuntime) -> GraphState:
    """The terminal record: one decision, closed."""
    return {"node": "receipt", "trace": _note(state, "closed")}


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
        ("interrupt", interrupt),
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
) -> GraphOutcome:
    """Walk a lane through the graph, one decision per checkpoint thread.

    The lane is delivered in the order the seed drew, exactly as the simulator delivers
    it, so the two paths can be compared arrival by arrival.
    """
    deliveries = tuple(
        case for item in schedule(view.cases, window=window, seed=seed) for case in item.cases
    )
    context = GraphRuntime(
        cases={case.case_id: case for case in view.cases},
        gateway=gateway if gateway is not None else ProposalGateway(RuleProvider()),
        registry=registry if registry is not None else build_registry(mailbox or SimulatedMailbox()),
        clock=SeededClock(seed=seed),
        known_senders=dict(known_senders or {}),
        mask=mask,
    )
    app = build_graph(context, checkpointer=checkpointer)
    outcome = GraphOutcome()
    for index, case in enumerate(deliveries, start=1):
        initial: GraphState = {
            "case_id": case.case_id,
            "lane": view.lane.value,
            "sequence_index": index,
        }
        thread = {"configurable": {"thread_id": f"{seed}:{case.case_id}"}}
        state: GraphState = {}
        try:
            state = await app.ainvoke(initial, thread)
        except GraphError:
            raise
        except Exception as error:
            raise GraphError(
                f"case {case.case_id} failed in {state.get('node') or 'the graph'}: "
                f"{type(error).__name__}: {error}"
            ) from error

        outcome.processed += 1
        outcome.order.append(case.case_id)
        outcome.nodes[case.case_id] = list(state.get("trace", []))
        route_value = state.get("route", "")
        outcome.routes[case.case_id] = route_value
        outcome.route_counts[route_value] = outcome.route_counts.get(route_value, 0) + 1
        if receipt := context.receipts.get(case.case_id):
            outcome.receipts.append(receipt)
        elif interrupt := state.get("interrupt"):
            code = str(interrupt.get("code", ""))
            outcome.interrupts[case.case_id] = code
            prepared = context.prepared.get(case.case_id)
            if prepared is not None and code == ApprovalRequired.code:
                outcome.held.append(prepared)
            else:
                outcome.refusals.append(f"{case.case_id}: {code}")
        if trace is not None:
            trace.write("decision", state, at=context.clock.now())
    return outcome


__all__ = [
    "GraphError",
    "GraphOutcome",
    "GraphRuntime",
    "build_graph",
    "run_graph",
]
