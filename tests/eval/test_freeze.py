"""The freeze: a learned run has to survive a process, and a bad payload has to be named.

The sealed lane is scored against the state the calibration left behind, so the payload
has to carry back every field the decision path reads. A payload this build cannot read
is refused rather than half-restored: a learner rebuilt from a shape it does not know
would go on to decide what the agent does with real mail.
"""
from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

import pytest

from agent.autonomy import state as learner_state
from agent.autonomy.bandit import Learner
from agent.autonomy.confidence import Bucket
from agent.autonomy.router import Router
from agent.events import FeedbackEvent, FeedbackKind, is_learnable
from agent.safety.floor import Route

WHEN = datetime(2026, 8, 1, 9, 0, tzinfo=UTC)
BUCKET = Bucket(
    sender="elena@techcorp.synthetic.example",
    intent="scheduling",
    action="email.create_draft",
)
OTHER = Bucket(sender="news@engweekly.synthetic.example", intent="promotion", action="email.archive")


def event(
    number: int,
    kind: FeedbackKind,
    route: Route | None = None,
    action: str | None = None,
) -> FeedbackEvent:
    return FeedbackEvent(
        event_id=f"ev-{number}",
        case_id=f"WAJO-{number:04d}",
        kind=kind,
        explicit_for_learning=is_learnable(kind),
        chosen_route=route,
        chosen_action_id=action,
        recorded_at=WHEN,
    )


def taught() -> tuple[Learner, Router]:
    """A learner and a router that have counted a few real readings."""
    learner = Learner()
    router = Router(learner)
    readings = (
        (event(1, FeedbackKind.APPROVE, Route.PROCEED_AND_NOTIFY), BUCKET),
        (event(2, FeedbackKind.EDIT_DRAFT, Route.ASK_FIRST_WITH_PREDRAFT), BUCKET),
        (event(3, FeedbackKind.REVERT, Route.PROCEED_AND_NOTIFY), BUCKET),
        (event(4, FeedbackKind.REJECT, None), OTHER),
        (
            event(5, FeedbackKind.NEVER_DO_THIS, None, action="email.archive"),
            OTHER,
        ),
    )
    for reading, bucket in readings:
        assert learner.observe(reading, bucket) is True
        assert router.observe(reading, bucket) is True
    return learner, router


def test_a_frozen_run_rebuilds_its_posteriors_cutoffs_and_refusals(tmp_path: Path):
    learner, router = taught()
    live = learner_state.freeze(learner, router)
    path = learner_state.save(tmp_path / "learner.json", learner, router)
    restored, restored_router = learner_state.load(path)

    assert restored.store.counts == learner.store.counts
    assert restored.blocks == learner.blocks
    assert restored.seen == learner.seen
    assert (restored.applied, restored.ignored) == (learner.applied, learner.ignored)
    assert restored_router.thresholds.cutoffs == router.thresholds.cutoffs
    assert restored_router.adapted == router.adapted
    assert restored_router.routings == router.routings
    # The one property that matters: the payload is the same object, field for field.
    assert learner_state.freeze(restored, restored_router) == live


def test_a_decision_reads_the_same_bucket_the_same_way_after_a_thaw(tmp_path: Path):
    """The restored learner has to answer the routing question, not just hold the counts."""
    learner, router = taught()
    before = learner.store.posterior(BUCKET)
    path = learner_state.save(tmp_path / "learner.json", learner, router)
    restored, _ = learner_state.load(path)
    assert restored.store.posterior(BUCKET) == before
    assert restored.refuses(BUCKET) == learner.refuses(BUCKET)


def test_the_frozen_file_is_json_a_reader_can_check(tmp_path: Path):
    learner, router = taught()
    path = learner_state.save(tmp_path / "learner.json", learner, router)
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert sorted(payload) == ["learner", "router", "version"]
    assert payload["version"] == learner_state.FREEZE_VERSION
    assert payload["learner"]["counts"], "a taught learner has to carry its counts"


def test_a_version_this_build_does_not_read_is_refused(tmp_path: Path):
    path = tmp_path / "learner.json"
    path.write_text(json.dumps({"version": 99, "learner": {}, "router": {}}), encoding="utf-8")
    with pytest.raises(ValueError, match="99"):
        learner_state.load(path)


def test_a_malformed_count_names_the_level_it_could_not_read():
    payload = learner_state.freeze(*taught())
    payload["learner"]["counts"][0]["approved"] = "lots"
    with pytest.raises(ValueError, match="malformed"):
        learner_state.thaw(payload)


def test_a_payload_missing_a_section_is_named():
    with pytest.raises(ValueError, match="router"):
        learner_state.thaw({"version": learner_state.FREEZE_VERSION, "learner": {}})


def test_a_file_that_cannot_be_read_is_named(tmp_path: Path):
    missing = tmp_path / "nowhere" / "learner.json"
    with pytest.raises(ValueError, match="nowhere"):
        learner_state.load(missing)
    broken = tmp_path / "broken.json"
    broken.write_text("{not json", encoding="utf-8")
    with pytest.raises(ValueError, match="not JSON"):
        learner_state.load(broken)
