from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from fractions import Fraction
from typing import Any

from .timecode import TimePoint


class AssetKind(StrEnum):
    VIDEO = "video"
    AUDIO = "audio"
    IMAGE = "image"
    SUBTITLE = "subtitle"
    GENERATED = "generated"


class StreamKind(StrEnum):
    VIDEO = "video"
    AUDIO = "audio"
    SUBTITLE = "subtitle"
    DATA = "data"
    OTHER = "other"


@dataclass(frozen=True, slots=True)
class Rational:
    numerator: int
    denominator: int

    def __post_init__(self) -> None:
        if self.denominator == 0:
            raise ValueError("denominator cannot be zero")

    @property
    def fraction(self) -> Fraction:
        return Fraction(self.numerator, self.denominator)


@dataclass(frozen=True, slots=True)
class MediaStream:
    index: int
    kind: StreamKind
    codec_name: str | None = None
    codec_long_name: str | None = None
    width: int | None = None
    height: int | None = None
    pixel_format: str | None = None
    sample_rate: int | None = None
    channels: int | None = None
    channel_layout: str | None = None
    frame_rate: Rational | None = None
    time_base: Rational | None = None
    duration: TimePoint | None = None
    bitrate: int | None = None
    language: str | None = None
    rotation_degrees: int | None = None
    color_primaries: str | None = None
    color_transfer: str | None = None
    color_space: str | None = None
    disposition: dict[str, bool] = field(default_factory=dict)
    tags: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class SourceAsset:
    id: str
    project_id: str
    kind: AssetKind
    original_filename: str
    storage_key: str
    checksum_sha256: str
    byte_size: int
    container: str | None
    duration: TimePoint | None
    streams: tuple[MediaStream, ...]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.byte_size < 0:
            raise ValueError("byte_size cannot be negative")
        if len(self.checksum_sha256) != 64:
            raise ValueError("checksum_sha256 must be a 64-character hex digest")
