from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from .media_asset import SourceAsset, StreamKind


class DerivedAssetKind(StrEnum):
    PROXY_VIDEO = "proxy_video"
    ANALYSIS_AUDIO = "analysis_audio"
    THUMBNAIL_SPRITE = "thumbnail_sprite"
    WAVEFORM = "waveform"


@dataclass(frozen=True, slots=True)
class ProxyVideoSpec:
    max_width: int = 1920
    max_height: int = 1080
    video_codec: str = "h264"
    audio_codec: str = "aac"
    target_video_bitrate: int = 6_000_000
    target_audio_bitrate: int = 160_000


@dataclass(frozen=True, slots=True)
class AnalysisAudioSpec:
    sample_rate: int = 16_000
    channels: int = 1
    codec: str = "pcm_s16le"


@dataclass(frozen=True, slots=True)
class ThumbnailSpec:
    width: int = 320
    interval_seconds: int = 5


@dataclass(frozen=True, slots=True)
class WaveformSpec:
    sample_rate: int = 100
    channels: int = 1


@dataclass(frozen=True, slots=True)
class DerivedAssetPlan:
    source_asset_id: str
    proxy: ProxyVideoSpec | None
    analysis_audio: AnalysisAudioSpec | None
    thumbnails: ThumbnailSpec | None
    waveform: WaveformSpec | None


def plan_derived_assets(asset: SourceAsset) -> DerivedAssetPlan:
    has_video = any(s.kind == StreamKind.VIDEO for s in asset.streams)
    has_audio = any(s.kind == StreamKind.AUDIO for s in asset.streams)

    return DerivedAssetPlan(
        source_asset_id=asset.id,
        proxy=ProxyVideoSpec() if has_video else None,
        analysis_audio=AnalysisAudioSpec() if has_audio else None,
        thumbnails=ThumbnailSpec() if has_video else None,
        waveform=WaveformSpec() if has_audio else None,
    )
