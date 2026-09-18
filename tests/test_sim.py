"""Phase 3.4: the chat simulator, its CLI and bounded reply-tree reconstruction."""
import asyncio
import io
import json
import re
import sys
from collections.abc import Mapping, Sequence
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from agent.cli import main
from agent.dataset import Lane, Manifest
from agent.events import Direction, FeedbackKind, Message, SenderIdentity
from agent.safety.floor import Route
from agent.sim.policy import GoldPolicy
from agent.sim.reply_tree import build_reply_tree
from agent.sim.runner import (
    DecisionSource,
    SimError,
    close_input,
    run_simulation,
    thread_tree_for,
)
from agent.sim.schedule import release_order
from agent.trace import TraceSink

FIXTURE = Path(__file__).parent / "fixtures" / "stream_12.jsonl"
INTERRUPTING = {Route.ASK_FIRST_WITH_PREDRAFT, Route.ESCALATE}
START = datetime(2026, 8, 1, 8, 15, tzinfo=UTC)


def message(
    message_id: str,
    *,
    parent: str | None = None,
    minutes: int | None = 0,
) -> Message:
    """A minimal message for tree tests; ``minutes=None`` means no timestamp."""
    return Message(
        message_id=message_id,
        thread_id="th-1",
        sender=SenderIdentity(email=f"{message_id}@example.com", display_name=message_id),
        recipients=("me@example.com",),
        direction=Direction.INBOUND,
        subject="subject",
        body="body",
        parent_message_id=parent,
        sent_at=START + timedelta(minutes=minutes) if minutes is not None else None,
    )


def view(lane: Lane = Lane.CALIBRATION):
    return Manifest.load(FIXTURE).view(lane)


def scheduled_case_ids(seed: int = 7) -> list[str]:
    """Fixture case ids in the order the windows deliver them."""
    return [case.case_id for case in release_order(view().cases, seed=seed)]


def interrupting_case_ids(seed: int = 7) -> list[str]:
    """Fixture cases whose gold route asks the user, in delivery order."""
    routes = {
        case.case_id: Route(str(case.row["gold"]["autonomy_outcome"]))
        for case in Manifest.load(FIXTURE).cases
    }
    return [case_id for case_id in scheduled_case_ids(seed) if routes[case_id] in INTERRUPTING]


async def run_typed(
    typed: Mapping[int, Sequence[str]],
    *,
    seed: int = 7,
    show_labels: bool = False,
    policy: DecisionSource | None = None,
    trace: TraceSink | None = None,
):
    """Replay the fixture, typing ``typed`` at the given interrupt numbers.

    Lines enter the queue the way a human types them - while a decision waits - and the
    script ends behind them, so the remaining prompts read as end of input and the run
    terminates without a human. A line that has to be confirmed finds end of input
    rather than waiting on a queue nobody will feed again.
    """
    queue: asyncio.Queue = asyncio.Queue()
    last_fed = max(typed) if typed else 0
    seen = 0

    async def hook(index: int, decision) -> None:
        nonlocal seen
        seen += 1
        if seen > last_fed:
            await close_input(queue)
            return
        for line in typed.get(seen, ()):
            queue.put_nowait(line)
        if seen == last_fed:
            await close_input(queue)

    out = io.StringIO()
    outcome = await run_simulation(
        view(),
        seed=seed,
        out=out,
        input_queue=queue,
        on_interrupt=hook,
        show_labels=show_labels,
        policy=policy,
        trace=trace,
    )
    return outcome, out.getvalue()


ARRIVAL = re.compile(r"^\[\s*\d+/\d+\] (WAJO-\d+)$")
LABELS = re.compile(r"^    pipeline: route=(\w+) source=(\w+)")
DATASET = re.compile(r"^    labels:   dataset_route=(\w+)")


def arrivals(transcript: str) -> list[str]:
    """The case ids of the arrival blocks, in the order they were printed."""
    return [match.group(1) for line in transcript.splitlines() if (match := ARRIVAL.match(line))]


def labelled_routes(transcript: str) -> list[str]:
    """The route the pipeline chose for each arrival, in order."""
    return [
        match.group(1)
        for line in transcript.splitlines()
        if (match := LABELS.match(line))
    ]


