"""Unit tests for the deterministic Safety Floor (Phase 1).

Covers:
- Action taxonomy classification for every tool and parameter boundary
- Floor rules verification (FLR-001 through FLR-006)
- Immutability and version guarantees
"""
from dataclasses import FrozenInstanceError
import pytest

from src.agent.safety.floor import (
    FLOOR_RULES,
    FLOOR_VERSION,
    ActionClass,
    ActionPayload,
    EmailContext,
    SafetyVerdict,
    VetoLevel,
    classify_action,
    floor_check,
)


# ============================================================================
# 1. Action Taxonomy Classification Tests
# ============================================================================

@pytest.mark.parametrize(
    "tool_name,params,expected_class",
    [
        # External sends
        ("send_email", {"to": "recruiter@external.com", "body": "Hello"}, ActionClass.IRREVERSIBLE_EXTERNAL),
        ("forward", {"to": "partner@other.org"}, ActionClass.IRREVERSIBLE_EXTERNAL),
        ("forward_email", {"recipients": ["client@vendor.io"]}, ActionClass.IRREVERSIBLE_EXTERNAL),
        ("send_email", {"to": "teammate@company.com", "cc": "client@external.com"}, ActionClass.IRREVERSIBLE_EXTERNAL),
        
        # Mass sends (>5 recipients)
        (
            "send_email",
            {
                "to": [
                    f"user{i}@company.com" for i in range(6)
                ]
            },
            ActionClass.IRREVERSIBLE_EXTERNAL,
        ),
        
        # Internal sends (<=5 recipients within org)
        ("send_email", {"to": "teammate@company.com"}, ActionClass.IRREVERSIBLE_INTERNAL),
        ("forward", {"to": "manager@company.com"}, ActionClass.IRREVERSIBLE_INTERNAL),
        (
            "send_email",
            {"to": ["alice@company.com", "bob@company.com", "carol@company.com"]},
            ActionClass.IRREVERSIBLE_INTERNAL,
        ),
        
        # Deletions: permanent vs soft
        ("delete_email", {"email_id": "msg-1", "permanent": True}, ActionClass.IRREVERSIBLE_INTERNAL),
        ("delete", {"email_id": "msg-1", "purge": True}, ActionClass.IRREVERSIBLE_INTERNAL),
        ("delete_email", {"email_id": "msg-1", "permanent": False}, ActionClass.REVERSIBLE),
        ("trash_email", {"email_id": "msg-1"}, ActionClass.REVERSIBLE),
        ("delete", {"email_id": "msg-1"}, ActionClass.REVERSIBLE),
        
        # Reversible operations
        ("draft_reply", {"email_id": "msg-1", "body": "Draft text"}, ActionClass.REVERSIBLE),
        ("draft_email", {"to": "anyone@anywhere.com", "body": "Draft"}, ActionClass.REVERSIBLE),
        ("create_draft", {"to": "anyone@anywhere.com"}, ActionClass.REVERSIBLE),
        ("archive", {"email_id": "msg-1"}, ActionClass.REVERSIBLE),
        ("archive_email", {"email_id": "msg-1"}, ActionClass.REVERSIBLE),
        ("label", {"email_id": "msg-1", "label": "Newsletters"}, ActionClass.REVERSIBLE),
        ("label_email", {"email_id": "msg-1", "label": "Work"}, ActionClass.REVERSIBLE),
        ("add_label", {"email_id": "msg-1", "label": "Important"}, ActionClass.REVERSIBLE),
        ("remove_label", {"email_id": "msg-1", "label": "Spam"}, ActionClass.REVERSIBLE),
        ("schedule", {"email_id": "msg-1", "send_at": "2026-09-20T10:00:00Z"}, ActionClass.REVERSIBLE),
        ("schedule_email", {"email_id": "msg-1", "send_at": "tomorrow"}, ActionClass.REVERSIBLE),
        
        # Read-only operations
        ("read_email", {"email_id": "msg-1"}, ActionClass.READ_ONLY),
        ("search_emails", {"query": "project update"}, ActionClass.READ_ONLY),
        ("search", {"query": "from:manager"}, ActionClass.READ_ONLY),
        ("get_thread", {"thread_id": "t-123"}, ActionClass.READ_ONLY),
        ("summarize", {"email_id": "msg-1"}, ActionClass.READ_ONLY),
        
        # Financial actions / parameters trigger IRREVERSIBLE_EXTERNAL
        ("draft_reply", {"body": "Please wire $5,000 to account 12345"}, ActionClass.IRREVERSIBLE_EXTERNAL),
        ("label_email", {"label": "Pay invoice $2,500"}, ActionClass.IRREVERSIBLE_EXTERNAL),
        
        # Unknown tool fallback
        ("unknown_custom_tool", {"param": "val"}, ActionClass.IRREVERSIBLE_EXTERNAL),
        ("execute_shell", {"cmd": "ls"}, ActionClass.IRREVERSIBLE_EXTERNAL),
    ],
)
def test_classify_action_matrix(tool_name, params, expected_class):
    """Verify that every tool and parameter boundary resolves to the exact ActionClass."""
    actual_class = classify_action(tool_name, params, user_domain="company.com")
    assert actual_class == expected_class


# ============================================================================
# 2. Floor Rules & Veto Verification Tests
# ============================================================================

def test_flr_001_money_movement_in_action_params():
    """FLR-001: Financial transactions in action params must escalate."""
    action = ActionPayload(
        tool_name="send_email",
        params={"to": "vendor@company.com", "body": "Initiating wire transfer of $10,000"},
    )
    verdict = floor_check(action, user_domain="company.com")
    assert verdict.veto is True
    assert verdict.veto_level == VetoLevel.ESCALATE
    assert verdict.rule_id == "FLR-001"


