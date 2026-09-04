from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

from .render_graph import RenderGraph, RenderOperationKind


class UnsupportedRenderGraphError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class FFmpegCommand:
    argv: tuple[str, ...]
    input_asset_ids: tuple[str, ...]


def _seconds(value) -> str:
    return f"{float(value):.6f}"


def build_rough_cut_ffmpeg_command(
    graph: RenderGraph,
    *,
    asset_paths: Mapping[str, str | Path],
    output_path: str | Path,
) -> FFmpegCommand:
    """Compile a simple source-clip rough cut into one deterministic ffmpeg command.

    This first executor deliberately rejects visual overlays/captions/transforms rather
    than silently rendering them incorrectly. Those operations will be compiled by
    dedicated stages as the renderer grows.
    """
    graph.validate()
    clips = [op for op in graph.operations if op.kind == RenderOperationKind.SOURCE_CLIP]
    unsupported = [op for op in graph.operations if op.kind in {
        RenderOperationKind.OVERLAY,
        RenderOperationKind.CAPTION_LAYER,
        RenderOperationKind.TRANSFORM,
        RenderOperationKind.COLOR_CORRECTION,
    }]
    if unsupported:
        raise UnsupportedRenderGraphError(
            "rough-cut executor cannot yet compile: " + ", ".join(sorted({op.kind.value for op in unsupported}))
        )
    if not clips:
        raise UnsupportedRenderGraphError("render graph has no source clips")

    input_ids: list[str] = []
    argv: list[str] = ["ffmpeg", "-y"]
    for op in clips:
        assert op.source_asset_id is not None and op.source_range is not None
        if op.source_asset_id not in asset_paths:
            raise KeyError(f"missing asset path: {op.source_asset_id}")
        input_ids.append(op.source_asset_id)
        argv += ["-i", str(asset_paths[op.source_asset_id])]

    filters: list[str] = []
    concat_inputs: list[str] = []
    for index, op in enumerate(clips):
        assert op.source_range is not None
        start = _seconds(op.source_range.start.fraction)
        end = _seconds(op.source_range.end.fraction)
        fade_in = float(next((x.params.get("duration_seconds", 0.0) for x in graph.operations if x.kind == RenderOperationKind.AUDIO_EDGE_FADE and x.source_asset_id == op.source_asset_id and x.params.get("direction") == "in" and x.timeline_range.start.equivalent(op.timeline_range.start)), 0.0))
        fade_out = float(next((x.params.get("duration_seconds", 0.0) for x in graph.operations if x.kind == RenderOperationKind.AUDIO_EDGE_FADE and x.source_asset_id == op.source_asset_id and x.params.get("direction") == "out" and x.timeline_range.end.equivalent(op.timeline_range.end)), 0.0))
        audio_chain = f"[{index}:a]atrim=start={start}:end={end},asetpts=PTS-STARTPTS"
        if fade_in > 0:
            audio_chain += f",afade=t=in:st=0:d={fade_in:.6f}"
        if fade_out > 0:
            fade_start = max(0.0, float(op.source_range.duration) - fade_out)
            audio_chain += f",afade=t=out:st={fade_start:.6f}:d={fade_out:.6f}"
        filters.append(f"[{index}:v]trim=start={start}:end={end},setpts=PTS-STARTPTS,scale={graph.profile.width}:{graph.profile.height}:force_original_aspect_ratio=decrease,pad={graph.profile.width}:{graph.profile.height}:(ow-iw)/2:(oh-ih)/2[v{index}]")
        filters.append(audio_chain + f"[a{index}]")
        concat_inputs.append(f"[v{index}][a{index}]")

    filters.append("".join(concat_inputs) + f"concat=n={len(clips)}:v=1:a=1[vout][aout]")
    argv += [
        "-filter_complex", ";".join(filters),
        "-map", "[vout]", "-map", "[aout]",
        "-c:v", graph.profile.video_codec,
        "-c:a", graph.profile.audio_codec,
        str(output_path),
    ]
    return FFmpegCommand(tuple(argv), tuple(input_ids))