def dataset_routes(transcript: str) -> list[str]:
    """The dataset's route for each arrival, which only the label view prints."""
    return [
        match.group(1)
        for line in transcript.splitlines()
        if (match := DATASET.match(line))
    ]


def decision_sources(transcript: str) -> set[str]:
    """Which decision source produced the routes in a labelled run."""
    return {match.group(2) for line in transcript.splitlines() if (match := LABELS.match(line))}


def block_of(transcript: str, case_id: str) -> str:
    """One arrival's text, from its header up to the next arrival."""
    for block in re.split(r"(?m)^(?=\[\s*\d+/\d+\] WAJO-)", transcript):
        if block.startswith("[") and case_id in block.splitlines()[0]:
            return block
    raise AssertionError(f"no arrival block for {case_id}")


def test_walk_is_depth_first_root_first() -> None:
    tree = build_reply_tree(
        [
            message("a", minutes=0),
            message("b", parent="a", minutes=1),
            message("c", parent="b", minutes=2),
        ]
    )
    assert [item.message_id for item in tree.walk()] == ["a", "b", "c"]
    assert tree.node_count == 3
    assert tree.max_depth_reached == 2
    assert tree.truncated is False


def test_siblings_expand_in_timestamp_order_then_id() -> None:
    tree = build_reply_tree(
        [
            message("root", minutes=0),
            message("late", parent="root", minutes=5),
            message("early", parent="root", minutes=1),
        ]
    )
    assert [item.message_id for item in tree.branch("root")] == ["early", "late"]


def test_cycle_is_walked_once() -> None:
    tree = build_reply_tree([message("a", parent="b"), message("b", parent="a")])
    assert tree.node_count == 2
    assert {item.message_id for item in tree.walk()} == {"a", "b"}


def test_duplicate_ids_are_kept_once() -> None:
    tree = build_reply_tree([message("a", minutes=0), message("a", minutes=9)])
    assert tree.node_count == 1


def test_depth_cap_stops_the_walk() -> None:
    thread = [message("m0", minutes=0)] + [
        message(f"m{index}", parent=f"m{index - 1}", minutes=index) for index in range(1, 8)
    ]
    tree = build_reply_tree(thread, max_depth=2)
    assert tree.truncated is True
    assert tree.max_depth_reached == 2
    assert tree.node_count == 3


def test_node_cap_stops_the_walk() -> None:
    thread = [message("root", minutes=0)] + [
        message(f"child{index}", parent="root", minutes=index + 1) for index in range(5)
    ]
    tree = build_reply_tree(thread, max_nodes=3)
    assert tree.truncated is True
    assert tree.node_count == 3


def test_missing_parent_is_reported_not_silently_dropped() -> None:
    tree = build_reply_tree([message("root", minutes=0), message("lost", parent="ghost", minutes=1)])
    assert tree.orphan_ids == ("lost",)
    assert {item.message_id for item in tree.walk()} == {"root", "lost"}


def test_every_root_is_walked_not_just_the_first() -> None:
    tree = build_reply_tree(
        [
            message("undated", minutes=None),
            message("root", minutes=0),
            message("child", parent="root", minutes=1),
        ]
    )
    assert tree.root.message_id == "root"
    assert tree.node_count == len(tree.walk()) == 3
    assert [item.message_id for item in tree.walk()] == ["root", "child", "undated"]


def test_bad_caps_and_empty_threads_are_rejected() -> None:
    with pytest.raises(ValueError):
        build_reply_tree([message("a")], max_depth=-1)
    with pytest.raises(ValueError):
        build_reply_tree([message("a")], max_nodes=0)
    with pytest.raises(ValueError):
        build_reply_tree([])
    with pytest.raises(KeyError):
        build_reply_tree([message("a")], root_id="missing")


def test_thread_tree_for_uses_the_case_thread() -> None:
    case = view().cases[0]
    tree = thread_tree_for(case)
    assert tree.root.thread_id == case.event.thread.thread_id
    assert case.event.message.message_id in {item.message_id for item in tree.walk()}


def test_every_case_in_the_fixture_is_processed() -> None:
    outcome, transcript = asyncio.run(run_typed({}))
    assert outcome.processed == len(view().cases) == 12
    assert len(arrivals(transcript)) == 12


