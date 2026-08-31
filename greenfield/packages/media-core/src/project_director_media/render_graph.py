from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .timecode import TimeRange


class RenderOperationKind(StrEnum):
    SOURCE_CLIP = "source_clip"
    AUDIO_EDGE_FADE = "audio_edge_fade"
    AUDIO_GAIN = "audio_gain"
    LOUDNESS_NORMALIZE = "loudness_normalize"
    OVERLAY = "overlay"
    CAPTION_LAYER = "caption_layer"
    TRANSFORM = "transform"
    COLOR_CORRECTION = "color_correction"


@dataclass(frozen=True, slots=True)
class RenderProfile:
    name: str
    width: int
    height: int
    video_codec: str
    audio_codec: str
    target_lufs: float | None = None
    max_true_peak_db: float | None = None

    def __post_init__(self) -> None:
        if self.width <= 0 or self.height <= 0:
            raise ValueError("render dimensions must be > 0")


@dataclass(frozen=True, slots=True)
class RenderOperation:
    id: str
    kind: RenderOperationKind
    timeline_range: TimeRange
    source_asset_id: str | None = None
    source_range: TimeRange | None = None
    params: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.kind == RenderOperationKind.SOURCE_CLIP:
            if not self.source_asset_id or self.source_range is None:
                raise ValueError("source_clip requires source_asset_id and source_range")
            if self.timeline_range.duration != self.source_range.duration:
                raise ValueError("source clip source/timeline duration mismatch")


@dataclass(frozen=True, slots=True)
class RenderGraph:
    schema_version: str
    project_id: str
    timeline_id: str
    profile: RenderProfile
    operations: tuple[RenderOperation, ...]

    def validate(self) -> None:
        ids: set[str] = set()
        captions_seen = False
        for op in self.operations:
            if op.id in ids:
                raise ValueError(f"duplicate render operation id: {op.id}")
            ids.add(op.id)

            if op.kind == RenderOperationKind.CAPTION_LAYER:
                captions_seen = True
            elif captions_seen and op.kind in {
                RenderOperationKind.OVERLAY,
                RenderOperationKind.TRANSFORM,
                RenderOperationKind.COLOR_CORRECTION,
            }:
                raise ValueError(
                    "visual compositing operations cannot appear after caption_layer; "
                    "captions must remain top-most unless explicitly modeled otherwise"
                )

    def ordered_operations(self) -> tuple[RenderOperation, ...]:
        self.validate()
        return self.operations
