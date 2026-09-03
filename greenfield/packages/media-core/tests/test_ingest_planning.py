import hashlib

from project_director_media import (
    AssetKind,
    MediaStream,
    SourceAsset,
    StreamKind,
    plan_derived_assets,
    sha256_file,
)


def asset(*streams: MediaStream) -> SourceAsset:
    return SourceAsset(
        id="a1",
        project_id="p1",
        kind=AssetKind.VIDEO,
        original_filename="take.mp4",
        storage_key="workspaces/w/projects/p/assets/a1/source",
        checksum_sha256="0" * 64,
        byte_size=100,
        container="mp4",
        duration=None,
        streams=streams,
    )


def test_sha256_file(tmp_path) -> None:
    p = tmp_path / "sample.bin"
    p.write_bytes(b"project-director")
    assert sha256_file(p) == hashlib.sha256(b"project-director").hexdigest()


def test_video_audio_asset_plans_all_analysis_derivatives() -> None:
    plan = plan_derived_assets(
        asset(
            MediaStream(index=0, kind=StreamKind.VIDEO),
            MediaStream(index=1, kind=StreamKind.AUDIO),
        )
    )
    assert plan.proxy is not None
    assert plan.analysis_audio is not None
    assert plan.thumbnails is not None
    assert plan.waveform is not None


def test_audio_only_asset_skips_video_derivatives() -> None:
    plan = plan_derived_assets(asset(MediaStream(index=0, kind=StreamKind.AUDIO)))
    assert plan.proxy is None
    assert plan.thumbnails is None
    assert plan.analysis_audio is not None
    assert plan.waveform is not None
