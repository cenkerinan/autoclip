from __future__ import annotations

from dataclasses import dataclass

from .render_graph import RenderGraph, RenderOperation, RenderOperationKind
from .timecode import TimePoint, TimeRange


@dataclass(frozen=True, slots=True)
class AudioEdgePolicy:
    fade_in_ms: int = 8
    fade_out_ms: int = 12

    def __post_init__(self) -> None:
        if self.fade_in_ms < 0 or self.fade_out_ms < 0:
            raise ValueError("fade durations cannot be negative")


def _point(seconds) -> TimePoint:
    return TimePoint(seconds.numerator, seconds.denominator)


def add_audio_edge_fades(graph: RenderGraph, *, policy: AudioEdgePolicy = AudioEdgePolicy()) -> RenderGraph:
    """Add short click-prevention fades around source-clip edit boundaries."""
    operations: list[RenderOperation] = []
    for op in graph.operations:
        operations.append(op)
        if op.kind != RenderOperationKind.SOURCE_CLIP:
            continue
        duration = op.timeline_range.duration
        if duration <= 0:
            continue
        fade_in = min(duration / 2, policy.fade_in_ms / 1000)
        fade_out = min(duration / 2, policy.fade_out_ms / 1000)
        if fade_in > 0:
            operations.append(RenderOperation(
                id=f"{op.id}-audio-in",
                kind=RenderOperationKind.AUDIO_EDGE_FADE,
                timeline_range=TimeRange(op.timeline_range.start, _point(op.timeline_range.start.fraction + fade_in)),
                source_asset_id=op.source_asset_id,
                params={"direction":"in","duration_seconds":float(fade_in)},
            ))
        if fade_out > 0:
            operations.append(RenderOperation(
                id=f"{op.id}-audio-out",
                kind=RenderOperationKind.AUDIO_EDGE_FADE,
                timeline_range=TimeRange(_point(op.timeline_range.end.fraction - fade_out), op.timeline_range.end),
                source_asset_id=op.source_asset_id,
                params={"direction":"out","duration_seconds":float(fade_out)},
            ))
    result = RenderGraph(graph.schema_version, graph.project_id, graph.timeline_id, graph.profile, tuple(operations))
    result.validate()
    return result
