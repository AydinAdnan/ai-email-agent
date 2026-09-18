"""Phase 7.1: retrieving the few sent replies a draft may learn from."""
from pathlib import Path

from agent.dataset import Lane, Manifest
from agent.drafts import (
    MAX_STYLE_EXAMPLES,
    SentExample,
    estimate_tokens,
    examples_from_row,
    retrieve_style,
    style_limit,
)

FIXTURE = Path(__file__).parent / "fixtures" / "stream_12.jsonl"
ME = "elena@techcorp.synthetic.example"


def example(
    source_message_id: str,
    *,
    recipient: str = "someone.else@example.com",
    intent: str = "scheduling",
    text: str = "Short note.",
    sent_at: str = "2026-07-01T09:00:00Z",
) -> SentExample:
    """One sent reply, from the mailbox's own history."""
    return SentExample(
        source_message_id=source_message_id,
        recipient=recipient,
        intent=intent,
        text=text,
        sent_at=sent_at,
    )


def test_the_same_person_ranks_first() -> None:
    """A reply the user sent this person beats an older one to anybody else."""
    archive = [
        example("msg-to-other", recipient="other@example.com", intent="scheduling"),
        example("msg-to-them", recipient=ME, intent="scheduling"),
        example("msg-unrelated", recipient="other@example.com", intent="receipt"),
    ]
    style = retrieve_style(archive, sender=ME, intent="information request")

    assert next(item.example.source_message_id for item in style.picked) == "msg-to-them"
    assert style.picked[0].reason == "same person"


def test_the_same_intent_beats_the_fallback() -> None:
    """An example about the same kind of mail is worth more than an unrelated one."""
    archive = [
        example("msg-scheduling", intent="scheduling", sent_at="2026-07-01T09:00:00Z"),
        example("msg-receipt", intent="receipt", sent_at="2026-07-09T09:00:00Z"),
    ]
    style = retrieve_style(archive, sender=ME, intent="scheduling")

    assert [item.example.source_message_id for item in style.picked] == [
        "msg-scheduling",
        "msg-receipt",
    ]
    assert [item.reason for item in style.picked] == ["same intent", "fallback"]


def test_recency_orders_the_examples_inside_a_group() -> None:
    archive = [
        example("msg-old", recipient=ME, sent_at="2026-06-01T09:00:00Z"),
        example("msg-new", recipient=ME, sent_at="2026-07-30T09:00:00Z"),
    ]
    style = retrieve_style(archive, sender=ME, intent="scheduling")

    assert [item.example.source_message_id for item in style.picked] == ["msg-new", "msg-old"]


def test_the_count_cap_is_honoured() -> None:
    archive = [example(f"msg-{index}", recipient=ME) for index in range(8)]
    style = retrieve_style(archive, sender=ME, intent="scheduling", limit=2)

    assert len(style.picked) == 2
    assert style.considered == 8
    assert style.dropped == 6


def test_an_example_that_does_not_fit_the_token_budget_is_left_out_whole() -> None:
    """Half of somebody's sentence is not their style, so it is dropped, not truncated."""
    long_text = " ".join(["word"] * 400)
    archive = [
        example("msg-long", recipient=ME, text=long_text),
        example("msg-short", recipient=ME, text="Short note."),
    ]
    style = retrieve_style(archive, sender=ME, intent="scheduling", token_budget=20)

    assert [item.example.source_message_id for item in style.picked] == ["msg-short"]
    assert style.tokens <= 20
    assert style.dropped == 1


def test_the_budget_shrinks_what_is_kept_not_what_is_counted() -> None:
    """The cap is spent by the examples actually kept, longest first refused."""
    archive = [example(f"msg-{index}", recipient=ME, text="one two three") for index in range(4)]
    cost = estimate_tokens("one two three")
    style = retrieve_style(archive, sender=ME, intent="scheduling", token_budget=cost * 2)

    assert len(style.picked) == 2
    assert style.tokens == cost * 2


def test_a_mail_with_no_consented_examples_borrows_nothing() -> None:
    style = retrieve_style((), sender=ME, intent="scheduling")

    assert style.picked == ()
    assert style.tokens == 0
    assert "none" in style.describe()


def test_the_describe_line_names_what_was_kept() -> None:
    style = retrieve_style(
        [example("msg-to-them", recipient=ME), example("msg-other")],
        sender=ME,
        intent="scheduling",
        limit=1,
    )
    described = style.describe()

    assert "msg-to-them" in described
    assert "same person" in described
    assert "1 left out over the cap" in described


def test_the_case_row_carries_the_examples_and_the_cap() -> None:
    """The archive and its budget come from the mailbox's own rows, not from the labels."""
    case = Manifest.load(FIXTURE).view(Lane.CALIBRATION).open("WAJO-0008")
    examples = examples_from_row(case.row)

    assert examples, "the fixture carries the user's sent examples"
    assert style_limit(case.row) == MAX_STYLE_EXAMPLES
    assert all(item.recipient and item.text for item in examples)


def test_a_row_without_the_field_borrows_nothing() -> None:
    assert examples_from_row({}) == ()
    assert style_limit({}) == MAX_STYLE_EXAMPLES
