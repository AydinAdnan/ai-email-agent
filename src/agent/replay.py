"""Seeded clock and append-only event stream (Phase 3.2).

Replay has to be reproducible before anything can be measured, so nothing here
reads wall-clock time: the clock starts at a fixed epoch plus the seed, and moves
only when the simulation advances it. The stream is append-only and revalidates
on every append, so a duplicate or out-of-order arrival is refused instead of
being quietly recorded, and two runs of the same seed emit byte-identical logs.
"""
import hashlib
import json
from dataclasses import asdict
from datetime import UTC, datetime, timedelta
from typing import Any

from agent.events import EmailEvent, validate_stream

# The dataset's first arrival, so simulated processing time lines up with it.
DATASET_EPOCH = datetime(2026, 8, 1, 8, 15, tzinfo=UTC)


def _json_default(value: Any) -> str:
    if isinstance(value, datetime):
        return value.isoformat()
    return str(value)


class SeededClock:
    """A deterministic clock. Time moves because the simulation says so."""

    def __init__(
        self,
        seed: int,
        start: datetime = DATASET_EPOCH,
        tick: timedelta = timedelta(minutes=1),
    ) -> None:
        self.seed = seed
        self.tick = tick
        self.started_at = start + timedelta(seconds=seed % 60)
        self._now = self.started_at
        self.ticks = 0

    def now(self) -> datetime:
        """The current simulated time."""
        return self._now

    def advance(self, ticks: int = 1) -> datetime:
        """Move simulated time forward and return the new time."""
        if ticks < 1:
            raise ValueError("advance() needs a positive number of ticks")
        self._now += self.tick * ticks
        self.ticks += ticks
        return self._now


class EventStream:
    """An append-only log of arriving events.

    There is no update, no delete and no reorder: the only way in is ``append``,
    and every append has to survive the ordering and duplicate rules before it is
    recorded.
    """

    def __init__(self, clock: SeededClock) -> None:
        self._clock = clock
        self._events: list[EmailEvent] = []
        self._delivered_at: list[datetime] = []

    @property
    def clock(self) -> SeededClock:
        return self._clock

    @property
    def events(self) -> tuple[EmailEvent, ...]:
        """Every appended event, in arrival order."""
        return tuple(self._events)

    def __len__(self) -> int:
        return len(self._events)

    def append(self, event: EmailEvent) -> EmailEvent:
        """Record one arrival, or refuse it and leave the stream untouched.

        The whole stream is revalidated per append. That is O(n^2) and fine for a
        few hundred cases; incremental bookkeeping can replace it if the dataset
        ever grows by orders of magnitude.
        """
        self._events.append(event)
        try:
            validate_stream(self._events)
        except Exception:
            self._events.pop()
            raise
        self._delivered_at.append(self._clock.advance())
        return event

    def log_jsonl(self) -> str:
        """The canonical JSONL replay log: header line, then one line per arrival."""
        header = {
            "seed": self._clock.seed,
            "started_at": self._clock.started_at.isoformat(),
            "tick_seconds": int(self._clock.tick.total_seconds()),
            "event_count": len(self._events),
        }
        lines = [self._line(header)]
        lines.extend(
            self._line(
                {
                    "sequence_index": event.sequence_index,
                    "delivered_at": delivered_at.isoformat(),
                    "event": asdict(event),
                }
            )
            for event, delivered_at in zip(self._events, self._delivered_at, strict=True)
        )
        return "".join(lines)

    def digest(self) -> str:
        """A stable hash of the replay log."""
        return hashlib.sha256(self.log_jsonl().encode("utf-8")).hexdigest()

    @staticmethod
    def _line(payload: dict[str, Any]) -> str:
        return json.dumps(payload, sort_keys=True, separators=(",", ":"), default=_json_default) + "\n"


def replay(
    events: tuple[EmailEvent, ...] | list[EmailEvent],
    seed: int,
    start: datetime = DATASET_EPOCH,
    tick: timedelta = timedelta(minutes=1),
) -> EventStream:
    """Replay events through a fresh seeded stream."""
    stream = EventStream(SeededClock(seed=seed, start=start, tick=tick))
    for event in events:
        stream.append(event)
    return stream


__all__ = [
    "DATASET_EPOCH",
    "EventStream",
    "SeededClock",
    "replay",
]
