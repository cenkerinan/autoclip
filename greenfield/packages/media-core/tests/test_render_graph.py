import pytest

from project_director_media import (
    RenderGraph,
    RenderOperation,
    RenderOperationKind,
    RenderProfile,
    TimePoint,
    TimeRange,
)


def r(a: int, b: int) -> TimeRange:
    return TimeRange(TimePoint(a, 1000), TimePoint(b, 1000))


PROFILE = RenderProfile(
    name="preview",
    width=1920,
    height=1080,
    video_codec="h264",
    audio_codec="aac",
)


def test_source_clip_requires_matching_duration() -> None:
    with pytest.raises(ValueError):
        RenderOperation(
            id="clip",
            kind=RenderOperationKind.SOURCE_CLIP,
            timeline_range=r(0, 1000),
            source_asset_id="asset",
            source_range=r(0, 900),
        )


def test_captions_must_remain_after_visual_compositing() -> None:
    graph = RenderGraph(
        schema_version="1",
        project_id="p",
        timeline_id="t",
        profile=PROFILE,
        operations=(
            RenderOperation("caption", RenderOperationKind.CAPTION_LAYER, r(0, 1000)),
            RenderOperation("overlay", RenderOperationKind.OVERLAY, r(0, 1000)),
        ),
    )
    with pytest.raises(ValueError):
        graph.validate()


def test_valid_graph_passes() -> None:
    graph = RenderGraph(
        schema_version="1",
        project_id="p",
        timeline_id="t",
        profile=PROFILE,
        operations=(
            RenderOperation(
                "clip",
                RenderOperationKind.SOURCE_CLIP,
                r(0, 1000),
                source_asset_id="asset",
                source_range=r(2000, 3000),
            ),
            RenderOperation("overlay", RenderOperationKind.OVERLAY, r(100, 400)),
            RenderOperation("caption", RenderOperationKind.CAPTION_LAYER, r(0, 1000)),
        ),
    )
    graph.validate()
