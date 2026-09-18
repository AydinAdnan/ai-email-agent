"""Phase 7.2: the predraft an ask carries - facts cited, gaps exposed, nothing sent."""
import asyncio
import json
from dataclasses import replace
from datetime import UTC, datetime
from pathlib import Path

import pytest

from agent.dataset import Case, Lane, Manifest
from agent.drafts import (
    DRAFTING_TOOLS,
    DraftCode,
    Drafting,
    SentExample,
    Style,
    draft_reply,
    drafting_for,
    retrieve_style,
    validate_draft,
)
from agent.gateway import Proposal
from agent.graph import run_graph
from agent.safety.floor import Route
from agent.sim import policy
from agent.sim.policy import route_decision
from agent.tools.email_tools import SimulatedMailbox, build_registry
from agent.tools.registry import Approval, ApprovalRequired
from agent.trace import TraceSink
from agent.triage import triage

FIXTURE = Path(__file__).parent / "fixtures" / "stream_12.jsonl"
HELD = ("WAJO-0004", "WAJO-0008", "WAJO-0026")
AT = datetime(2026, 8, 2, 9, 10, tzinfo=UTC)


def view():
    return Manifest.load(FIXTURE).view(Lane.CALIBRATION)


def held(case_id: str = "WAJO-0008") -> Case:
    """One of the three fixture cases whose route is an ask with a predraft."""
    return view().open(case_id)


def drafting(case_id: str = "WAJO-0008") -> Drafting:
    return drafting_for(held(case_id), intent=triage(held(case_id).event.message).intent)


def test_the_three_held_fixture_cases_all_come_back_with_a_draft() -> None:
    """An ask that arrives with nothing prepared is the gap this phase closes."""
    for case_id in HELD:
        made = drafting(case_id)
        assert made.ok, made.describe()
        assert made.draft.body.strip()


def test_a_draft_cites_the_facts_it_stands_on() -> None:
    made = drafting()
    origins = {fact.origin for fact in made.draft.facts}

    assert made.draft.subject.startswith("Re: ")
    assert made.draft.recipient == "claire@nexustalent.synthetic.example"
    assert {"mail", "thread"} <= origins
    assert "subject" in {fact.label for fact in made.draft.facts}


def test_a_draft_exposes_the_question_it_cannot_answer() -> None:
    """The answer belongs to the user, so the draft quotes the ask and marks the gap."""
    made = drafting()

    assert len(made.draft.unresolved) == 1
    assert made.draft.unresolved[0].startswith("question 1:")
    assert "[needs your answer: question 1]" in made.draft.body
    assert "Are you available" in made.draft.body


def test_a_gap_is_visible_in_the_lines_a_human_reads() -> None:
    shown = "\n".join(drafting().draft.lines())

    assert "nothing is sent" in shown
    assert "gaps (1)" in shown
    assert "facts:" in shown


def test_the_salutation_follows_the_example_the_user_wrote_in() -> None:
    """Style is not decoration: the greeting is the one the retrieved example opens with."""
    case = held()
    borrowed = SentExample(
        source_message_id="msg-sent-003",
        recipient="recruiter@talentsearch.synthetic.example",
        intent="recruiter follow-up",
        text="Hey Amanda,\n\nThanks for reaching out.\n\nBest,\nAydin",
        sent_at="2026-07-25T16:30:00Z",
    )
    style = retrieve_style([borrowed], sender=case.event.message.sender.email, intent="recruiter follow-up")
    drafted = draft_reply(case, style)

    assert drafted.body.startswith("Hey Claire,")
    assert any(fact.origin == "style" for fact in drafted.facts)


def test_a_draft_falls_back_to_the_mail_when_there_is_no_example() -> None:
    drafted = draft_reply(held(), Style())

    assert drafted.body.startswith("Hi Claire,")
    assert not [fact for fact in drafted.facts if fact.origin == "style"]


def test_a_draft_is_addressed_to_whoever_wrote_and_is_never_a_send() -> None:
    made = drafting()
    params = made.draft.params()

    assert params["to"] == ("claire@nexustalent.synthetic.example",)
    assert made.draft.no_send
    assert not [tool for tool in DRAFTING_TOOLS if tool == "send_email" and params["to"] == ()]


def test_the_approved_draft_is_the_draft_that_is_committed() -> None:
    """End to end through the real contract: prepare, authorize, commit one draft."""
    mailbox = SimulatedMailbox()
    registry = build_registry(mailbox)
    case = held()
    message = case.event.message
    decision = route_decision(
        case,
        triage(message),
        Proposal(
            route=Route.ASK_FIRST_WITH_PREDRAFT,
            action_id="email.create_draft",
            tool_name="create_draft",
            params={},
            rationale="test",
        ),
        "test",
        source="test",
    )
    assert decision.predraft is not None

    prepared = registry.prepare(
        case_id=case.case_id,
        message_id=message.message_id,
        route=decision.route,
        action_id=decision.action_id,
        tool_name=decision.tool_name,
        params=decision.params,
    )
    assert not prepared.blocked, prepared.summary()
    with pytest.raises(ApprovalRequired):
        registry.authorize(prepared, verdict_routes=decision.verdict.allowed_routes)

    authorization = registry.authorize(
        prepared,
        approval=Approval(prepared_digest=prepared.digest),
        verdict_routes=decision.verdict.allowed_routes,
    )
    receipt = registry.commit(prepared, authorization, at=AT)

    assert [effect.tool for effect in receipt.effects] == ["create_draft"]
    assert mailbox.drafts[message.message_id].body == decision.predraft.body
    assert mailbox.sends == []


def test_a_draft_that_cannot_be_shown_escalates_instead_of_asking(monkeypatch) -> None:
    """A reply the user cannot trust is worse than a mail handed back."""
    case = held()
    made = drafting()
    withdrawn = replace(made.draft, recipient="someone.else@example.com")
    broken = Drafting(
        draft=withdrawn,
        validation=validate_draft(withdrawn, case),
        style=made.style,
    )
    assert broken.validation.code == DraftCode.WRONG_RECIPIENT  # the fixture is the point
    monkeypatch.setattr(policy, "drafting_for", lambda case, *, intent: broken)

    decision = route_decision(
        case,
        triage(case.event.message),
        Proposal(
            route=Route.ASK_FIRST_WITH_PREDRAFT,
            action_id="email.create_draft",
            tool_name="create_draft",
            params={},
            rationale="test",
        ),
        "test",
        source="test",
    )

    assert decision.route is Route.ESCALATE
    assert decision.predraft is None
    assert DraftCode.WRONG_RECIPIENT in decision.reason


def test_the_trace_carries_the_draft_without_the_reply(tmp_path: Path) -> None:
    """A draft is mail text: the record keeps its shape, sizes and labels, not its words."""
    path = tmp_path / "graph.jsonl"
    sink = TraceSink(path)
    asyncio.run(run_graph(view(), seed=7, mask=False, trace=sink))
    sink.close()

    decisions = [
        json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()
    ]
    drafts = [line["draft"] for line in decisions if (line.get("draft") or {}).get("chars")]
    assert drafts, "an ask in this lane carries a predraft"
    assert any(item["gaps"] for item in drafts)
    assert any(item["facts"] for item in drafts)
    assert all(item["no_send"] for item in drafts)
    # The one question worth recording about an address is whether it was the right one.
    assert all(item["right_person"] for item in drafts)

    text = path.read_text(encoding="utf-8")
    assert "Thanks for the note" not in text
    for case_id in HELD:
        assert drafting(case_id).draft.body not in text
