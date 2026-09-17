import asyncio
from dataclasses import replace
from pathlib import Path

import pytest

from agent.dataset import Lane, Manifest
from agent.events import Message
from agent.gateway import Proposal, ProposalGateway, RuleProvider
from agent.graph import GraphError, GraphSession
from agent.safety.floor import Route
from agent.tools.email_tools import TOOL_CLASSES, SimulatedMailbox
from agent.tools.registry import ToolRegistry
from agent.triage import Triage

FIXTURE = Path(__file__).parent / "fixtures" / "stream_12.jsonl"
ASKED = "WAJO-0026"
NOTIFIED = "WAJO-0005"
ESCALATED = "WAJO-0011"


class Crash(RuntimeError):
    """A run that dies where it stands."""


class Crashing(ToolRegistry):
    """A registry that dies inside commit, to see what a resume recovers."""

    def __init__(self, mailbox: SimulatedMailbox) -> None:
        super().__init__(tool_class(mailbox) for tool_class in TOOL_CLASSES)
        self.mailbox = mailbox
        self.mode = ""

    def commit(self, prepared, authorization, *, at):
        if self.mode == "before":
            raise Crash("died before the work ran")
        receipt = super().commit(prepared, authorization, at=at)
        if self.mode == "after":
            raise Crash("died after the work ran, before the receipt was recorded")
        return receipt


class Flaky(ProposalGateway):
    """A provider that answers differently the second time it is asked about a mail."""

    def __init__(self) -> None:
        super().__init__(RuleProvider())
        self.asked = 0

    async def propose(self, message: Message, hints: Triage) -> Proposal:
        answer = await super().propose(message, hints)
        if message.message_id != f"msg-in-{ASKED.lower()}":
            return answer
        self.asked += 1
        if self.asked == 1:
            return answer
        return replace(answer, route=Route.PROCEED_AND_NOTIFY)


def session(**kwargs) -> GraphSession:
    lane = Manifest.load(FIXTURE).view(Lane.CALIBRATION)
    return GraphSession(lane, seed=7, mask=False, **kwargs)


def approval_for(item) -> dict[str, str]:
    """The yes a reviewer would send back for the work they were shown."""
    return {"approved_by": "user", "prepared_digest": item.digest}


def test_a_held_decision_resumes_with_an_approval_and_commits_once():
    run = session()
    asyncio.run(run.run())
    held = {item.case_id: item for item in run.outcome.held}
    assert ASKED in held

    result = asyncio.run(run.resume(ASKED, approval_for(held[ASKED])))
    assert result.status == "committed"
    assert result.receipt is not None
    assert result.receipt.prepared_digest == held[ASKED].digest
    assert len(run.outcome.held) == len(held) - 1
    assert ASKED in {item.case_id for item in run.outcome.receipts}
    assert ASKED not in run.outcome.interrupts
    assert ASKED not in {item.case_id for item in run.outcome.held}


def test_an_approval_for_other_work_is_refused_as_stale():
    run = session()
    asyncio.run(run.run())
    held = {item.case_id: item for item in run.outcome.held}
    other = next(item for item in held.values() if item.case_id != ASKED)

    result = asyncio.run(run.resume(ASKED, approval_for(other)))
    assert result.status == "APPROVAL_STALE"
    assert result.receipt is None
    assert ASKED not in {item.case_id for item in run.outcome.receipts}
    assert any(ASKED in item for item in run.outcome.refusals)


def test_a_decision_that_moved_between_asking_and_answering_is_refused():
    """The provider answers differently on the second look: the yes no longer fits."""
    flaky = Flaky()
    run = session(gateway=flaky)
    asyncio.run(run.run())
    held = {item.case_id: item for item in run.outcome.held}
    assert ASKED in held

    result = asyncio.run(run.resume(ASKED, approval_for(held[ASKED])))
    assert result.status == "APPROVAL_STALE"
    assert "the work changed" in result.reason
    assert result.receipt is None


