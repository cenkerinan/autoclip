from fractions import Fraction

from project_director_media import TimePoint, TimeRange, boundary_samples, evenly_spaced_samples


def test_even_sampling_is_exact() -> None:
    samples = evenly_spaced_samples(
        TimeRange(TimePoint(0, 1), TimePoint(10, 1)), count=3
    )
    assert [s.at.fraction for s in samples] == [Fraction(0), Fraction(5), Fraction(10)]


def test_boundary_sampling_clamps_before_zero() -> None:
    ranges = boundary_samples((TimePoint(1, 2),), context=Fraction(3, 2))
    assert ranges[0].start.fraction == 0
    assert ranges[0].end.fraction == 2
