from fractions import Fraction

import pytest

from project_director_media import TimePoint, TimeRange


def t(ticks: int, timebase: int = 1000) -> TimePoint:
    return TimePoint(ticks, timebase)


def test_equivalent_points_across_timebases() -> None:
    assert TimePoint(1, 2).equivalent(TimePoint(500, 1000))


def test_exact_rescale() -> None:
    assert TimePoint(1, 2).rescale(1000) == TimePoint(500, 1000)


def test_inexact_rescale_is_rejected() -> None:
    with pytest.raises(ValueError):
        TimePoint(1, 3).rescale(1000)


def test_range_intersection() -> None:
    a = TimeRange(t(100), t(500))
    b = TimeRange(t(400), t(800))
    assert a.intersection(b) == TimeRange(t(400), t(500))
    assert a.duration == Fraction(2, 5)


def test_touching_ranges_do_not_intersect() -> None:
    assert not TimeRange(t(0), t(100)).intersects(TimeRange(t(100), t(200)))
