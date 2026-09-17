"""Windowed-random arrival scheduling (plan Commit 3.5).

A lane replayed in sequence order is a burst: every newsletter, then every vendor
receipt, then the interesting mail. A burst cannot show whether the agent interrupts at
a rate a person would tolerate, because the interruptions arrive back to back. So the
lane is cut into ordered windows and the order inside a window is drawn from the run's
seed. The partition is fixed, the order inside a window is nobody's design, and no case
crosses a window boundary - which is what makes two seeds comparable: seed 17 and seed
18 disagree about the order inside a window and agree about which cases belong together.

Order is drawn per window from ``"<seed>:<window>"`` rather than one generator walked
in sequence, so a window's order survives a change to the case set in another window,
and a single window can be reproduced without replaying everything before it.

A row may declare ``depends_on`` (one id or a list) or ``not_before_case`` (one id), and
those are checked before release. The dataset does not use either field yet; when a case
does, it must not be delivered before what it builds on, and a dependency its own window
cannot satisfy is a dataset error rather than a reason to shuffle quietly around it.
"""
import random
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import Any

from agent.dataset import Case

# The plan's window: ten arrivals is a session's worth of inbox before time moves on.
WINDOW_SIZE = 10


class ScheduleError(RuntimeError):
    """Raised when a case names a dependency no window can deliver before it."""


@dataclass(frozen=True)
class Window:
    """One released window: its cases in delivery order, and the seed that ordered it."""

    index: int
    seed: str
    cases: tuple[Case, ...]

    @property
    def case_ids(self) -> tuple[str, ...]:
        """The window's case ids in the order they will arrive."""
        return tuple(case.case_id for case in self.cases)


def _row_of(case: Case) -> Mapping[str, Any]:
    row = getattr(case, "row", None)
    return row if isinstance(row, Mapping) else {}


def dependencies_of(case: Case) -> tuple[str, ...]:
    """The ids a case says must arrive before it, from ``depends_on``/``not_before_case``."""
    row = _row_of(case)
    declared = [str(name) for name in (row.get("depends_on") or ())]
    sole = row.get("not_before_case")
    if sole:
        declared.append(str(sole))
    # A case cannot wait for itself, and a repeated id is still one dependency.
    return tuple(name for name in dict.fromkeys(declared) if name != case.case_id)


def schedule(cases: Iterable[Case], *, window: int = WINDOW_SIZE, seed: int = 7) -> tuple[Window, ...]:
    """Cut a lane into ordered windows, shuffling only inside each one."""
    if window < 1:
        raise ValueError("a window holds at least one case")
    windows: list[Window] = []
    released: set[str] = set()
    ordered = tuple(cases)
    for index, start in enumerate(range(0, len(ordered), window), start=1):
        drawn = list(ordered[start : start + window])
        window_seed = f"{seed}:{index}"
        # A seeded draw for a reproducible order, not a secret.
        random.Random(window_seed).shuffle(drawn)  # noqa: S311
        placed = _dependencies_first(drawn, released)
        released.update(case.case_id for case in placed)
        windows.append(Window(index=index, seed=window_seed, cases=tuple(placed)))
    return tuple(windows)


def release_order(cases: Iterable[Case], *, window: int = WINDOW_SIZE, seed: int = 7) -> tuple[Case, ...]:
    """Every case in the order the windows will deliver them."""
    return tuple(case for item in schedule(cases, window=window, seed=seed) for case in item.cases)


def _dependencies_first(drawn: list[Case], released: set[str]) -> list[Case]:
    """Keep the drawn order, moving a case after anything it says it waits for.

    Reordering is confined to the window: a case only ever moves later than where it was
    drawn, and only past cases it named. A dependency that is not in this window and was
    not released by an earlier one cannot be honoured at all, so it raises.
    """
    placed: list[Case] = []
    done = set(released)
    pending = list(drawn)
    while pending:
        ready = [case for case in pending if set(dependencies_of(case)) <= done]
        if not ready:
            blocked = pending[0]
            missing = sorted(set(dependencies_of(blocked)) - done)
            raise ScheduleError(
                f"case {blocked.case_id} waits for {', '.join(missing)}, which is not "
                f"released by its own window: a dependency that crosses a window "
                f"boundary is a dataset error, not a scheduling choice"
            )
        for case in ready:
            pending.remove(case)
            placed.append(case)
            done.add(case.case_id)
    return placed


__all__ = [
    "WINDOW_SIZE",
    "ScheduleError",
    "Window",
    "dependencies_of",
    "release_order",
    "schedule",
]
