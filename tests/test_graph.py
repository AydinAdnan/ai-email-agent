import asyncio
import io
import json
import re
import sys
from pathlib import Path

import pytest
from langgraph.checkpoint.memory import InMemorySaver

from agent.cli import main
from agent.dataset import Lane, LaneView, Manifest
from agent.events import Message
from agent.gateway import ProposalGateway, RuleProvider
from agent.graph import GraphError, GraphRuntime, build_graph, run_graph
from agent.pii import mask_for_llm
from agent.replay import SeededClock
from agent.sim.runner import run_simulation
from agent.tools.email_tools import SimulatedMailbox, build_registry
from agent.trace import TraceSink
from agent.triage import Triage

FIXTURE = Path(__file__).parent / "fixtures" / "stream_12.jsonl"
PIPELINE_ROUTE = re.compile(r"^    pipeline: route=(\w+)")


def view() -> LaneView:
    return Manifest.load(FIXTURE).view(Lane.CALIBRATION)


class Recording(ProposalGateway):
    """A gateway that keeps what the provider was allowed to see."""

    def __init__(self) -> None:
        super().__init__(RuleProvider())
        self.seen: list[Message] = []

    async def propose(self, message: Message, hints: Triage):
        self.seen.append(message)
        return await super().propose(message, hints)


def runtime(lane: LaneView, **kwargs) -> GraphRuntime:
    return GraphRuntime(
        cases={case.case_id: case for case in lane.cases},
        gateway=kwargs.get("gateway") or ProposalGateway(RuleProvider()),
        registry=kwargs.get("registry") or build_registry(SimulatedMailbox()),
        clock=SeededClock(seed=7),
        mask=kwargs.get("mask", False),
    )


def test_every_arrival_ends_in_exactly_one_receipt_or_one_interrupt():
    outcome = asyncio.run(run_graph(view(), seed=7, mask=False))
    assert outcome.processed == len(view().cases)
    committed = {receipt.case_id for receipt in outcome.receipts}
    held = set(outcome.interrupts)
    assert committed.isdisjoint(held)
    assert committed | held == set(outcome.order)
    assert len(outcome.receipts) == len(committed)
    # A held decision waits for a human; a refusal has nothing to wait on.
    assert len(outcome.held) + len(outcome.refusals) == len(held)


def test_the_graph_and_the_simulator_agree_case_by_case():
    """The graph is not a second opinion: same proposals, same route, same receipts."""
    lane = view()
    transcript = io.StringIO()
    sim = asyncio.run(run_simulation(lane, seed=7, out=transcript, show_labels=True))
    graph = asyncio.run(run_graph(lane, seed=7, mask=False))

    sim_routes = [
        match.group(1)
        for line in transcript.getvalue().splitlines()
        if (match := PIPELINE_ROUTE.match(line))
    ]
    assert [graph.routes[case_id] for case_id in graph.order] == sim_routes
    assert sorted((item.case_id, item.receipt_id) for item in graph.receipts) == sorted(
        (item.case_id, item.receipt_id) for item in sim.receipts
    )
    assert graph.effects("label") == sim.effects("label")
    assert graph.effects("notify") == sim.effects("notify")
    # The simulator records a wait and a refusal in the same list; the graph separates them.
    assert set(graph.interrupts) == {item.split(":")[0] for item in sim.refusals}
    assert len(graph.held) == len(sim.awaiting_approval)


def test_the_provider_is_shown_the_masked_mail_and_the_floor_is_not():
    lane = view()
    spied = Recording()
    outcome = asyncio.run(run_graph(lane, seed=7, mask=True, gateway=spied))

    raw = {case.event.message.thread_id: case.event.message for case in lane.cases}
    assert len(spied.seen) == outcome.processed
    changed = 0
    for message in spied.seen:
        original = raw[message.thread_id]
        expected = mask_for_llm(original.subject, original.body, message.thread_id)
        assert (message.subject, message.body) == expected
        changed += int((message.subject, message.body) != (original.subject, original.body))
    assert changed >= 5, f"masking reached the provider with nothing to do on {changed} arrivals"

    # The floor still reads the mail as it arrived, so the wire request still escalates.
    assert outcome.routes["WAJO-0011"] == "ESCALATE"


def test_the_state_and_the_trace_carry_no_mail_text(tmp_path: Path):
    lane = view()
    path = tmp_path / "graph.jsonl"
    sink = TraceSink(path)
    outcome = asyncio.run(run_graph(lane, seed=7, mask=True, trace=sink))
    sink.close()

    lines = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
    decisions = [line for line in lines if line["event"] == "decision"]
    assert len(decisions) == outcome.processed
    # The minimize node's only product is a record; a schema that drops it hides the stage.
    assert any(line.get("pii", {}).get("redactions", 0) > 0 for line in decisions)
    text = path.read_text(encoding="utf-8")
    for case in lane.cases:
        assert case.event.message.body[:60] not in text
        assert case.event.message.subject not in text
    assert not re.search(r"secret|token_map", text, re.IGNORECASE)


def test_a_waiting_decision_holds_its_prepared_action_and_commits_nothing():
    outcome = asyncio.run(run_graph(view(), seed=7, mask=False))
    held = {item.case_id: item for item in outcome.held}
    assert held, "the fixture has ask-first cases"
    for case_id, prepared in held.items():
        assert outcome.interrupts[case_id] == "APPROVAL_REQUIRED"
        assert prepared.digest
        assert case_id not in {receipt.case_id for receipt in outcome.receipts}


def test_a_decision_the_floor_fences_waits_on_nothing():
    outcome = asyncio.run(run_graph(view(), seed=7, mask=False))
    assert outcome.routes["WAJO-0011"] == "ESCALATE"
    assert outcome.interrupts["WAJO-0011"] == "AUTHORIZATION_REFUSED"
    assert all(item.endswith(": AUTHORIZATION_REFUSED") for item in outcome.refusals)
    assert any(item.startswith("WAJO-0011") for item in outcome.refusals)
    assert "WAJO-0011" not in {item.case_id for item in outcome.held}


def test_the_checkpointer_records_every_step_of_a_decision():
    lane = view()
    case = lane.cases[0]
    saver = InMemorySaver()
    app = build_graph(runtime(lane), checkpointer=saver)
    config = {"configurable": {"thread_id": "one-decision"}}

    state = asyncio.run(
        app.ainvoke(
            {"case_id": case.case_id, "lane": lane.lane.value, "sequence_index": 1}, config
        )
    )
    assert state["message_digest"].startswith("sha256:")
    assert state["floor"]["allowed_routes"]
    assert len(list(saver.list(config))) > 5


def test_a_case_the_lane_does_not_hold_fails_with_its_name():
    app = build_graph(runtime(view()))
    config = {"configurable": {"thread_id": "unknown-case"}}
    with pytest.raises(GraphError, match="WAJO-9999"):
        asyncio.run(app.ainvoke({"case_id": "WAJO-9999", "lane": "calibration"}, config))


def test_the_cli_walks_a_lane_and_says_what_each_arrival_ended_in(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
):
    monkeypatch.setattr(sys, "stdin", io.StringIO(""))
    assert main(["graph", "run", "--fixture", str(FIXTURE), "--seed", "7"]) == 0
    printed = capsys.readouterr().out
    assert printed.count("committed\n") == 5
    assert "processed=12 committed=5 held=3 refused=4" in printed
    assert "provider view: masked subject and body" in printed


def test_the_cli_keeps_the_held_out_lane_shut():
    with pytest.raises(SystemExit):
        main(["graph", "run", "--fixture", str(FIXTURE), "--lane", "held_out"])