def test_arrivals_come_in_the_windowed_order_the_seed_recorded() -> None:
    """The lane is delivered window by window, not in the dataset's sequence order."""
    _, transcript = asyncio.run(run_typed({}))
    assert arrivals(transcript) == scheduled_case_ids()
    assert arrivals(transcript) != [case.case_id for case in view().cases]
    assert "order drawn from seed 7" in transcript


def test_only_the_pipeline_routes_that_ask_wait_for_a_reply() -> None:
    outcome, transcript = asyncio.run(run_typed({}, show_labels=True))
    assert len(labelled_routes(transcript)) == 12
    marked = [
        case_id
        for case_id, route in zip(arrivals(transcript), labelled_routes(transcript), strict=True)
        if "[waiting]" in block_of(transcript, case_id)
    ]
    waiting = [
        case_id
        for case_id, route in zip(arrivals(transcript), labelled_routes(transcript), strict=True)
        if Route(route) in INTERRUPTING
    ]
    assert marked == waiting
    assert outcome.interrupts == len(marked) == transcript.count("[waiting]")


def test_the_run_records_a_route_per_case_and_who_it_waited_on() -> None:
    """The eval curve is built from these two, so they have to be the run's own record."""
    outcome, transcript = asyncio.run(run_typed({}, show_labels=True))
    waiting = {
        case_id
        for case_id, route in zip(arrivals(transcript), labelled_routes(transcript), strict=True)
        if Route(route) in INTERRUPTING
    }

    assert list(outcome.routes) == arrivals(transcript)
    assert sum(outcome.route_counts.values()) == outcome.processed == len(outcome.routes)
    assert set(outcome.asked) == waiting
    assert set(outcome.asked.values()) <= {"APPROVAL_REQUIRED", "AUTHORIZATION_REFUSED"}


def test_the_reference_policy_reproduces_the_dataset_routes() -> None:
    """The plan's check, against the labels: only ask-first and escalate lines wait."""
    expected = interrupting_case_ids()
    assert len(expected) == 7
    outcome, transcript = asyncio.run(
        run_typed({}, show_labels=True, policy=GoldPolicy())
    )
    assert dataset_routes(transcript) == labelled_routes(transcript)
    assert [
        case_id
        for case_id, route in zip(arrivals(transcript), labelled_routes(transcript), strict=True)
        if Route(route) in INTERRUPTING
    ] == expected
    assert outcome.interrupts == len(expected)


def test_the_default_run_decides_from_the_pipeline() -> None:
    _, transcript = asyncio.run(run_typed({}, show_labels=True))
    assert decision_sources(transcript) == {"proposal"}


def test_the_pipeline_escalates_every_case_the_dataset_escalates() -> None:
    """The one error direction that matters: never act on mail the labels fence."""
    _, transcript = asyncio.run(run_typed({}, show_labels=True))
    pairs = zip(arrivals(transcript), labelled_routes(transcript), dataset_routes(transcript), strict=True)
    unsafe = [
        case_id
        for case_id, chosen, wanted in pairs
        if wanted == Route.ESCALATE.value and chosen != Route.ESCALATE.value
    ]
    assert unsafe == []


def test_silent_and_notify_routes_never_wait() -> None:
    outcome, transcript = asyncio.run(run_typed({}))
    assert sum(outcome.route_counts.values()) == outcome.processed == 12
    assert len(arrivals(transcript)) == 12
    # Nothing blocks on a route the plan did not nominate for a human.
    waiting = outcome.route_counts["ASK_FIRST_WITH_PREDRAFT"] + outcome.route_counts["ESCALATE"]
    assert outcome.interrupts == waiting
    assert outcome.route_counts["PROCEED_SILENTLY"] > 0
    assert outcome.route_counts["PROCEED_AND_NOTIFY"] > 0


def gold_route(case_id: str) -> Route:
    case = next(item for item in Manifest.load(FIXTURE).cases if item.case_id == case_id)
    return Route(str(case.row["gold"]["autonomy_outcome"]))


def first_interrupt_of(route: Route) -> tuple[int, str]:
    """The interrupt number and case id of the first arrival with this gold route."""
    for position, case_id in enumerate(interrupting_case_ids(), start=1):
        if gold_route(case_id) is route:
            return position, case_id
    raise AssertionError(f"the fixture has no {route.value} case in delivery order")