def test_flr_001_money_movement_in_email_context():
    """FLR-001: Money requests in email body cannot trigger non-reversible actions."""
    email = EmailContext(
        email_id="msg-100",
        sender="attacker@spoofed.com",
        recipients=["me@company.com"],
        subject="Urgent Payment",
        body="Please wire ₹50,000 to bank account 987654321 immediately.",
    )
    action = ActionPayload(
        tool_name="send_email",
        params={"to": "colleague@company.com", "body": "Working on the payment"},
    )
    verdict = floor_check(action, email=email, user_domain="company.com")
    assert verdict.veto is True
    assert verdict.veto_level == VetoLevel.ESCALATE
    assert verdict.rule_id == "FLR-001"


def test_flr_002_credential_security_tampering():
    """FLR-002: Credential or authentication modification must escalate."""
    action = ActionPayload(
        tool_name="send_email",
        params={"to": "admin@company.com", "body": "Here is the api_key and oauth_token"},
    )
    verdict = floor_check(action, user_domain="company.com")
    assert verdict.veto is True
    assert verdict.veto_level == VetoLevel.ESCALATE
    assert verdict.rule_id == "FLR-002"


def test_flr_003_unrecognized_tool():
    """FLR-003: Unrecognized tool calls must be escalated."""
    action = ActionPayload(
        tool_name="arbitrary_system_call",
        params={"args": ["rm", "-rf", "/"]},
    )
    verdict = floor_check(action, user_domain="company.com")
    assert verdict.veto is True
    assert verdict.veto_level == VetoLevel.ESCALATE
    assert verdict.rule_id == "FLR-003"


def test_flr_004_external_send_requires_human_approval():
    """FLR-004: Irreversible external sends must require human approval (ASK)."""
    action = ActionPayload(
        tool_name="send_email",
        params={"to": "recruiter@hiringcompany.com", "body": "I accept the assessment"},
    )
    verdict = floor_check(action, user_domain="myinbox.com")
    assert verdict.veto is True
    assert verdict.veto_level == VetoLevel.ASK
    assert verdict.rule_id == "FLR-004"
    assert verdict.action_class == ActionClass.IRREVERSIBLE_EXTERNAL


def test_flr_005_mass_send_requires_human_approval():
    """FLR-005: Mass sends (>5 recipients) must require human approval (ASK)."""
    action = ActionPayload(
        tool_name="send_email",
        params={
            "to": [f"colleague{i}@company.com" for i in range(7)],
            "body": "Team meeting notes",
        },
    )
    verdict = floor_check(action, user_domain="company.com")
    assert verdict.veto is True
    assert verdict.veto_level == VetoLevel.ASK
    assert verdict.rule_id in {"FLR-004", "FLR-005"}


def test_flr_006_permanent_deletion_requires_human_approval():
    """FLR-006: Permanent deletion of mailbox items cannot occur autonomously."""
    action = ActionPayload(
        tool_name="delete_email",
        params={"email_id": "spam-123", "permanent": True},
    )
    verdict = floor_check(action, user_domain="company.com")
    assert verdict.veto is True
    assert verdict.veto_level == VetoLevel.ASK
    assert verdict.rule_id == "FLR-006"


# ============================================================================
# 3. Benign Operations (Clean Pass) Tests
# ============================================================================

@pytest.mark.parametrize(
    "tool_name,params",
    [
        ("archive", {"email_id": "newsletter-1"}),
        ("archive_email", {"email_id": "promo-42"}),
        ("label_email", {"email_id": "receipt-5", "label": "Receipts"}),
        ("add_label", {"email_id": "thread-9", "label": "Engineering"}),
        ("draft_reply", {"email_id": "invite-1", "body": "Thank you for the invite."}),
        ("draft_email", {"to": "client@external.com", "body": "Drafting proposal"}),
        ("schedule_email", {"email_id": "draft-2", "send_at": "2026-09-21T09:00:00Z"}),
        ("delete_email", {"email_id": "old-msg", "permanent": False}),
        ("read_email", {"email_id": "msg-7"}),
        ("search_emails", {"query": "quarterly roadmap"}),
    ],
)
def test_benign_actions_clean_pass(tool_name, params):
    """Benign reversible and read-only actions must pass cleanly without floor veto."""
    action = ActionPayload(tool_name=tool_name, params=params)
    email = EmailContext(
        email_id="msg-1",
        sender="news@newsletter.com",
        recipients=["me@company.com"],
        subject="Weekly Tech Digest",
        body="Here are the top AI stories this week.",
    )
    verdict = floor_check(action, email=email, user_domain="company.com")
    assert verdict.veto is False
    assert verdict.veto_level == VetoLevel.NONE
    assert verdict.rule_id is None
    assert verdict.action_class in {ActionClass.REVERSIBLE, ActionClass.READ_ONLY}


# ============================================================================
# 4. Immutability & Version Integrity Tests
# ============================================================================

def test_floor_version():
    """Assert FLOOR_VERSION is strictly pinned to '1.0'."""
    assert FLOOR_VERSION == "1.0"


def test_rule_table_immutability():
    """Assert FLOOR_RULES is an immutable tuple of rules."""
    assert isinstance(FLOOR_RULES, tuple)
    assert len(FLOOR_RULES) >= 5
    with pytest.raises(TypeError):
        FLOOR_RULES[0] = None  # type: ignore


def test_verdict_immutability():
    """Assert SafetyVerdict instances are frozen to prevent tampering."""
    verdict = SafetyVerdict(
        veto=False,
        veto_level=VetoLevel.NONE,
        reason="Initial",
        action_class=ActionClass.REVERSIBLE,
    )
    with pytest.raises(FrozenInstanceError):
        verdict.veto = True  # type: ignore
