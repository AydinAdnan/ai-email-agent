"""Unit tests for Presidio PII Masker (Phase 2)."""
from src.agent.pii.masker import (
    _MAX_THREADS,
    PresidioMasker,
    forget_thread,
    get_token_map,
    mask_for_llm,
)


def test_standard_entities_masked():
    """Verify common PII entities (email, phone, person, location) are masked."""
    subject = "Meeting with Sarah Connor in Chicago"
    body = "Please reach out to sarah.connor@cyberdyne.com or call 555-123-4567."

    masked_sub, masked_bod = mask_for_llm(subject, body, thread_id="test_std")

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
    _, masked_bod = mask_for_llm("IDs", body, thread_id="test_in_ids")

    assert "ABCDE1234F" not in masked_bod
    assert "<IN_PAN_1>" in masked_bod
    assert "4567 8901 2345" not in masked_bod
    assert "<IN_AADHAAR_1>" in masked_bod
    assert "K1234567" not in masked_bod
    assert "<IN_PASSPORT_1>" in masked_bod


def test_custom_domain_entities_masked():
    """Verify project codenames and ticket IDs are masked."""
    body = "Reviewing ticket ACME-48201 for Project Titan deployment."
    _, masked_bod = mask_for_llm("Ticket Update", body, thread_id="test_custom")

    assert "ACME-48201" not in masked_bod
    assert "<TICKET_ID_1>" in masked_bod
    assert "Project Titan" not in masked_bod
    assert "<PROJECT_CODENAME_1>" in masked_bod


def test_per_thread_consistency():
    """Verify entities receive identical tokens across multiple turns in the same thread."""
    thread_id = "thread_turn_consistency"

    # Turn 1
    _, body_1 = mask_for_llm("", "Hello from Robert Bruce (robert@scot.org)", thread_id=thread_id)
    assert "<PERSON_1>" in body_1
    assert "<EMAIL_ADDRESS_1>" in body_1

    # Turn 2: same entity appears again
    _, body_2 = mask_for_llm("", "Robert Bruce requested follow-up at robert@scot.org", thread_id=thread_id)
    assert "<PERSON_1>" in body_2
    assert "<EMAIL_ADDRESS_1>" in body_2

    # Check that another person gets index 2
    _, body_3 = mask_for_llm("", "William Wallace joined the call", thread_id=thread_id)
    assert "<PERSON_2>" in body_3


def test_person_token_numbering_has_no_gaps_after_alias():
    """A registered alias must not consume a person index and leave a hole."""
    thread_id = "thread_alias_numbering"

    _, first = mask_for_llm("", "Robert Bruce called", thread_id=thread_id)
    _, alias = mask_for_llm("", "Robert called back", thread_id=thread_id)
    _, second_person = mask_for_llm("", "William Wallace called", thread_id=thread_id)

    assert "<PERSON_1>" in first
    assert "<PERSON_1>" in alias
    assert "<PERSON_2>" in second_person
    assert "<PERSON_3>" not in second_person
    assert get_token_map(thread_id) == {"<PERSON_1>": "Robert Bruce", "<PERSON_2>": "William Wallace"}


def test_unmasking():
    """Verify unmask_text restores original values accurately."""
    masker = PresidioMasker.get_instance()
    thread_id = "thread_unmask"

    text = "Contact Alice at alice@acme.com."
    masked = masker.mask_text(text, thread_id=thread_id)
    restored = masker.unmask_text(masked, thread_id=thread_id)

    assert restored == text


def test_mask_api_never_returns_raw_values_or_the_reverse_map():
    """The masking API hands back masked text only; the reverse map is opt-in."""
    thread_id = "thread_one_way"

    result = mask_for_llm(
        "Invoice for Bob Stone", "bob@vendor.com owes 4111 1111 1111 1111", thread_id=thread_id
    )

    assert isinstance(result, tuple) and len(result) == 2
    assert all(isinstance(part, str) for part in result)

    masked_sub, masked_bod = result
    for raw_value in ("Bob Stone", "bob@vendor.com", "4111 1111 1111 1111"):
        assert raw_value not in masked_sub
        assert raw_value not in masked_bod
    assert get_token_map(thread_id), "reverse map stays retrievable explicitly for unmasking"


def test_forget_thread_drops_tokens_and_reverse_map():
    """Retention is explicit: a forgotten thread keeps no raw values in memory."""
    thread_id = "thread_forget"
    mask_for_llm("", "Reach Priya Raman at priya@acme.com", thread_id=thread_id)
    assert get_token_map(thread_id)

    assert forget_thread(thread_id) is True
    assert get_token_map(thread_id) == {}
    assert forget_thread(thread_id) is False


def test_thread_registry_is_bounded():
    """The thread registry evicts the oldest entry instead of growing without limit."""
    masker = PresidioMasker.get_instance()

    for index in range(_MAX_THREADS + 5):
        masker.mask_text("Reach Dana at dana@acme.com", thread_id=f"bounded_{index}")

    assert len(masker._thread_registries) <= _MAX_THREADS
    assert get_token_map("bounded_0") == {}
    assert get_token_map(f"bounded_{_MAX_THREADS + 4}")
