from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from .timecode import TimePoint, TimeRange


@dataclass(frozen=True, slots=True)
class EvidenceSample:
    at: TimePoint
    reason: str


def evenly_spaced_samples(
    range_: TimeRange,
    *,
    count: int,
    reason: str = "uniform",
) -> tuple[EvidenceSample, ...]:
    if count <= 0:
        raise ValueError("count must be > 0")
    if range_.is_empty:
        return (EvidenceSample(range_.start, reason),)
    if count == 1:
        midpoint = range_.start.fraction + range_.duration / 2
        return (
            EvidenceSample(
                TimePoint(midpoint.numerator, midpoint.denominator),
                reason,
            ),
        )

    step = range_.duration / (count - 1)
    out: list[EvidenceSample] = []
    for i in range(count):
        point = range_.start.fraction + step * i
        out.append(
            EvidenceSample(
                at=TimePoint(point.numerator, point.denominator),
                reason=reason,
            )
        )
    return tuple(out)


def boundary_samples(
    cuts: tuple[TimePoint, ...],
    *,
    context: Fraction = Fraction(3, 2),
) -> tuple[TimeRange, ...]:
    if context <= 0:
        raise ValueError("context must be > 0")
    out: list[TimeRange] = []
    for cut in cuts:
        start_fraction = cut.fraction - context
        if start_fraction < 0:
            start_fraction = Fraction(0, 1)
        end_fraction = cut.fraction + context
        out.append(
            TimeRange(
                TimePoint(start_fraction.numerator, start_fraction.denominator),
                TimePoint(end_fraction.numerator, end_fraction.denominator),
            )
        )
    return tuple(out)
