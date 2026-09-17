"""Phase 3.5: windowed-random arrival scheduling."""
from types import SimpleNamespace

import pytest

from agent.sim.schedule import ScheduleError, release_order, schedule


def fake(case_id: str, **row) -> SimpleNamespace:
    """A case the scheduler can order: it reads an id and a row, nothing else."""
    return SimpleNamespace(case_id=case_id, row=row)


def lane(size: int = 25) -> tuple:
    return tuple(fake(f"case-{index:03}") for index in range(1, size + 1))


def test_the_lane_is_cut_into_windows_and_no_case_crosses_a_boundary() -> None:
    cases = lane(25)
    windows = schedule(cases, seed=7)
    assert [len(item.cases) for item in windows] == [10, 10, 5]
    assert [item.index for item in windows] == [1, 2, 3]
    for index, item in enumerate(windows):
        # Each window holds exactly its slice of the lane, however it was drawn.
        assert set(item.case_ids) == {case.case_id for case in cases[index * 10 : (index + 1) * 10]}
    assert sorted(case_id for item in windows for case_id in item.case_ids) == [
        case.case_id for case in cases
    ]


def test_seed_17_and_seed_18_agree_on_the_partition_and_not_on_the_order() -> None:
    cases = lane(40)
    one = schedule(cases, seed=17)
    other = schedule(cases, seed=18)
    assert [item.case_ids for item in one] != [item.case_ids for item in other]
    for first, second in zip(one, other, strict=True):
        assert set(first.case_ids) == set(second.case_ids)
    # Inside a full window the two seeds disagree about the order, not about the cases.
    assert one[0].case_ids != other[0].case_ids


def test_the_same_seed_draws_the_same_order() -> None:
    once = [item.case_ids for item in schedule(lane(30), seed=7)]
    again = [item.case_ids for item in schedule(lane(30), seed=7)]
    assert once == again


def test_each_window_records_the_seed_that_ordered_it() -> None:
    assert [item.seed for item in schedule(lane(20), seed=7)] == ["7:1", "7:2"]


def test_a_dependency_is_delivered_before_the_case_that_names_it() -> None:
    cases = (fake("a"), fake("b", depends_on=["a"]), fake("c"), fake("d"), fake("e"))
    order = [case.case_id for case in release_order(cases, seed=3)]
    assert order.index("a") < order.index("b")
    assert sorted(order) == ["a", "b", "c", "d", "e"]


def test_not_before_case_is_the_same_constraint() -> None:
    cases = (fake("a"), fake("b", not_before_case="a"), fake("c", not_before_case="b"))
    assert [case.case_id for case in release_order(cases, seed=11)] == ["a", "b", "c"]


def test_a_dependency_outside_its_window_is_refused() -> None:
    """A dependency nothing releases cannot be honoured by shuffling around it."""
    cases = (
        fake("early", depends_on=["late"]),
        *(fake(f"filler-{index}") for index in range(1, 11)),
        fake("late"),
    )
    with pytest.raises(ScheduleError) as caught:
        schedule(cases, window=10, seed=7)
    assert "early waits for late" in str(caught.value)


def test_a_window_holds_at_least_one_case() -> None:
    with pytest.raises(ValueError):
        schedule(lane(3), window=0)
