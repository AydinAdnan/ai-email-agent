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
import re
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
    EventValidationError,
    FeedbackKind,
    Message,
    SenderIdentity,
    Thread,
    validate_stream,
)
from agent.safety.floor import Route
from agent.tools.email_tools import ACTION_TO_TOOL

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATASET_PATH = REPO_ROOT / "datasets" / "wajo_cases.jsonl"

SCHEMA_VERSION = "wajo_dataset_v1"

# The sizes the case set has to reach: below this the ask-rate curve is noise and the
# held-out accuracy is one lucky case. Checked rather than assumed, so a truncated file
# fails at validation instead of quietly reporting a confident number.
MIN_LEARNING_CASES = 30
MIN_SEALED_CASES = 10

# The generator fills a body in later for rows it only sketched. Such a row still carries
# a gold route, so it scores, but triage sees no text: worth saying out loud, not a failure.
_PLACEHOLDER_BODY = re.compile(r"detailed email body according to scenario", re.IGNORECASE)
_REPLY_PREFIX = re.compile(r"^\s*(?:re|fwd)\s*:\s*", re.IGNORECASE)

# What every case has to carry for the pipeline to run it and for the report to score it.
_CASE_FIELDS = (
    "schema_version",
    "case_id",
    "split",
    "sequence_index",
    "timestamp",
    "canonical_candidate_action.action_id",
    "gold.autonomy_outcome",
    "incoming_email.sender.email",
    "incoming_email.subject",
    "thread.thread_id",
    "observed_user_feedback.kind",
    "safety_floor.autonomy_ceiling",
)


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
    def labelled(self) -> bool:
        """Whether this case carries the dataset's answer at all."""
        return "gold" in self.row and "incoming_email" in self.row

    @property
    def labels(self) -> CaseLabels:
        """The dataset's answer for this case, for scoring and debugging only."""
        try:
            incoming = self.row["incoming_email"]
            gold = self.row["gold"]
            return CaseLabels(
                intent=incoming["intent"],
                relationship_class=incoming["relationship_class"],
                action_id=gold["action_id"],
                autonomy_outcome=gold["autonomy_outcome"],
            )
        except (KeyError, TypeError) as error:
            raise ManifestError(
                f"case {self.case_id} has no {error} label: this input carried mail only"
            ) from error


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


def _case_from_mail_row(row: Mapping[str, Any], index: int) -> Case:
    """Turn one plain mail row into a case the simulator can walk.

    Missing ids are synthesised deterministically, and the lane is calibration because
    an interactive mailbox is where a user may teach from. A row that carries no
    verification signal is treated as delivered mail rather than as a spoof attempt: a
    mailbox that knows its own SPF/DMARC result should say so per row.
    """
    case_id = str(row.get("case_id") or f"mail-{index:04d}")
    thread_id = str(row.get("thread_id") or f"th-{index:04d}")
    sender = row.get("sender", row.get("from", ""))
    if isinstance(sender, Mapping):
        identity = SenderIdentity(
            email=str(sender.get("email", "")),
            display_name=str(sender.get("display_name", "")),
            verified_identity=bool(sender.get("verified_identity", True)),
        )
    else:
        identity = SenderIdentity(email=str(sender), verified_identity=True)
    if not identity.email:
        raise ManifestError(f"{case_id}: a mail row needs a sender address")

    def addresses(key: str) -> tuple[str, ...]:
        value = row.get(key) or ()
        if isinstance(value, str):
            value = [item.strip() for item in value.split(",") if item.strip()]
        return tuple(str(item) for item in value)

    message = Message(
        message_id=str(row.get("message_id") or f"msg-{index:04d}"),
        thread_id=thread_id,
        sender=identity,
        recipients=addresses("to"),
        cc=addresses("cc"),
        direction=Direction.INBOUND,
        subject=str(row.get("subject", "")),
        body=str(row.get("body", "")),
        attachments=tuple(_attachment(item) for item in row.get("attachments") or ()),
        sent_at=_sent_at(row),
    )
    event = EmailEvent(
        case_id=case_id,
        sequence_index=index,
        message=message,
        thread=Thread(
            thread_id=thread_id,
            parent_message_id=row.get("parent_message_id"),
        ),
    )
    return Case(
        case_id=case_id,
        lane=SPLIT_TO_LANE["learning_stream"],
        split="learning_stream",
        sequence_index=index,
        event=event,
        row=row,
    )


