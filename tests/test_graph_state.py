from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from agent.events import Message, SenderIdentity
from agent.replay import SeededClock
from agent.safety.floor import ActionClass, Route, SafetyVerdict, VetoLevel
from agent.state import (
    TRACE_KEYS,
    GraphState,
    hint_fields,
    message_digest,
    prepared_fields,
    receipt_fields,
    verdict_fields,
)
from agent.tools.registry import Effect, PreparedAction, Receipt, Step
from agent.trace import MAX_STRING, TraceError, TraceSink
from agent.triage import triage

BODY = "Hi Aydin, the wire details changed: pay to account 999-888 at First National."
SENDER = "billing@officesupply.synthetic.example"
FORBIDDEN = re.compile(r"secret|token_map", re.IGNORECASE)


def message() -> Message:
    return Message(
        message_id="m-wajo-0011",
        thread_id="th-wajo-0011",
        sender=SenderIdentity(email=SENDER, display_name="OfficeSupply Hub"),
        recipients=("aydin@techcorp.synthetic.example",),
        subject="Urgent Invoice #9012 - Wire Transfer Required",
        body=BODY,
    )


def verdict() -> SafetyVerdict:
    return SafetyVerdict(
        veto=True,
        veto_level=VetoLevel.ESCALATE,
        allowed_routes=(Route.ASK_FIRST_WITH_PREDRAFT, Route.ESCALATE),
        reason="money movement leaves the single-user boundary",
        rule_id="FLR-001",
        action_class=ActionClass.IRREVERSIBLE_EXTERNAL,
    )


def state() -> GraphState:
    """One decision as a producer would build it: ids, digests and bounded records."""
    email = message()
    prepared = PreparedAction(
        case_id="WAJO-0011",
        message_id=email.message_id,
        route=Route.ASK_FIRST_WITH_PREDRAFT,
        action_id="email.create_draft",
        steps=(Step(tool="create_draft", params={"body": BODY, "to": SENDER}),),
        digest="digest-of-the-work",
        blocked=("send: no send tool is wired for this run",),
    )
    receipt = Receipt(
        receipt_id="rcpt-000000000001",
        case_id="WAJO-0011",
        message_id=email.message_id,
        route=Route.PROCEED_AND_NOTIFY,
        action_id="email.apply_label",
        prepared_digest="digest-of-the-work",
        effects=(Effect(tool="apply_label", target=SENDER, detail=f"labelled with {BODY}"),),
        committed_at=SeededClock(seed=7).now(),
    )
    return {
        "case_id": "WAJO-0011",
        "message_id": email.message_id,
        "thread_id": email.thread_id,
        "lane": "calibration",
        "sequence_index": 3,
        "message_digest": message_digest(email),
        "dataset_digest": "a" * 64,
        "replay_seed": 7,
        "hints": hint_fields(triage(email)),
        "proposal": {"source": "rules", "route": "ESCALATE", "action_id": "email.escalate"},
        "floor": verdict_fields(verdict()),
        "route": "ESCALATE",
        "action_id": "email.escalate",
        "prepared": prepared_fields(prepared),
        "receipt": receipt_fields(receipt),
        "interrupt": {"code": "AUTHORIZATION_REFUSED"},
        "feedback": ["WAJO-0011:input:1"],
        "claims": ["clm-1"],
        "node": "sim",
    }


def test_the_state_round_trips_through_the_serde():
    """What the checkpointer serialises is what it reads back, unchanged."""
    from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer

    serde = JsonPlusSerializer()
    original = state()
    kind, blob = serde.dumps_typed(original)
    assert kind == "msgpack"
    assert serde.loads_typed((kind, blob)) == original


def test_the_state_comes_back_out_of_a_real_checkpointer():
    """Not just the serde: a compiled graph through a saver hands back the same values."""
    from langgraph.checkpoint.memory import InMemorySaver
    from langgraph.graph import END, START, StateGraph

    def echo(_: GraphState) -> GraphState:
        return {"node": "echo"}

    builder = StateGraph(GraphState)
    builder.add_node("echo", echo)
    builder.add_edge(START, "echo")
    builder.add_edge("echo", END)
    app = builder.compile(checkpointer=InMemorySaver())
    config = {"configurable": {"thread_id": "t-1"}}
    original = state()

    app.invoke(original, config)
    loaded = app.get_state(config).values
    assert loaded["floor"] == original["floor"]
    assert loaded["prepared"] == original["prepared"]
    assert loaded["receipt"] == original["receipt"]
    assert loaded["hints"] == original["hints"]
    assert loaded["message_digest"] == original["message_digest"]
    assert loaded["sequence_index"] == 3
    assert loaded["node"] == "echo"


