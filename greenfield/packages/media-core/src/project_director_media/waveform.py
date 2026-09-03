from __future__ import annotations

from dataclasses import dataclass
from math import ceil
from typing import Iterable


@dataclass(frozen=True, slots=True)
class WaveformLevel:
    samples_per_bucket: int
    peaks: tuple[float, ...]


@dataclass(frozen=True, slots=True)
class WaveformPyramid:
    sample_rate: int
    channels: int
    levels: tuple[WaveformLevel, ...]


def _bucket_peaks(samples: list[float], bucket_size: int) -> tuple[float, ...]:
    if bucket_size <= 0:
        raise ValueError("bucket_size must be > 0")
    if not samples:
        return ()
    out: list[float] = []
    for i in range(0, len(samples), bucket_size):
        chunk = samples[i:i + bucket_size]
        out.append(max(abs(v) for v in chunk))
    return tuple(out)


def build_waveform_pyramid(
    samples: Iterable[float],
    *,
    sample_rate: int,
    channels: int = 1,
    base_bucket_size: int = 160,
    levels: int = 6,
) -> WaveformPyramid:
    """Build multi-resolution peak data for fast timeline zooming.

    Input samples are expected to be mono-normalized floats in [-1, 1].
    Each higher level doubles the bucket size.
    """
    if sample_rate <= 0:
        raise ValueError("sample_rate must be > 0")
    if channels <= 0:
        raise ValueError("channels must be > 0")
    if base_bucket_size <= 0:
        raise ValueError("base_bucket_size must be > 0")
    if levels <= 0:
        raise ValueError("levels must be > 0")

    materialized = [max(-1.0, min(1.0, float(v))) for v in samples]
    result: list[WaveformLevel] = []
    bucket_size = base_bucket_size

    for _ in range(levels):
        result.append(
            WaveformLevel(
                samples_per_bucket=bucket_size,
                peaks=_bucket_peaks(materialized, bucket_size),
            )
        )
        bucket_size *= 2

    return WaveformPyramid(
        sample_rate=sample_rate,
        channels=channels,
        levels=tuple(result),
    )