def _case_from_row(row: Mapping[str, Any]) -> Case:
    """Build one case, naming the case on anything the row gets wrong.

    A bare ``KeyError: 'gold'`` from a malformed row says nothing about which of a
    hundred and forty rows is malformed, which is the only thing a reader needs.
    """
    case_id = str(row.get("case_id", "<row without a case_id>"))
    split = row.get("split")
    if split not in SPLIT_TO_LANE:
        raise ManifestError(f"case {case_id} has unknown split {split!r}")
    try:
        sequence_index = row["sequence_index"]
        event = event_from_row(row)
    except (KeyError, TypeError, ValueError) as error:
        raise ManifestError(f"case {case_id}: {type(error).__name__}: {error}") from error
    return Case(
        case_id=case_id,
        lane=SPLIT_TO_LANE[split],
        split=split,
        sequence_index=sequence_index,
        event=event,
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
    def from_mail_rows(
        cls,
        rows: Sequence[Mapping[str, Any]],
        source: str = "<mail>",
        dataset_digest: str | None = None,
    ) -> "Manifest":
        """Build a manifest from plain mail: sender, recipients, subject and body.

        A stream of real mail has no window, no gold route and no labels, so this makes
        the shape the simulator needs and leaves the labels absent - ``Case.labels``
        then refuses, which is the point: a case nobody labelled cannot be scored.
        Everything the pipeline decides about such mail has to come from the mail.
        """
        cases = tuple(
            _case_from_mail_row(row, index) for index, row in enumerate(rows, start=1)
        )
        if not cases:
            raise ManifestError(f"{source} holds no mail")
        validate_stream(tuple(case.event for case in cases))
        if dataset_digest is None:
            dataset_digest = hashlib.sha256(
                "\n".join(json.dumps(dict(case.row), sort_keys=True) for case in cases).encode()
            ).hexdigest()
        return cls(cases=cases, dataset_digest=dataset_digest, source=source)

    @classmethod
    def load(
        cls, path: Path | str = DEFAULT_DATASET_PATH, *, mail_only: bool = False
    ) -> "Manifest":
        """Load the manifest from a JSONL dataset file, or from plain mail rows."""
        dataset_path = Path(path)
        try:
            payload = dataset_path.read_bytes()
        except OSError as error:
            raise ManifestError(f"cannot read dataset {dataset_path}: {error}") from error
        rows: list[Mapping[str, Any]] = []
        for number, line in enumerate(payload.decode("utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as error:
                raise ManifestError(
                    f"{dataset_path}: line {number} is not JSON: {error}"
                ) from error
        build = cls.from_mail_rows if mail_only else cls.from_rows
        return build(
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
        raise KeyError(f"no case {case_id!r} in {self._manifest.source}")

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


@dataclass(frozen=True)
class DatasetProblem:
    """One thing the case set gets wrong, named so it can be found and fixed."""

    code: str
    case_id: str
    detail: str

    def describe(self) -> str:
        return f"{self.code:<18} {self.case_id:<12} {self.detail}"


@dataclass(frozen=True)
class CaseReport:
    """What the case set holds and whatever is wrong with it.

    ``ok`` is about problems only: a warning is something a reader should know and a
    run may proceed past, an empty case set or a scenario in two lanes is not.
    """

    source: str
    digest: str
    split_counts: Mapping[str, int]
    lane_counts: Mapping[str, int]
    problems: tuple[DatasetProblem, ...] = ()
    warnings: tuple[DatasetProblem, ...] = ()

    @property
    def total(self) -> int:
        return sum(self.split_counts.values())

    @property
    def learning(self) -> int:
        return self.lane_counts.get(Lane.CALIBRATION.value, 0)

    @property
    def sealed(self) -> int:
        return self.lane_counts.get(Lane.HELD_OUT.value, 0)

    @property
    def ok(self) -> bool:
        return not self.problems

    def render(self) -> str:
        """The report as a reader sees it: counts first, then what fails."""
        lines = [f"case set: {self.source}", f"digest: {self.digest[:16]}"]
        for split in SPLIT_TO_LANE:
            count = self.split_counts.get(split, 0)
            lines.append(f"  {split:<20} {count:>4}  lane {SPLIT_TO_LANE[split].value}")
        lines.append(
            f"learning {self.learning}  sealed {self.sealed}"
            f"  development {self.lane_counts.get(Lane.DEVELOPMENT.value, 0)}"
            f"  total {self.total}"
        )
        for problem in self.problems:
            lines.append(f"problem: {problem.describe()}")
        # A warning repeats: one line per code, with the cases that carry it, keeps a
        # placeholder body in a quarter of the file from burying the counts it sits under.
        for code in dict.fromkeys(warning.code for warning in self.warnings):
            named = [warning for warning in self.warnings if warning.code == code]
            shown = ", ".join(warning.case_id for warning in named[:6])
            more = f" and {len(named) - 6} more" if len(named) > 6 else ""
            lines.append(f"warning: {code} on {len(named)} case(s): {shown}{more}")
            lines.append(f"         {named[0].detail}")
        if self.ok:
            lines.append("ok: counts, enums and splits hold")
        else:
            lines.append(f"failed: {len(self.problems)} problem(s) in the case set")
        return "\n".join(lines)


def _value(row: Mapping[str, Any], path: str, default: Any = None) -> Any:
    """Read a dotted path out of a row, or the default when any step is absent."""
    found: Any = row
    for step in path.split("."):
        if not isinstance(found, Mapping) or step not in found:
            return default
        found = found[step]
    return found


def _scenario(row: Mapping[str, Any]) -> tuple[str, str] | None:
    """The scenario a rule would be scoped to: who sent it, and about what.

    Sender plus subject is the narrowest scope a learned preference can cover, which
    makes it exactly the key that must not repeat across the learning and the sealed
    lane: a held-out case the learner was already taught is not held out at all.
    """
    sender = str(_value(row, "incoming_email.sender.email", "")).strip().lower()
    subject = str(_value(row, "incoming_email.subject", "")).strip().lower()
    subject = _REPLY_PREFIX.sub("", subject)
    subject = " ".join(subject.split())
    if not sender or not subject:
        return None
    return (sender, subject)


def _row_problems(row: Mapping[str, Any], number: int) -> tuple[list[DatasetProblem], list[DatasetProblem]]:
    """Check one row's fields and enums. Returns its problems and its warnings."""
    case_id = str(row.get("case_id") or f"line {number}")
    problems: list[DatasetProblem] = []
    warnings: list[DatasetProblem] = []

    for path in _CASE_FIELDS:
        if _value(row, path) in (None, ""):
            problems.append(DatasetProblem("MISSING_FIELD", case_id, f"no {path}"))

    version = _value(row, "schema_version")
    if version is not None and version != SCHEMA_VERSION:
        problems.append(
            DatasetProblem(
                "SCHEMA_VERSION",
                case_id,
                f"{version!r} is not the {SCHEMA_VERSION!r} the loader reads",
            )
        )

    split = _value(row, "split")
    if split is not None and split not in SPLIT_TO_LANE:
        problems.append(
            DatasetProblem(
                "UNKNOWN_SPLIT", case_id, f"{split!r} is not one of {', '.join(SPLIT_TO_LANE)}"
            )
        )

    outcome = _value(row, "gold.autonomy_outcome")
    if outcome is not None and outcome not in {route.value for route in Route}:
        problems.append(DatasetProblem("UNKNOWN_ROUTE", case_id, f"{outcome!r} is not a route"))

    ceiling = _value(row, "safety_floor.autonomy_ceiling")
    if ceiling is not None and ceiling not in {route.value for route in Route}:
        problems.append(DatasetProblem("UNKNOWN_CEILING", case_id, f"{ceiling!r} is not a route"))

    kind = _value(row, "observed_user_feedback.kind")
    if kind is not None:
        try:
            FeedbackKind(str(kind))
        except ValueError:
            problems.append(
                DatasetProblem("UNKNOWN_FEEDBACK", case_id, f"{kind!r} is not a feedback kind")
            )

    action_id = _value(row, "canonical_candidate_action.action_id")
    if action_id is not None and action_id not in ACTION_TO_TOOL and outcome != Route.ESCALATE.value:
        problems.append(
            DatasetProblem(
                "UNKNOWN_ACTION",
                case_id,
                f"nothing implements {action_id!r}, so its gold route can only be ESCALATE, not {outcome!r}",
            )
        )

    sealed = split in SPLIT_TO_LANE and SPLIT_TO_LANE[split] is Lane.HELD_OUT
    if sealed and _value(row, "observed_user_feedback.explicit_for_learning"):
        problems.append(
            DatasetProblem(
                "SEALED_FEEDBACK",
                case_id,
                "a sealed case carries explicit learning feedback, which would teach on the held-out run",
            )
        )

    body = str(_value(row, "incoming_email.body", ""))
    if not body.strip() or _PLACEHOLDER_BODY.search(body):
        warnings.append(
            DatasetProblem(
                "PLACEHOLDER_BODY",
                case_id,
                "the body is the generator's placeholder, so the row cannot exercise triage",
            )
        )
    return problems, warnings


def validate_cases(path: Path | str = DEFAULT_DATASET_PATH) -> CaseReport:
    """Check a case set's counts, enums and splits before anything is asked to run it.

    Reports every problem it finds rather than the first, because a case set is edited
    in one sitting and a reader wants the whole list. The manifest is built at the end
    as a backstop: whatever the field checks do not reach, the loader does.
    """
    dataset_path = Path(path)
    try:
        payload = dataset_path.read_bytes()
    except OSError as error:
        raise ManifestError(f"cannot read dataset {dataset_path}: {error}") from error

    rows: list[Mapping[str, Any]] = []
    problems: list[DatasetProblem] = []
    warnings: list[DatasetProblem] = []
    for number, line in enumerate(payload.decode("utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as error:
            problems.append(DatasetProblem("NOT_JSON", f"line {number}", str(error)))
            continue
        if not isinstance(row, Mapping):
            problems.append(
                DatasetProblem("ROW_SHAPE", f"line {number}", "a case has to be a JSON object")
            )
            continue
        found, noted = _row_problems(row, number)
        problems.extend(found)
        warnings.extend(noted)
        rows.append(row)

    split_counts: dict[str, int] = {}
    lane_counts: dict[str, int] = {}
    for row in rows:
        split = str(_value(row, "split"))
        split_counts[split] = split_counts.get(split, 0) + 1
        lane = SPLIT_TO_LANE.get(split)
        if lane is not None:
            lane_counts[lane.value] = lane_counts.get(lane.value, 0) + 1

    problems.extend(_split_problems(rows))
    learning = lane_counts.get(Lane.CALIBRATION.value, 0)
    sealed = lane_counts.get(Lane.HELD_OUT.value, 0)
    for count, floor, lane in (
        (learning, MIN_LEARNING_CASES, Lane.CALIBRATION),
        (sealed, MIN_SEALED_CASES, Lane.HELD_OUT),
    ):
        if count < floor:
            problems.append(
                DatasetProblem(
                    "TOO_FEW_CASES",
                    lane.value,
                    f"{count} case(s) in this lane; the case set needs at least {floor}",
                )
            )

    digest = hashlib.sha256(payload).hexdigest()
    try:
        Manifest.from_rows(rows, source=str(dataset_path), dataset_digest=digest)
    except (ManifestError, EventValidationError) as error:
        problems.append(DatasetProblem("LOAD", "<file>", str(error)))

    return CaseReport(
        source=str(dataset_path),
        digest=digest,
        split_counts=split_counts,
        lane_counts=lane_counts,
        problems=tuple(problems),
        warnings=tuple(warnings),
    )


def _split_problems(rows: Sequence[Mapping[str, Any]]) -> list[DatasetProblem]:
    """The cross-row checks: ids and ordering, and nothing landing in two lanes."""
    problems: list[DatasetProblem] = []
    seen_ids: set[str] = set()
    seen_order: dict[int, str] = {}
    scenarios: dict[tuple[str, str], list[tuple[str, str]]] = {}
    threads: dict[str, list[tuple[str, str]]] = {}

    for row in rows:
        case_id = str(_value(row, "case_id", "<row without a case_id>"))
        split = str(_value(row, "split", ""))
        if case_id in seen_ids:
            problems.append(DatasetProblem("DUPLICATE_CASE_ID", case_id, "appears twice"))
        seen_ids.add(case_id)

        index = _value(row, "sequence_index")
        if isinstance(index, int):
            first = seen_order.get(index)
            if first is not None:
                problems.append(
                    DatasetProblem(
                        "DUPLICATE_SEQUENCE", case_id, f"sequence_index {index} is also {first}'s"
                    )
                )
            seen_order[index] = case_id

        scenario = _scenario(row)
        if scenario is not None:
            scenarios.setdefault(scenario, []).append((case_id, split))
        thread_id = str(_value(row, "thread.thread_id", ""))
        if thread_id:
            threads.setdefault(thread_id, []).append((case_id, split))

    for found, label in ((scenarios, "scenario"), (threads, "thread")):
        for key, holders in found.items():
            splits = {split for _, split in holders}
            if len(splits) < 2:
                continue
            # The case named is the one that crossed: a leak is reported against the row
            # in the wrong lane, not against whichever lane happened to come first.
            intruder, intruder_split = next(
                (case_id, split) for case_id, split in holders if split != holders[0][1]
            )
            others = "; ".join(
                f"{split} as {case_id}" for case_id, split in holders if split != intruder_split
            )
            name = key if label == "thread" else f"{key[0]} / {key[1]}"
            problems.append(
                DatasetProblem(
                    "SPLIT_LEAK",
                    intruder,
                    f"{label} {name!r} is also {others} ({intruder_split} against those)",
                )
            )
    return problems


__all__ = [
    "DEFAULT_DATASET_PATH",
    "LEARNABLE_LANES",
    "MIN_LEARNING_CASES",
    "MIN_SEALED_CASES",
    "SCHEMA_VERSION",
    "SPLIT_TO_LANE",
    "Case",
    "CaseLabels",
    "CaseReport",
    "DatasetProblem",
    "Lane",
    "LaneView",
    "Manifest",
    "ManifestError",
    "SplitViolation",
    "event_from_row",
    "validate_cases",
]
