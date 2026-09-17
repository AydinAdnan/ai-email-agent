"""Phase 3.3: the simulated tools and the prepare/authorize/commit contract.

The plan's check is here: a label+notify on the AWS fixture produces one receipt and
zero sends.
"""
import asyncio
import io
import json
from datetime import UTC, datetime
from pathlib import Path

import pytest

from agent.dataset import Manifest
from agent.events import Direction, Message, SenderIdentity
from agent.safety.floor import ActionPayload, EmailContext, Route, floor_check
from agent.sim.runner import run_simulation
from agent.tools.email_tools import (
    ACTION_TO_TOOL,
    SimulatedMailbox,
    build_registry,
)
from agent.tools.registry import (
    Approval,
    ApprovalRequired,
    AuthorizationRefused,
    StaleApproval,
    ToolError,
    UnknownTool,
)

FIXTURE = Path(__file__).parent / "fixtures" / "stream_12.jsonl"
AWS_CASE = "WAJO-0005"
NOW = datetime(2026, 8, 1, 9, 0, tzinfo=UTC)


def mailbox() -> SimulatedMailbox:
    return SimulatedMailbox()


def registry_for(mail: SimulatedMailbox | None = None):
    return build_registry(mail if mail is not None else mailbox())


def prepare(reg, *, route=Route.PROCEED_SILENTLY, tool="label", params=None, action="email.apply_label"):
    return reg.prepare(
        case_id="mail-0001",
        message_id="msg-1",
        route=route,
        action_id=action,
        tool_name=tool,
        params=params if params is not None else {"label": "Newsletter"},
    )


def test_the_aws_fixture_labels_notifies_and_never_pays() -> None:
    """The plan's check: one receipt, zero sends, no payment tool anywhere."""
    mail = mailbox()
    manifest = Manifest.load(FIXTURE)
    case = next(item for item in manifest.cases if item.case_id == AWS_CASE)
    out = io.StringIO()
    outcome = asyncio.run(
        run_simulation(manifest.view(case.lane), seed=7, out=out, mailbox=mail)
    )

    receipt = next(item for item in outcome.receipts if item.case_id == AWS_CASE)
    effects = {effect.tool: effect.detail for effect in receipt.effects}
    assert set(effects) == {"label", "notify"}
    assert effects["label"] == "labelled Finance/Cloud"
    assert mail.labels_for(case.event.message.message_id) == ("Finance/Cloud",)
    assert len(mail.notifications) == 2  # the AWS bill and the CloudWatch notice
    assert outcome.effects("send_email") == 0
    assert mail.sends == []
    assert "Finance/Cloud" in mail.labels[case.event.message.message_id]
    assert receipt.route is Route.PROCEED_AND_NOTIFY
    assert "label:labelled Finance/Cloud, notify:notified the user" in out.getvalue()


def test_every_tool_the_registry_holds_is_a_tool_the_floor_knows() -> None:
    """A tool the floor does not know would escalate every action that used it."""
    reg = registry_for()
    verdicts = {
        name: floor_check(
            ActionPayload(tool_name=name, params={}),
            email=EmailContext(
                email_id="e-1",
                sender="a@b.test",
                recipients=("me@b.test",),
                subject="s",
                body="b",
            ),
        )
        for name in reg.tool_names
    }
    for name, verdict in verdicts.items():
        assert "Unrecognized tool" not in (verdict.reason or ""), f"{name} is not known to the floor"


def test_prepare_touches_nothing() -> None:
    mail = mailbox()
    reg = registry_for(mail)
    prepared = prepare(reg)
    assert prepared.steps and not prepared.blocked
    assert mail.labels == {} and mail.notifications == [] and mail.archived == []


def test_commit_writes_one_receipt_for_the_whole_action() -> None:
    mail = mailbox()
    reg = registry_for(mail)
    prepared = prepare(reg, route=Route.PROCEED_AND_NOTIFY)
    authorization = reg.authorize(prepared, verdict_routes={Route.PROCEED_AND_NOTIFY})
    receipt = reg.commit(prepared, authorization, at=NOW)
    assert len(prepared.steps) == 2
    assert receipt.receipt_id.startswith("rcpt-")
    assert [effect.tool for effect in receipt.effects] == ["label", "notify"]
    assert mail.labels["msg-1"] == ["Newsletter"]
    assert len(mail.notifications) == 1