def test_resuming_a_decision_that_never_waited_says_so():
    run = session()
    asyncio.run(run.run())
    committed = next(item for item in run.outcome.receipts if item.route.value == "PROCEED_AND_NOTIFY")
    result = asyncio.run(run.resume(committed.case_id, {"approved_by": "user", "prepared_digest": "x"}))
    assert result.status == "NOT_WAITING"
    assert run.outcome.receipts.count(committed) == 1


def test_a_rejection_commits_nothing():
    run = session()
    asyncio.run(run.run())
    held = {item.case_id: item for item in run.outcome.held}
    before = len(run.outcome.receipts)

    result = asyncio.run(run.resume(ASKED, None))
    assert result.status == "REJECTED"
    assert len(run.outcome.receipts) == before
    assert held[ASKED].case_id in run.outcome.interrupts


def test_an_escalation_cannot_be_approved():
    """A yes is not an answer where the floor sent it to a human to decide."""
    run = session()
    asyncio.run(run.run())
    assert run.outcome.interrupts[ESCALATED] == "AUTHORIZATION_REFUSED"

    result = asyncio.run(
        run.resume(ESCALATED, {"approved_by": "user", "prepared_digest": "anything"})
    )
    assert result.status == "AUTHORIZATION_REFUSED"
    assert result.receipt is None
    assert ESCALATED not in {item.case_id for item in run.outcome.receipts}


def test_resuming_a_decision_that_does_not_exist_fails_with_its_name():
    run = session()
    with pytest.raises(GraphError, match="no checkpoint"):
        asyncio.run(run.resume("WAJO-9999", None))


@pytest.mark.parametrize("mode", ["before", "after"])
def test_a_crash_inside_a_commit_recovers_to_exactly_one_effect(mode: str):
    """The plan's crash matrix: whether the work ran or not, a resume applies it once."""
    mailbox = SimulatedMailbox()
    registry = Crashing(mailbox)
    run = session(registry=registry, mailbox=mailbox)
    registry.mode = mode
    with pytest.raises(GraphError, match="failed in the graph"):
        asyncio.run(run.run())

    # The first decision that changes anything is the AWS bill: label, then notify.
    crashed = len(mailbox.notifications), len(mailbox.labels)
    assert crashed == ((1, 1) if mode == "after" else (0, 0))

    registry.mode = ""
    result = asyncio.run(run.resume(NOTIFIED, None))
    assert result.status == "committed", result.reason
    assert (len(mailbox.notifications), len(mailbox.labels)) == (1, 1)
    assert result.receipt is not None
    assert [effect.tool for effect in result.receipt.effects] == ["label", "notify"]
    assert [item.case_id for item in run.outcome.receipts].count(NOTIFIED) == 1


def test_a_crash_before_the_work_ran_leaves_the_decision_waiting():
    run = session()
    asyncio.run(run.run())
    held = {item.case_id: item for item in run.outcome.held}
    # Nothing has run: the decision is prepared, and its thread still holds the question.
    assert held[ASKED].blocked
    values = asyncio.run(run._checkpointed({"configurable": {"thread_id": run.thread_for(ASKED)}}))
    assert values["interrupt"]["code"] == "APPROVAL_REQUIRED"
    assert values.get("receipt", {}) == {}
    assert ASKED not in {item.case_id for item in run.outcome.receipts}


def test_the_same_work_is_never_applied_twice():
    """The effect log is what makes a retry safe: a second commit returns the same effects."""
    mailbox = SimulatedMailbox()
    registry = ToolRegistry(tool_class(mailbox) for tool_class in TOOL_CLASSES)
    run = session(registry=registry, mailbox=mailbox)
    asyncio.run(run.run())
    prepared = next(item for item in run.outcome.receipts if item.case_id == NOTIFIED)
    action = run.context.prepared[NOTIFIED]

    before = (len(mailbox.notifications), len(mailbox.labels))
    first = registry.commit(action, registry.authorize(action), at=run.context.clock.now())
    second = registry.commit(action, registry.authorize(action), at=run.context.clock.now())
    # Neither attempt changes anything, and both describe the work the run already did.
    assert first == second == prepared
    assert (len(mailbox.notifications), len(mailbox.labels)) == before
