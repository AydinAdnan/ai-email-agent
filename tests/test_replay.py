"""Unit tests for deterministic replay and the split firewall (Phase 3.2).

Covers:
- Seeded clock determinism (no wall-clock input)
- Append-only stream: duplicates and order regressions refused, stream untouched
- Two same-seed replays produce byte-identical logs; a different seed does not
- Manifest loading: lane counts, dataset digest, unknown split and duplicate ids
- The firewall both ways: no cross-lane reads, no learner writes outside calibration
"""
import hashlib
import json
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from src.agent.dataset import (
    DEFAULT_DATASET_PATH,
    LEARNABLE_LANES,
    SPLIT_TO_LANE,
    Lane,
    Manifest,
    ManifestError,
    SplitViolation,
    event_from_row,
)
from src.agent.events import DuplicateEventError, EmailEvent, OutOfOrderEventError
from src.agent.replay import DATASET_EPOCH, EventStream, SeededClock, replay

SEED = 7


@pytest.fixture(scope="module")
def manifest() -> Manifest:
    return Manifest.load(DEFAULT_DATASET_PATH)


@pytest.fixture(scope="module")
def rows() -> list[dict]:
    assert DEFAULT_DATASET_PATH.exists(), f"dataset missing at {DEFAULT_DATASET_PATH}"
    with open(DEFAULT_DATASET_PATH, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


# ============================================================================
# 1. Seeded clock
# ============================================================================

def test_clock_is_deterministic_for_a_seed():
    """Same seed, same time; different seed, different start."""
    assert SeededClock(7).started_at == SeededClock(7).started_at
    assert SeededClock(7).started_at != SeededClock(8).started_at


def test_clock_starts_at_the_dataset_epoch_and_only_moves_on_advance():
    """Nothing reads the wall clock, so time is frozen until the simulation moves it."""
    clock = SeededClock(SEED)
    first = clock.now()
    assert clock.now() == first
    assert clock.ticks == 0

    moved = clock.advance(3)
    assert moved == first + timedelta(minutes=3)
    assert clock.ticks == 3


def test_clock_can_be_configured_but_not_moved_backwards():
    """A custom epoch and tick are honoured; a non-positive advance is refused."""
    clock = SeededClock(0, start=datetime(2030, 1, 1, tzinfo=UTC), tick=timedelta(seconds=30))
    assert clock.now() == datetime(2030, 1, 1, tzinfo=UTC)
    assert clock.advance() == datetime(2030, 1, 1, 0, 0, 30, tzinfo=UTC)
    with pytest.raises(ValueError):
        clock.advance(0)


def test_seed_offsets_the_start_but_keeps_the_epoch():
    """The seed offsets within the first minute, so replays stay plausible."""
    clock = SeededClock(SEED)
    assert clock.started_at >= DATASET_EPOCH
    assert clock.started_at < DATASET_EPOCH + timedelta(minutes=1)


# ============================================================================
# 2. Append-only stream
# ============================================================================

def test_stream_refuses_a_duplicate_arrival(manifest):
    """The same case cannot arrive twice, and the stream keeps its state."""
    stream = EventStream(SeededClock(SEED))
    first, second = manifest.cases[0].event, manifest.cases[1].event
    stream.append(first)
    stream.append(second)

    with pytest.raises(DuplicateEventError):
        stream.append(first)

    assert stream.events == (first, second)
    assert len(stream) == 2


def test_stream_refuses_a_regression_in_sequence(manifest):
    """An arrival numbered before the last one is out of order, not a new arrival."""
    stream = EventStream(SeededClock(SEED))
    stream.append(manifest.cases[1].event)

    with pytest.raises(OutOfOrderEventError):
        stream.append(manifest.cases[0].event)

    assert len(stream) == 1


def test_stream_has_no_mutating_api():
    """Append-only is structural: there is no update, delete or reorder."""
    stream = EventStream(SeededClock(SEED))
    for name in ("remove", "pop", "insert", "delete", "sort", "clear", "extend"):
        assert not hasattr(stream, name), f"EventStream must not expose {name}"


def test_stream_timestamps_come_from_the_clock(manifest):
    """Each arrival is stamped by the clock, one tick apart."""
    clock = SeededClock(SEED)
    stream = EventStream(clock)
    for case in manifest.cases[:3]:
        stream.append(case.event)

    assert clock.ticks == 3
    lines = stream.log_jsonl().splitlines()
    delivered = [json.loads(line)["delivered_at"] for line in lines[1:]]
    assert delivered == sorted(delivered)


# ============================================================================
# 3. Deterministic logs
# ============================================================================

def test_same_seed_produces_byte_identical_logs(manifest):
    """The plan's check: two same-seed runs emit identical event logs."""
    events = manifest.view(Lane.CALIBRATION).events()
    first = replay(events, seed=SEED)
    second = replay(events, seed=SEED)

    assert first.log_jsonl() == second.log_jsonl()
    assert first.digest() == second.digest()


def test_a_different_seed_changes_the_log(manifest):
    """The seed is load-bearing, so it has to show up in the artifact."""
    events = manifest.view(Lane.CALIBRATION).events()
    assert replay(events, seed=7).log_jsonl() != replay(events, seed=8).log_jsonl()


def test_log_is_canonical_jsonl_with_a_header(manifest):
    """One header line, then one parseable line per arrival."""
    events = manifest.view(Lane.CALIBRATION).events()[:5]
    stream = replay(events, seed=SEED)
    lines = stream.log_jsonl().splitlines()

    assert len(lines) == len(events) + 1
    header = json.loads(lines[0])
    assert header["seed"] == SEED
    assert header["event_count"] == len(events)
    assert all(json.loads(line)["event"]["case_id"] for line in lines[1:])

    assert stream.digest() == hashlib.sha256(stream.log_jsonl().encode("utf-8")).hexdigest()


def test_replay_preserves_the_arrival_order(manifest):
    """The log's order is the dataset's sequence order, not file order."""
    view = manifest.view(Lane.CALIBRATION)
    stream = replay(view.events(), seed=SEED)
    logged = [json.loads(line)["sequence_index"] for line in stream.log_jsonl().splitlines()[1:]]

    assert logged == sorted(logged)
    assert logged == [case.sequence_index for case in view.cases]


# ============================================================================
# 4. Manifest loading
# ============================================================================

def test_lane_counts_are_reported(manifest):
    """Counts per split and per lane, with the dataset's real sizes."""
    summary = manifest.summary()
    assert summary["learning_stream"] == 60
    assert summary["development"] == 20
    assert summary["golden_ordinary"] == 40
    assert summary["golden_adversarial"] == 20
    assert summary["lane:calibration"] == 60
    assert summary["lane:development"] == 20
    assert summary["lane:held_out"] == 60


def test_dataset_digest_matches_the_file(manifest):
    """A replay can name the exact dataset it ran against."""
    assert manifest.dataset_digest == hashlib.sha256(DEFAULT_DATASET_PATH.read_bytes()).hexdigest()


def test_lanes_split_the_dataset_without_overlap(manifest):
    """Every case lands in exactly one lane."""
    lanes = {lane: manifest.lane_cases(lane) for lane in Lane}
    assert sum(len(cases) for cases in lanes.values()) == len(manifest.cases)

    ids = [case.case_id for cases in lanes.values() for case in cases]
    assert len(ids) == len(set(ids))


def test_unknown_split_is_rejected(rows):
    """A split the manifest does not know is a data error, not a silent default."""
    broken = [dict(rows[0], split="mystery_lane")]
    with pytest.raises(ManifestError):
        Manifest.from_rows(broken)


def test_duplicate_case_id_is_rejected(rows):
    """A case appearing twice would double-count in every denominator."""
    with pytest.raises(ManifestError):
        Manifest.from_rows([rows[0], rows[0]])


def test_manifest_sorts_by_sequence_not_file_order(rows):
    """A shuffled file replays identically, because order is sequence_index."""
    shuffled = list(reversed(rows))
    assert Manifest.from_rows(shuffled).cases == Manifest.from_rows(rows).cases

    replayed = replay(Manifest.from_rows(shuffled).view(Lane.HELD_OUT).events(), seed=SEED)
    straight = replay(Manifest.from_rows(rows).view(Lane.HELD_OUT).events(), seed=SEED)
    assert replayed.log_jsonl() == straight.log_jsonl()


def test_events_are_canonical_events(manifest):
    """The manifest hands out EmailEvents, not raw rows."""
    view = manifest.view(Lane.HELD_OUT)
    assert all(isinstance(event, EmailEvent) for event in view.events())
    assert view.events() == tuple(event_from_row(case.row) for case in view.cases)


# ============================================================================
# 5. The firewall, both ways
# ============================================================================

def test_a_learning_read_of_a_held_out_case_is_a_split_violation(manifest):
    """The plan's check, verbatim: SPLIT_VIOLATION on a cross-lane read."""
    learning = manifest.view(Lane.CALIBRATION)
    held_out_case = manifest.view(Lane.HELD_OUT).case_ids[0]

    with pytest.raises(SplitViolation) as excinfo:
        learning.open(held_out_case)

    assert excinfo.value.code == "SPLIT_VIOLATION"
    assert "SPLIT_VIOLATION" in str(excinfo.value)
    assert held_out_case in str(excinfo.value)


def test_a_held_out_view_cannot_open_a_calibration_case(manifest):
    """The separation is symmetric: a lane view only sees its own rows."""
    held_out = manifest.view(Lane.HELD_OUT)
    calibration_case = manifest.view(Lane.CALIBRATION).case_ids[0]

    with pytest.raises(SplitViolation):
        held_out.open(calibration_case)


def test_only_the_calibration_lane_may_write_learner_state(manifest):
    """Held-out and development code cannot update the learner."""
    manifest.view(Lane.CALIBRATION).require_learner_write()

    for lane in (Lane.HELD_OUT, Lane.DEVELOPMENT):
        view = manifest.view(lane)
        assert view.can_write_learner_state() is False
        with pytest.raises(SplitViolation):
            view.require_learner_write()

    assert {Lane.CALIBRATION} == LEARNABLE_LANES


def test_unknown_case_id_is_a_lookup_error(manifest):
    """An id that is in no lane is not a firewall breach, just a miss."""
    with pytest.raises(KeyError):
        manifest.view(Lane.CALIBRATION).open("WAJO-9999")


def test_held_out_lane_carries_the_adversarial_cases(manifest):
    """The sealed lane holds the whole adversarial split plus the ordinary gold set."""
    held_out = manifest.view(Lane.HELD_OUT)
    adversarial = [
        case.case_id for case in held_out.cases if case.split == "golden_adversarial"
    ]
    assert len(adversarial) == 20
    assert all(case.row["adversarial_tags"] for case in held_out.cases if case.split == "golden_adversarial")


def test_split_to_lane_mapping_is_complete():
    """Every dataset split has a lane, and the golden splits are sealed."""
    assert SPLIT_TO_LANE["learning_stream"] == Lane.CALIBRATION
    assert SPLIT_TO_LANE["development"] == Lane.DEVELOPMENT
    assert SPLIT_TO_LANE["golden_ordinary"] == Lane.HELD_OUT
    assert SPLIT_TO_LANE["golden_adversarial"] == Lane.HELD_OUT


def test_development_lane_has_nothing_to_learn_from(manifest):
    """The debug lane carries no explicit feedback, which is why it never teaches."""
    development = manifest.view(Lane.DEVELOPMENT)
    assert development.cases
    assert not any(
        case.row["observed_user_feedback"]["explicit_for_learning"]
        for case in development.cases
    )


def test_lane_view_is_bound_to_its_lane(manifest):
    """A view cannot be re-pointed at another lane after it is built."""
    view = manifest.view(Lane.CALIBRATION)
    assert view.lane == Lane.CALIBRATION
    assert set(view.case_ids).isdisjoint(manifest.view(Lane.HELD_OUT).case_ids)
    assert isinstance(DEFAULT_DATASET_PATH, Path)
