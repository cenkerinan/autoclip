from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import gcd


def _require_positive_timebase(timebase: int) -> None:
    if timebase <= 0:
        raise ValueError("timebase must be > 0")


@dataclass(frozen=True, slots=True)
class TimePoint:
    """Exact timeline coordinate represented as integer ticks / integer timebase."""

    ticks: int
    timebase: int

    def __post_init__(self) -> None:
        _require_positive_timebase(self.timebase)

    @property
    def fraction(self) -> Fraction:
        return Fraction(self.ticks, self.timebase)

    def rescale(self, target_timebase: int) -> "TimePoint":
        _require_positive_timebase(target_timebase)
        scaled = self.fraction * target_timebase
        if scaled.denominator != 1:
            raise ValueError(
                f"timepoint {self.ticks}/{self.timebase} cannot be represented "
                f"exactly at timebase {target_timebase}"
            )
        return TimePoint(int(scaled), target_timebase)

    def equivalent(self, other: "TimePoint") -> bool:
        return self.fraction == other.fraction

    def __lt__(self, other: "TimePoint") -> bool:
        return self.fraction < other.fraction

    def __le__(self, other: "TimePoint") -> bool:
        return self.fraction <= other.fraction

    def __gt__(self, other: "TimePoint") -> bool:
        return self.fraction > other.fraction

    def __ge__(self, other: "TimePoint") -> bool:
        return self.fraction >= other.fraction

    def __sub__(self, other: "TimePoint") -> Fraction:
        return self.fraction - other.fraction

    def to_dict(self) -> dict[str, int]:
        return {"ticks": self.ticks, "timebase": self.timebase}

    @classmethod
    def from_dict(cls, value: dict[str, int]) -> "TimePoint":
        return cls(ticks=int(value["ticks"]), timebase=int(value["timebase"]))

    @classmethod
    def from_seconds_fraction(cls, numerator: int, denominator: int) -> "TimePoint":
        if denominator <= 0:
            raise ValueError("denominator must be > 0")
        common = gcd(abs(numerator), denominator)
        return cls(ticks=numerator // common, timebase=denominator // common)


@dataclass(frozen=True, slots=True)
class TimeRange:
    start: TimePoint
    end: TimePoint

    def __post_init__(self) -> None:
        if self.end < self.start:
            raise ValueError("end must be >= start")

    @property
    def duration(self) -> Fraction:
        return self.end - self.start

    @property
    def is_empty(self) -> bool:
        return self.start.equivalent(self.end)

    def contains(self, point: TimePoint) -> bool:
        return self.start <= point < self.end

    def intersects(self, other: "TimeRange") -> bool:
        return self.start < other.end and other.start < self.end

    def intersection(self, other: "TimeRange") -> "TimeRange | None":
        if not self.intersects(other):
            return None
        start = self.start if self.start >= other.start else other.start
        end = self.end if self.end <= other.end else other.end
        return TimeRange(start=start, end=end)

    def to_dict(self) -> dict[str, dict[str, int]]:
        return {"start": self.start.to_dict(), "end": self.end.to_dict()}

    @classmethod
    def from_dict(cls, value: dict[str, dict[str, int]]) -> "TimeRange":
        return cls(
            start=TimePoint.from_dict(value["start"]),
            end=TimePoint.from_dict(value["end"]),
        )