def up_to(position: int, lines: Sequence[str]) -> dict[int, list[str]]:
    """Answer the prompts before ``position`` with a blank line, then type ``lines``.

    The chat blocks on every prompt, so a script that only wants to speak at the fourth
    one still has to get past the first three; pressing enter is what a user does.
    """
    return {
        prompt: (list(lines) if prompt == position else [""]) for prompt in range(1, position + 1)
    }


def test_an_approval_releases_the_prepared_action_and_is_learnable() -> None:
    """A yes at an ASK prompt is both the release and the reward the learner counts."""
    position, case_id = first_interrupt_of(Route.ASK_FIRST_WITH_PREDRAFT)
    outcome, transcript = asyncio.run(run_typed(up_to(position, ["yes, send it"])))
    recorded = next(item for item in outcome.feedback if item.case_id == case_id)
    assert recorded.kind is FeedbackKind.APPROVE
    assert recorded.explicit_for_learning is True
    assert outcome.learnable_feedback == (recorded,)
    assert f"reply for {case_id}: 'yes, send it'" in transcript
    released = [receipt for receipt in outcome.receipts if receipt.case_id == case_id]
    assert len(released) == 1
    assert "released rcpt-" in transcript


def test_an_approval_at_an_escalation_decides_nothing() -> None:
    """Nothing was prepared, so a bare yes is not an approval to credit."""
    position, case_id = first_interrupt_of(Route.ESCALATE)
    outcome, transcript = asyncio.run(run_typed(up_to(position, ["yes"])))
    assert "nothing was prepared for this one" in transcript
    assert outcome.learnable_feedback == ()
    assert [receipt for receipt in outcome.receipts if receipt.case_id == case_id] == []
    typed = next(item for item in outcome.feedback if item.case_id == case_id)
    assert typed.kind is FeedbackKind.NONE


def test_a_policy_line_is_stored_only_once_it_is_confirmed() -> None:
    position, _ = first_interrupt_of(Route.ASK_FIRST_WITH_PREDRAFT)
    line = "always escalate mail from elena@techcorp.synthetic.example"
    assert asyncio.run(run_typed(up_to(position, [line])))[0].claims == []

    outcome, transcript = asyncio.run(run_typed(up_to(position, [line, "yes"])))
    assert len(outcome.claims) == 1
    claim = outcome.claims[0]
    assert claim.scope.sender == "elena@techcorp.synthetic.example"
    assert claim.route is Route.ESCALATE
    assert "stored clm-" in transcript
    assert len(outcome.learnable_feedback) == 1


def test_a_correction_typed_at_a_prompt_binds_to_that_decision() -> None:
    first = interrupting_case_ids()[0]
    outcome, transcript = asyncio.run(run_typed({1: ["yes", "actually that sender is spam"]}))
    assert outcome.replies == 1
    assert outcome.corrections == 1
    assert {item.case_id for item in outcome.feedback} == {first}
    assert f"correction bound to {first}" in transcript


def test_a_line_queued_before_the_first_arrival_has_no_decision_to_bind_to() -> None:
    queue: asyncio.Queue = asyncio.Queue()
    queue.put_nowait("hello?")
    asyncio.run(close_input(queue))
    out = io.StringIO()
    outcome = asyncio.run(run_simulation(view(), seed=7, out=out, input_queue=queue))
    assert outcome.corrections == 1
    assert outcome.feedback[0].case_id == "unbound"
    assert "correction recorded before any decision" in out.getvalue()


