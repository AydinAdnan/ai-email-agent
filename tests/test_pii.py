"""Unit tests for Presidio PII Masker (Phase 2)."""
import pytest
from src.agent.pii.masker import (
    PresidioMasker,
    get_token_map,
    mask_for_llm,
)


def test_standard_entities_masked():
    """Verify common PII entities (email, phone, person, location) are masked."""
    subject = "Meeting with Sarah Connor in Chicago"
    body = "Please reach out to sarah.connor@cyberdyne.com or call 555-123-4567."
    
    masked_sub, masked_bod, token_map = mask_for_llm(subject, body, thread_id="test_std")
    
    assert "Sarah Connor" not in masked_sub
    assert "<PERSON_1>" in masked_sub
    assert "sarah.connor@cyberdyne.com" not in masked_bod
    assert "<EMAIL_ADDRESS_1>" in masked_bod
    assert "555-123-4567" not in masked_bod
    assert "<PHONE_NUMBER_1>" in masked_bod


def test_custom_indian_entities_masked():
    """Verify Indian PAN, Aadhaar, and Passport numbers are masked."""
    body = (
        "PAN: ABCDE1234F\n"
        "Aadhaar: 4567 8901 2345\n"
        "Passport: K1234567"
    )
    _, masked_bod, token_map = mask_for_llm("IDs", body, thread_id="test_in_ids")
    
    assert "ABCDE1234F" not in masked_bod
    assert "<IN_PAN_1>" in masked_bod
    assert "4567 8901 2345" not in masked_bod
    assert "<IN_AADHAAR_1>" in masked_bod
    assert "K1234567" not in masked_bod
    assert "<IN_PASSPORT_1>" in masked_bod


def test_custom_domain_entities_masked():
    """Verify project codenames and ticket IDs are masked."""
    body = "Reviewing ticket ACME-48201 for Project Titan deployment."
    _, masked_bod, token_map = mask_for_llm("Ticket Update", body, thread_id="test_custom")
    
    assert "ACME-48201" not in masked_bod
    assert "<TICKET_ID_1>" in masked_bod
    assert "Project Titan" not in masked_bod
    assert "<PROJECT_CODENAME_1>" in masked_bod


def test_per_thread_consistency():
    """Verify entities receive identical tokens across multiple turns in the same thread."""
    thread_id = "thread_turn_consistency"
    
    # Turn 1
    _, body_1, _ = mask_for_llm("", "Hello from Robert Bruce (robert@scot.org)", thread_id=thread_id)
    assert "<PERSON_1>" in body_1
    assert "<EMAIL_ADDRESS_1>" in body_1
    
    # Turn 2: same entity appears again
    _, body_2, _ = mask_for_llm("", "Robert Bruce requested follow-up at robert@scot.org", thread_id=thread_id)
    assert "<PERSON_1>" in body_2
    assert "<EMAIL_ADDRESS_1>" in body_2
    
    # Check that another person gets index 2
    _, body_3, _ = mask_for_llm("", "William Wallace joined the call", thread_id=thread_id)
    assert "<PERSON_2>" in body_3


def test_unmasking():
    """Verify unmask_text restores original values accurately."""
    masker = PresidioMasker.get_instance()
    thread_id = "thread_unmask"
    
    text = "Contact Alice at alice@acme.com."
    masked, token_map = masker.mask_text(text, thread_id=thread_id)
    restored = masker.unmask_text(masked, thread_id=thread_id)
    
    assert restored == text
