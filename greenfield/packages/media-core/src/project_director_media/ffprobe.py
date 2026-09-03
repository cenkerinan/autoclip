from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from .media_asset import MediaStream, Rational, StreamKind
from .timecode import TimePoint


class FFprobeError(RuntimeError):
    pass


@dataclass(frozen=True, slots=True)
class ProbeResult:
    container: str | None
    duration: TimePoint | None
    bitrate: int | None
    streams: tuple[MediaStream, ...]
    raw_format_tags: dict[str, str]


def _parse_rational(value: str | None) -> Rational | None:
    if not value or value in {"0/0", "N/A"}:
        return None
    try:
        n, d = value.split("/", 1)
        return Rational(int(n), int(d))
    except Exception:
        return None


def _parse_int(value: Any) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _duration_to_timepoint(value: Any, *, timebase: int = 1_000_000) -> TimePoint | None:
    if value in {None, "N/A"}:
        return None
    try:
        fraction = Fraction(str(value))
    except Exception:
        return None
    scaled = fraction * timebase
    ticks = int(round(float(scaled)))
    return TimePoint(ticks=ticks, timebase=timebase)


def _stream_kind(codec_type: str | None) -> StreamKind:
    mapping = {
        "video": StreamKind.VIDEO,
        "audio": StreamKind.AUDIO,
        "subtitle": StreamKind.SUBTITLE,
        "data": StreamKind.DATA,
    }
    return mapping.get(codec_type or "", StreamKind.OTHER)


def normalize_ffprobe(payload: dict[str, Any]) -> ProbeResult:
    format_info = payload.get("format") or {}
    streams: list[MediaStream] = []

    for stream in payload.get("streams") or []:
        tags = {str(k): str(v) for k, v in (stream.get("tags") or {}).items()}
        disposition = {
            str(k): bool(v) for k, v in (stream.get("disposition") or {}).items()
        }

        rotation: int | None = None
        side_data = stream.get("side_data_list") or []
        for item in side_data:
            if "rotation" in item:
                rotation = _parse_int(item.get("rotation"))
                break
        if rotation is None:
            rotation = _parse_int(tags.get("rotate"))

        duration = _duration_to_timepoint(stream.get("duration"))
        if duration is None:
            tb = _parse_rational(stream.get("time_base"))
            duration_ts = _parse_int(stream.get("duration_ts"))
            if tb and duration_ts is not None:
                seconds = Fraction(duration_ts * tb.numerator, tb.denominator)
                scaled = seconds * 1_000_000
                duration = TimePoint(int(round(float(scaled))), 1_000_000)

        streams.append(
            MediaStream(
                index=int(stream.get("index", len(streams))),
                kind=_stream_kind(stream.get("codec_type")),
                codec_name=stream.get("codec_name"),
                codec_long_name=stream.get("codec_long_name"),
                width=_parse_int(stream.get("width")),
                height=_parse_int(stream.get("height")),
                pixel_format=stream.get("pix_fmt"),
                sample_rate=_parse_int(stream.get("sample_rate")),
                channels=_parse_int(stream.get("channels")),
                channel_layout=stream.get("channel_layout"),
                frame_rate=_parse_rational(stream.get("avg_frame_rate") or stream.get("r_frame_rate")),
                time_base=_parse_rational(stream.get("time_base")),
                duration=duration,
                bitrate=_parse_int(stream.get("bit_rate")),
                language=tags.get("language"),
                rotation_degrees=rotation,
                color_primaries=stream.get("color_primaries"),
                color_transfer=stream.get("color_transfer"),
                color_space=stream.get("color_space"),
                disposition=disposition,
                tags=tags,
            )
        )

    return ProbeResult(
        container=format_info.get("format_name"),
        duration=_duration_to_timepoint(format_info.get("duration")),
        bitrate=_parse_int(format_info.get("bit_rate")),
        streams=tuple(streams),
        raw_format_tags={
            str(k): str(v) for k, v in (format_info.get("tags") or {}).items()
        },
    )


def probe_media(path: str | Path, *, timeout_seconds: int = 30) -> ProbeResult:
    """Run ffprobe with a fixed, validated command template."""
    if timeout_seconds <= 0:
        raise ValueError("timeout_seconds must be > 0")

    media_path = Path(path)
    if not media_path.exists():
        raise FileNotFoundError(media_path)

    cmd = [
        "ffprobe",
        "-v", "error",
        "-show_streams",
        "-show_format",
        "-show_entries",
        "stream=index,codec_type,codec_name,codec_long_name,width,height,pix_fmt,"
        "sample_rate,channels,channel_layout,avg_frame_rate,r_frame_rate,time_base,"
        "duration,duration_ts,bit_rate,color_primaries,color_transfer,color_space,"
        "tags,disposition,side_data_list:"
        "format=format_name,duration,bit_rate,tags",
        "-of", "json",
        str(media_path),
    ]

    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise FFprobeError(f"ffprobe timed out after {timeout_seconds}s") from exc

    if proc.returncode != 0:
        raise FFprobeError(proc.stderr.strip()[:1000] or "ffprobe failed")

    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise FFprobeError("ffprobe returned invalid JSON") from exc

    return normalize_ffprobe(payload)