def test_a_route_the_floor_disallowed_is_refused() -> None:
    reg = registry_for()
    prepared = prepare(reg, route=Route.PROCEED_SILENTLY)
    with pytest.raises(AuthorizationRefused):
        reg.authorize(prepared, verdict_routes={Route.ESCALATE})


def test_escalation_commits_nothing() -> None:
    mail = mailbox()
    reg = registry_for(mail)
    prepared = reg.prepare(
        case_id="mail-0001",
        message_id="msg-1",
        route=Route.ESCALATE,
        action_id="unsupported",
        tool_name=None,
    )
    assert prepared.steps == ()
    with pytest.raises(AuthorizationRefused):
        reg.authorize(prepared)


def test_an_ask_route_waits_for_an_approval_that_matches() -> None:
    mail = mailbox()
    reg = registry_for(mail)
    prepared = prepare(reg, route=Route.ASK_FIRST_WITH_PREDRAFT)

    with pytest.raises(ApprovalRequired):
        reg.authorize(prepared)

    with pytest.raises(StaleApproval):
        reg.authorize(prepared, approval=Approval(prepared_digest="not-the-digest"))

    authorization = reg.authorize(prepared, approval=Approval(prepared_digest=prepared.digest))
    receipt = reg.commit(prepared, authorization, at=NOW)
    assert receipt.effects and mail.labels["msg-1"] == ["Newsletter"]


def test_an_approval_cannot_be_replayed_onto_different_work() -> None:
    """The digest covers the steps, so approving one label never approves another."""
    reg = registry_for()
    first = prepare(reg, route=Route.ASK_FIRST_WITH_PREDRAFT, params={"label": "Newsletter"})
    second = prepare(reg, route=Route.ASK_FIRST_WITH_PREDRAFT, params={"label": "Finance"})
    assert first.digest != second.digest
    with pytest.raises(StaleApproval):
        reg.authorize(second, approval=Approval(prepared_digest=first.digest))


def test_an_uncommittable_step_is_reported_not_dropped() -> None:
    """A draft with no body is a blocked step on the receipt, not a silent no-op."""
    mail = mailbox()
    reg = registry_for(mail)
    prepared = reg.prepare(
        case_id="mail-0001",
        message_id="msg-1",
        route=Route.PROCEED_AND_NOTIFY,
        action_id="email.create_draft",
        tool_name="create_draft",
        params={},
    )
    assert prepared.steps and [step.tool for step in prepared.steps] == ["notify"]
    assert prepared.blocked == ("create_draft: body is required",)
    authorization = reg.authorize(prepared, verdict_routes={Route.PROCEED_AND_NOTIFY})
    receipt = reg.commit(prepared, authorization, at=NOW)
    assert receipt.blocked == prepared.blocked
    assert "blocked: create_draft: body is required" in receipt.summary()


def test_an_unknown_tool_is_blocked_rather_than_crashing() -> None:
    reg = registry_for()
    prepared = reg.prepare(
        case_id="mail-0001",
        message_id="msg-1",
        route=Route.PROCEED_SILENTLY,
        action_id="finance.pay_invoice",
        tool_name="pay_invoice",
        params={"amount": "250"},
    )
    assert prepared.steps == ()
    assert prepared.blocked and prepared.blocked[0].startswith("pay_invoice:")


def test_the_registry_refuses_two_tools_with_one_name() -> None:
    mail = mailbox()
    tools = build_registry(mail)
    with pytest.raises(ToolError):
        type(tools)([tools.tool("label"), tools.tool("label")])


def test_an_unknown_tool_name_says_what_does_exist() -> None:
    with pytest.raises(UnknownTool) as caught:
        registry_for().tool("delete_everything")
    assert "label" in str(caught.value)


def test_a_send_needs_a_recipient_and_a_body_but_sends_nothing() -> None:
    mail = mailbox()
    reg = registry_for(mail)
    with pytest.raises(ToolError):
        reg.tool("send_email").check({"body": "hello"})
    with pytest.raises(ToolError):
        reg.tool("send_email").check({"to": ["a@b.test"]})

    prepared = reg.prepare(
        case_id="mail-0001",
        message_id="msg-1",
        route=Route.PROCEED_SILENTLY,
        action_id="email.send",
        tool_name="send_email",
        params={"to": ["a@b.test"], "body": "hello"},
    )
    authorization = reg.authorize(prepared, verdict_routes={Route.PROCEED_SILENTLY})
    receipt = reg.commit(prepared, authorization, at=NOW)
    assert receipt.effects[0].detail.endswith("(nothing left the mailbox)")
    assert mail.sends == []


