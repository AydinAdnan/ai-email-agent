"""Dataset manifest and the split firewall (Phase 3.2).

The dataset is loaded once, canonicalized into ``EmailEvent`` objects, and sorted
by ``sequence_index``. Three lanes come out of it:

- ``CALIBRATION`` (dataset split ``learning_stream``): the only lane the learner
  may update from, and the only lane the interactive simulator may read.
- ``HELD_OUT`` (splits ``golden_ordinary`` and ``golden_adversarial``): sealed.
  Read once by the eval run, never learned from, and the only lane allowed to
  supply route accuracy.
- ``DEVELOPMENT`` (split ``development``): a debug lane with no explicit feedback.
  Readable, teaches nothing, never reported.

Access goes through a ``LaneView``, so interactive code holds a calibration view
and cannot reach a held-out row at all: ``SplitViolation`` is raised at the point
of the attempt, not discovered in the report.
"""
import hashlib
import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from pathlib import Path
from typing import Any

from agent.events import (
    Attachment,
    Direction,
    EmailEvent,
    Message,
    SenderIdentity,
    Thread,
    validate_stream,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATASET_PATH = REPO_ROOT / "docs" / "wajo_dataset.jsonl"


class Lane(StrEnum):
    """Where a case sits relative to learning."""

    CALIBRATION = "calibration"
    HELD_OUT = "held_out"
    DEVELOPMENT = "development"


SPLIT_TO_LANE: Mapping[str, Lane] = {
    "learning_stream": Lane.CALIBRATION,
    "development": Lane.DEVELOPMENT,
    "golden_ordinary": Lane.HELD_OUT,
    "golden_adversarial": Lane.HELD_OUT,
}

# Only the calibration lane may write learner state. Every other lane is read-only
# by construction, so a sealed case can never influence a posterior.
LEARNABLE_LANES = frozenset({Lane.CALIBRATION})


class ManifestError(ValueError):
    """Raised when the dataset itself violates the manifest schema."""


class SplitViolation(RuntimeError):
    """Raised when code reaches across the learning/held-out firewall."""

    code = "SPLIT_VIOLATION"

    def __init__(self, message: str) -> None:
        super().__init__(f"{self.code}: {message}")


@dataclass(frozen=True)
class CaseLabels:
    """The dataset's ground truth for a case.

    These are answers: what the case was designed to be, and the route it was designed
    to deserve. Scoring code reads them; nothing on a decision path may, which is why
    they hang off the case rather than the event.
    """

    intent: str
    relationship_class: str
    action_id: str
    autonomy_outcome: str


@dataclass(frozen=True)
class Case:
    """One dataset row: its lane, its canonical event, its labels and the raw record."""

    case_id: str
    lane: Lane
    split: str
    sequence_index: int
    event: EmailEvent
    row: Mapping[str, Any]

    @property
    def labels(self) -> CaseLabels:
        """The dataset's answer for this case, for scoring and debugging only."""
        incoming = self.row["incoming_email"]
        gold = self.row["gold"]
        return CaseLabels(
            intent=incoming["intent"],
            relationship_class=incoming["relationship_class"],
            action_id=gold["action_id"],
            autonomy_outcome=gold["autonomy_outcome"],
        )


def _sender(raw: Mapping[str, Any]) -> SenderIdentity:
    return SenderIdentity(
        email=raw["email"],
        display_name=raw.get("display_name", ""),
        verified_identity=bool(raw.get("verified_identity", False)),
    )


def _attachment(raw: Mapping[str, Any]) -> Attachment:
    return Attachment(
        filename=raw["filename"],
        content_type=raw.get("content_type", "application/octet-stream"),
        text=raw.get("text"),
        size_bytes=raw.get("size_bytes"),
        sha256=raw.get("sha256"),
        contains_pii=raw.get("contains_pii"),
        contains_financial_data=raw.get("contains_financial_data"),
    )


def _sent_at(raw: Mapping[str, Any]) -> datetime | None:
    stamp = raw.get("timestamp")
    if not stamp:
        return None
    return datetime.fromisoformat(str(stamp).replace("Z", "+00:00"))


def _message(
    raw: Mapping[str, Any],
    thread_id: str,
    direction: Direction = Direction.INBOUND,
) -> Message:
    return Message(
        message_id=raw["message_id"],
        thread_id=thread_id,
        sender=_sender(raw["sender"]),
        recipients=tuple(raw.get("to") or ()),
        cc=tuple(raw.get("cc") or ()),
        direction=direction,
        subject=raw.get("subject", ""),
        body=raw.get("body", ""),
        quoted_text=raw.get("quoted_text"),
        attachments=tuple(_attachment(item) for item in raw.get("attachments") or ()),
        sent_at=_sent_at(raw),
    )


def event_from_row(row: Mapping[str, Any]) -> EmailEvent:
    """Canonicalize one dataset row into an EmailEvent."""
    thread = row["thread"]
    thread_id = thread["thread_id"]
    return EmailEvent(
        case_id=row["case_id"],
        sequence_index=row["sequence_index"],
        message=_message(row["incoming_email"], thread_id),
        thread=Thread(
            thread_id=thread_id,
            messages_before=tuple(
                _message(
                    message,
                    thread_id,
                    Direction(message.get("direction", Direction.INBOUND.value)),
                )
                for message in thread.get("messages_available_before_case") or ()
            ),
            parent_message_id=thread.get("parent_message_id"),
        ),
    )


def _case_from_row(row: Mapping[str, Any]) -> Case:
    split = row.get("split")
    if split not in SPLIT_TO_LANE:
        raise ManifestError(f"case {row.get('case_id')} has unknown split {split!r}")
    return Case(
        case_id=row["case_id"],
        lane=SPLIT_TO_LANE[split],
        split=split,
        sequence_index=row["sequence_index"],
        event=event_from_row(row),
        row=row,
    )


@dataclass(frozen=True)
class Manifest:
    """Every case in the dataset, sorted by sequence index, with its digest.

    ``dataset_digest`` is the hash of the bytes the manifest was built from, so a
    replay can name the exact dataset it ran against.
    """

    cases: tuple[Case, ...]
    dataset_digest: str
    source: str

    @classmethod
    def from_rows(
        cls,
        rows: Sequence[Mapping[str, Any]],
        source: str = "<memory>",
        dataset_digest: str | None = None,
    ) -> "Manifest":
        """Build a manifest from parsed rows, rejecting duplicate case ids and splits."""
        cases = [_case_from_row(row) for row in rows]
        seen: set[str] = set()
        for case in cases:
            if case.case_id in seen:
                raise ManifestError(f"case {case.case_id} appears twice in the dataset")
            seen.add(case.case_id)
        ordered = tuple(sorted(cases, key=lambda case: case.sequence_index))
        validate_stream(tuple(case.event for case in ordered))
        if dataset_digest is None:
            dataset_digest = hashlib.sha256(
                "\n".join(json.dumps(dict(case.row), sort_keys=True) for case in ordered).encode()
            ).hexdigest()
        return cls(cases=ordered, dataset_digest=dataset_digest, source=source)

    @classmethod
    def load(cls, path: Path | str = DEFAULT_DATASET_PATH) -> "Manifest":
        """Load the manifest from a JSONL dataset file."""
        dataset_path = Path(path)
        payload = dataset_path.read_bytes()
        rows = [
            json.loads(line)
            for line in payload.decode("utf-8").splitlines()
            if line.strip()
        ]
        return cls.from_rows(
            rows,
            source=str(dataset_path),
            dataset_digest=hashlib.sha256(payload).hexdigest(),
        )

    def view(self, lane: Lane) -> "LaneView":
        """Return the lane-bound handle for one lane."""
        return LaneView(manifest=self, lane=lane)

    def lane_cases(self, lane: Lane) -> tuple[Case, ...]:
        """Every case in one lane, in sequence order."""
        return tuple(case for case in self.cases if case.lane == lane)

    def summary(self) -> dict[str, int]:
        """Counts per split and per lane, for the validator's output."""
        summary: dict[str, int] = {}
        for case in self.cases:
            summary[case.split] = summary.get(case.split, 0) + 1
            key = f"lane:{case.lane.value}"
            summary[key] = summary.get(key, 0) + 1
        return summary


class LaneView:
    """A lane-bound handle over the manifest.

    A view can only open cases in its own lane, and only a learnable lane may
    write learner state. Both refusals raise SplitViolation.
    """

    def __init__(self, manifest: Manifest, lane: Lane) -> None:
        self._manifest = manifest
        self._lane = lane

    @property
    def lane(self) -> Lane:
        return self._lane

    @property
    def manifest(self) -> Manifest:
        return self._manifest

    @property
    def cases(self) -> tuple[Case, ...]:
        return self._manifest.lane_cases(self._lane)

    @property
    def case_ids(self) -> tuple[str, ...]:
        return tuple(case.case_id for case in self.cases)

    def events(self) -> tuple[EmailEvent, ...]:
        """The lane's arriving events, in sequence order."""
        return tuple(case.event for case in self.cases)

    def open(self, case_id: str) -> Case:
        """Open one case from this lane. Refuses any other lane's case."""
        for case in self.cases:
            if case.case_id == case_id:
                return case
        if any(case.case_id == case_id for case in self._manifest.cases):
            raise SplitViolation(
                f"lane '{self._lane.value}' may not open case {case_id}; it belongs to another lane"
            )
        raise KeyError(case_id)

    def can_write_learner_state(self) -> bool:
        """Whether this lane may update the learner."""
        return self._lane in LEARNABLE_LANES

    def require_learner_write(self) -> None:
        """Refuse a learner write from a lane that is not allowed to teach."""
        if not self.can_write_learner_state():
            raise SplitViolation(
                f"lane '{self._lane.value}' may not write learner state; "
                "only the calibration lane can"
            )


__all__ = [
    "DEFAULT_DATASET_PATH",
    "LEARNABLE_LANES",
    "SPLIT_TO_LANE",
    "Case",
    "CaseLabels",
    "Lane",
    "LaneView",
    "Manifest",
    "ManifestError",
    "SplitViolation",
    "event_from_row",
]