def test_buffered_input_is_recorded_as_corrections_not_answers(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A piped stream has no prompt to answer, so its lines are corrections.

    Reading them as answers would misattribute them to whichever case happens to be
    prompting when the pipe is drained, which is a race, not a decision.
    """
    monkeypatch.setattr(sys, "stdin", io.StringIO("yes, send it\nand one more thing\n"))
    out = io.StringIO()
    outcome = asyncio.run(run_simulation(view(), seed=7, out=out))
    assert (outcome.replies, outcome.corrections) == (0, 2)
    assert outcome.silent_ends == 7
    assert all(item.case_id == "unbound" for item in outcome.feedback)
    assert "correction recorded before any decision" in out.getvalue()


class ExplodingPolicy:
    """A decision source that fails, to check the failure names its case."""

    source = "exploding"

    async def decide(self, case, *, router=None):
        raise RuntimeError("policy is broken")


def test_a_failing_policy_names_the_case_it_stopped_on() -> None:
    with pytest.raises(SimError) as caught:
        asyncio.run(run_simulation(view(), seed=7, out=io.StringIO(), policy=ExplodingPolicy()))
    assert scheduled_case_ids()[0] in str(caught.value)
    assert "policy is broken" in str(caught.value)


def test_a_broken_input_stream_ends_the_run_instead_of_hanging(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """If the read fails, the prompts must see end of input, not wait forever."""

    class BrokenStdin:
        def readline(self) -> str:
            raise OSError("stdin is gone")

    monkeypatch.setattr(sys, "stdin", BrokenStdin())
    out = io.StringIO()
    outcome = asyncio.run(run_simulation(view(), seed=7, out=out))
    assert outcome.processed == 12
    assert outcome.silent_ends == outcome.interrupts
    assert "input failed" in out.getvalue()
    assert "input_error=OSError: stdin is gone" in out.getvalue()


def test_end_of_input_is_silence_not_approval() -> None:
    outcome, transcript = asyncio.run(run_typed({}))
    assert outcome.replies == 0
    assert outcome.silent_ends == 7
    assert transcript.count("silence is not approval") == 7
    assert outcome.learnable_feedback == ()
    assert outcome.feedback == []


def test_one_reply_then_silence_for_the_rest() -> None:
    outcome, _ = asyncio.run(run_typed({1: ["yes, send it"]}))
    assert (outcome.replies, outcome.silent_ends) == (1, 6)


def test_same_seed_reproduces_the_log_and_a_new_seed_does_not() -> None:
    first, _ = asyncio.run(run_typed({}, seed=7))
    second, _ = asyncio.run(run_typed({}, seed=7))
    other, _ = asyncio.run(run_typed({}, seed=8))
    assert first.replay_digest == second.replay_digest
    assert first.replay_digest != other.replay_digest


def test_an_arrival_shows_the_mail_a_production_inbox_shows() -> None:
    first = scheduled_case_ids()[0]
    case = next(item for item in Manifest.load(FIXTURE).cases if item.case_id == first)
    message = case.event.message
    _, transcript = asyncio.run(run_typed({}))
    block = block_of(transcript, case.case_id)
    assert block.splitlines()[0] == f"[ 1/12] {case.case_id}"
    assert f"From:    {message.sender.display_name} <{message.sender.email}>" in block
    assert f"Subject: {message.subject}" in block
    assert all(recipient in block for recipient in message.recipients)
    first_body_line = next(line for line in message.body.splitlines() if line.strip())
    assert first_body_line.strip()[:24] in block


def test_a_reply_prompt_is_reported_for_the_case_that_waits() -> None:
    first = interrupting_case_ids()[0]
    _, transcript = asyncio.run(run_typed({}))
    assert "[waiting]" in block_of(transcript, first)


def test_an_escalation_and_an_ask_are_not_the_same_wait() -> None:
    """Only one of the two has something to release, so only one says approval."""
    _, transcript = asyncio.run(run_typed({}, show_labels=True))
    routes = dict(zip(arrivals(transcript), labelled_routes(transcript), strict=True))
    asked = next(
        case for case, route in routes.items() if route == Route.ASK_FIRST_WITH_PREDRAFT.value
    )
    escalated = next(case for case, route in routes.items() if route == Route.ESCALATE.value)
    assert "[waiting] approval required" in block_of(transcript, asked)
    assert "[waiting] escalated" in block_of(transcript, escalated)
    assert "approval required" not in block_of(transcript, escalated)


def test_a_prompt_no_rule_can_quieten_says_so() -> None:
    """A user typing rules at an escalation would be teaching the wrong thing."""
    _, transcript = asyncio.run(run_typed({}, show_labels=True))
    routes = dict(zip(arrivals(transcript), labelled_routes(transcript), strict=True))
    asked = next(
        case for case, route in routes.items() if route == Route.ASK_FIRST_WITH_PREDRAFT.value
    )
    escalated = next(case for case, route in routes.items() if route == Route.ESCALATE.value)
    assert "no rule quietens this one" in block_of(transcript, escalated)
    assert "no rule quietens this one" not in block_of(transcript, asked)


def test_the_summary_says_which_prompts_a_rule_could_quieten() -> None:
    outcome, transcript = asyncio.run(run_typed({}))
    assert outcome.quietenable == 3
    assert outcome.interrupts == 7
    assert "prompts a rule could quieten=3 kept by the mail itself=4" in transcript


def test_the_thread_history_is_shown_as_the_prior_messages() -> None:
    case = next(case for case in Manifest.load(FIXTURE).cases if case.event.thread.messages_before)
    _, transcript = asyncio.run(run_typed({}))
    block = block_of(transcript, case.case_id)
    assert len(case.event.thread.messages_before) == block.count("  prior:  ")
    assert "message(s)" in block


def test_the_default_view_never_shows_the_answer_key() -> None:
    """Sender, subject and body are inputs in production; labels are only answers.

    Anyone calibrating has to judge the mail they would actually receive, so a leak
    here would be scored as skill and then fail in production.
    """
    _, transcript = asyncio.run(run_typed({}))
    shown = transcript.split("run summary")[0]
    for token in ("route=", "action=", "floor=", "gold=", "intent=", "relationship="):
        assert token not in shown
    for route in Route:
        assert route.value not in shown


def test_show_labels_reveals_the_decision_and_the_answer() -> None:
    _, transcript = asyncio.run(run_typed({}, show_labels=True))
    assert "route=" in transcript
    assert "intent='newsletter'" in transcript
    assert "dataset_route=" in transcript
    assert len(labelled_routes(transcript)) == len(dataset_routes(transcript)) == 12


def test_cli_show_labels_flag_is_off_by_default(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
) -> None:
    monkeypatch.setattr(sys, "stdin", io.StringIO(""))
    main(["sim", "run", "--fixture", str(FIXTURE)])
    assert "route=" not in capsys.readouterr().out
    main(["sim", "run", "--fixture", str(FIXTURE), "--show-labels"])
    assert "route=" in capsys.readouterr().out


def test_cli_replays_the_fixture(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
) -> None:
    monkeypatch.setattr(sys, "stdin", io.StringIO(""))
    assert main(["sim", "run", "--fixture", str(FIXTURE), "--seed", "7"]) == 0
    transcript = capsys.readouterr().out
    assert len(arrivals(transcript)) == 12
    assert transcript.count("[waiting]") == len(interrupting_case_ids())


def test_cli_seed_flag_changes_the_replay_digest(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
) -> None:
    monkeypatch.setattr(sys, "stdin", io.StringIO(""))
    digests = []
    for seed in ("7", "8"):
        main(["sim", "run", "--fixture", str(FIXTURE), "--seed", seed])
        digests.append(capsys.readouterr().out.splitlines()[-1])
    assert digests[0] != digests[1]


def test_cli_refuses_to_open_the_sealed_lane() -> None:
    with pytest.raises(SystemExit):
        main(["sim", "run", "--fixture", str(FIXTURE), "--lane", "held_out"])


def test_cli_requires_a_subcommand() -> None:
    with pytest.raises(SystemExit):
        main([])
    with pytest.raises(SystemExit):
        main(["sim"])


def test_a_traced_run_writes_the_decision_and_never_the_mail(tmp_path: Path) -> None:
    """On a real run: one line per arrival, and no mail text in any of them."""
    path = tmp_path / "run.jsonl"
    sink = TraceSink(path)
    outcome, transcript = asyncio.run(run_typed({1: ("okay",)}, trace=sink))
    sink.close()

    lines = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
    decisions = [line for line in lines if line["event"] == "decision"]
    assert len(decisions) == outcome.processed
    assert [line["case_id"] for line in decisions] == arrivals(transcript)
    # A decision is traceable without the mail: what it was, what it read, what it chose.
    assert all(line["message_digest"].startswith("sha256:") for line in decisions)
    assert all(line["floor"]["allowed_routes"] for line in decisions)
    assert all(line["dataset_digest"] for line in decisions)

    text = path.read_text(encoding="utf-8")
    for case in view().cases:
        assert case.event.message.body[:60] not in text
        assert case.event.message.subject not in text