def test_every_key_the_state_declares_is_traceable():
    """The allowlist is the schema: a new field is traceable, not silently dropped."""
    assert tuple(GraphState.__annotations__) == TRACE_KEYS
    assert set(state()) <= set(TRACE_KEYS)


def test_a_trace_holds_ids_and_not_the_mail(tmp_path: Path):
    """The body and subject are inputs to the decision, and must not reach the file."""
    path = tmp_path / "run.jsonl"
    with TraceSink(path) as sink:
        written = sink.write("decision", state())
    text = path.read_text(encoding="utf-8")
    assert BODY not in text
    assert message().subject not in text
    assert "wire details changed" not in text
    # The decision is still legible: what it was, what it decided, why.
    assert written["route"] == "ESCALATE"
    assert written["floor"]["rule_id"] == "FLR-001"
    assert written["prepared"]["digest"] == "digest-of-the-work"


def test_an_address_keeps_its_domain_and_loses_its_person(tmp_path: Path):
    path = tmp_path / "run.jsonl"
    with TraceSink(path) as sink:
        sink.write("decision", state())
    line = json.loads(path.read_text(encoding="utf-8").splitlines()[-1])
    target = line["receipt"]["effects"][0]["target"]
    assert SENDER not in target
    assert target.endswith("@officesupply.synthetic.example")


def test_a_secret_shaped_field_is_never_written(tmp_path: Path):
    """No line may contain these words, in a key or in a value."""
    path = tmp_path / "run.jsonl"
    nested = {
        "case_id": "WAJO-0011",
        "floor": {"reason": "cannot read token_map: no api_key for the backend"},
        "prepared": {"token_map": {"a@b.com": "tok_1"}, "summary": "send(secret=sk-live-123456)"},
        "proposal": {"source": "openrouter", "route": "ESCALATE", "api_key": "sk-live-123456"},
    }
    with TraceSink(path) as sink:
        sink.write("decision", nested)
    text = path.read_text(encoding="utf-8")
    assert not FORBIDDEN.search(text), text
    assert "sk-live" not in text
    assert "tok_1" not in text
    # And the field is replaced, not silently dropped: the digest is still there.
    line = json.loads(text.splitlines()[-1])
    assert line["prepared"]["summary"].startswith("sha256:")
    assert all(key.startswith("sha256:") for key in line["prepared"] if key != "summary")


def test_a_long_text_is_a_digest_and_a_short_one_is_not(tmp_path: Path):
    path = tmp_path / "run.jsonl"
    with TraceSink(path) as sink:
        sink.write("decision", {"case_id": "x", "node": "n" * (MAX_STRING + 1)})
        sink.write("decision", {"case_id": "x", "node": "route"})
    first, second = (json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()[-2:])
    assert first["node"].startswith("sha256:")
    assert "chars, str" in first["node"]
    assert second["node"] == "route"


def test_only_the_keys_the_state_names_are_written(tmp_path: Path):
    path = tmp_path / "run.jsonl"
    with TraceSink(path) as sink:
        written = sink.write("decision", {"case_id": "WAJO-0011", "sneaky": "raw text"})
    assert "sneaky" not in written
    assert "raw text" not in path.read_text(encoding="utf-8")


def test_the_sink_says_where_it_could_not_write(tmp_path: Path):
    """Error handling at the boundary: a path that is not a file names itself."""
    with pytest.raises(TraceError, match="cannot write a trace"):
        TraceSink(tmp_path)


def test_a_trace_keeps_its_lines_after_a_close(tmp_path: Path):
    """The run that dies is the one worth tracing, so lines are flushed as written."""
    path = tmp_path / "run.jsonl"
    sink = TraceSink(path)
    sink.write("decision", {"case_id": "WAJO-0011"})
    for line in path.read_text(encoding="utf-8").splitlines():
        json.loads(line)
    sink.close()
    sink.close()
    with pytest.raises(TraceError, match="already closed"):
        sink.write("decision", {"case_id": "WAJO-0011"})
