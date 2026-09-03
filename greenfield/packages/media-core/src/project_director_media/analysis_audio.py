from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class AnalysisAudioPlan:
    source_uri: str
    output_uri: str
    sample_rate: int = 16_000
    channels: int = 1
    codec: str = "pcm_s16le"
    loudness_normalize: bool = False

    def __post_init__(self) -> None:
        if self.sample_rate <= 0:
            raise ValueError("sample_rate must be > 0")
        if self.channels <= 0:
            raise ValueError("channels must be > 0")


def build_analysis_audio_ffmpeg_args(
    *,
    input_path: str | Path,
    output_path: str | Path,
    sample_rate: int = 16_000,
    channels: int = 1,
) -> list[str]:
    """Return a fixed ffmpeg command template for transcription audio extraction."""
    if sample_rate <= 0 or channels <= 0:
        raise ValueError("sample_rate and channels must be > 0")
    return [
        "ffmpeg",
        "-y",
        "-i",
        str(input_path),
        "-vn",
        "-ac",
        str(channels),
        "-ar",
        str(sample_rate),
        "-c:a",
        "pcm_s16le",
        str(output_path),
    ]