def test_the_action_id_map_covers_the_tools() -> None:
    """One vocabulary: a dataset action id either names a tool or has none on purpose."""
    assert ACTION_TO_TOOL["email.apply_label"] == "label"
    assert ACTION_TO_TOOL["email.create_draft"] == "create_draft"
    # No forward tool exists, so the floor's unknown-tool rule escalates it.
    assert "email.forward" not in ACTION_TO_TOOL
    assert "finance.pay_invoice" not in ACTION_TO_TOOL


def test_the_run_prepares_every_ask_and_commits_none_of_them() -> None:
    manifest = Manifest.load(FIXTURE)
    outcome = asyncio.run(
        run_simulation(manifest.view(manifest.cases[0].lane), seed=7, out=io.StringIO())
    )
    waiting = outcome.awaiting_approval
    assert len(waiting) == outcome.route_counts["ASK_FIRST_WITH_PREDRAFT"] == 3
    assert all(item.route is Route.ASK_FIRST_WITH_PREDRAFT for item in waiting)
    # Every case that waited for a human, plus every escalation, is a refusal.
    assert len(outcome.refusals) == outcome.interrupts == 7
    assert all(item.case_id not in {r.case_id for r in outcome.receipts} for item in waiting)
    assert outcome.effects("send_email") == 0


def test_a_plain_mail_stream_works_with_no_dataset_fields(tmp_path) -> None:
    """The goal: point it at sender, subject and body, and nothing else."""
    rows = [
        {
            "sender": {"email": "news@engweekly.example", "display_name": "Engineering Weekly"},
            "to": ["aydin@techcorp.example"],
            "subject": "Engineering Weekly Issue #204: Distributed Systems Patterns",
            "body": "Unsubscribe from this newsletter at any time.",
        },
        {
            "from": "receipts@cornercafe.example",
            "to": ["aydin@techcorp.example"],
            "subject": "Your receipt from Corner Cafe ($14.50)",
            "body": "Thank you for your purchase. Transaction Date: 2026-07-28. Total: $14.50",
        },
        {
            "from": "elena@techcorp.example",
            "to": ["aydin@techcorp.example"],
            "subject": "Quick catchup this week?",
            "body": "Would you have time for a quick sync on Thursday?",
        },
    ]
    path = tmp_path / "mail.jsonl"
    path.write_text("\n".join(json.dumps(row) for row in rows) + "\n", encoding="utf-8")

    manifest = Manifest.load(path, mail_only=True)
    assert [case.case_id for case in manifest.cases] == ["mail-0001", "mail-0002", "mail-0003"]
    assert not any(case.labelled for case in manifest.cases)
    with pytest.raises(ValueError):
        _ = manifest.cases[0].labels

    mail = mailbox()
    out = io.StringIO()
    outcome = asyncio.run(run_simulation(manifest.view(manifest.cases[0].lane), seed=7, out=out, mailbox=mail))
    assert outcome.processed == 3
    assert mail.labels_for("msg-0001") == ("Newsletter",)
    assert mail.labels_for("msg-0002") == ("Finance/Receipts",)
    assert outcome.effects("send_email") == 0
    assert "labels:   none" not in out.getvalue(), "labels are off unless --show-labels"


def test_a_message_needs_no_dataset_to_be_acted_on() -> None:
    """A tool takes mail, not a case: the same call works for any message."""
    mail = mailbox()
    reg = registry_for(mail)
    message = Message(
        message_id="msg-free",
        thread_id="th-free",
        sender=SenderIdentity(email="someone@example.test"),
        recipients=("me@example.test",),
        direction=Direction.INBOUND,
        subject="Hello",
        body="body",
    )
    prepared = reg.prepare(
        case_id=message.message_id,
        message_id=message.message_id,
        route=Route.PROCEED_SILENTLY,
        action_id="email.archive",
        tool_name="archive",
        params={},
    )
    assert prepared.steps[0].params["email_id"] == "msg-free"
    authorization = reg.authorize(prepared, verdict_routes={Route.PROCEED_SILENTLY})
    reg.commit(prepared, authorization, at=NOW)
    assert mail.archived == ["msg-free"]
