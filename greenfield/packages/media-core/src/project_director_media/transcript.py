from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .timecode import TimeRange


class TranscriptEventType(StrEnum):
    LAUGHTER = "laughter"
    APPLAUSE = "applause"
    SIGH = "sigh"
    MUSIC = "music"
    OTHER = "other"


@dataclass(frozen=True, slots=True)
class TranscriptWord:
    id: str
    text: str
    range: TimeRange
    confidence: float | None = None
    speaker_id: str | None = None

    def __post_init__(self) -> None:
        if not self.text:
            raise ValueError("word text cannot be empty")
        if self.confidence is not None and not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")


@dataclass(frozen=True, slots=True)
class TranscriptEvent:
    id: str
    type: TranscriptEventType
    range: TimeRange
    label: str
    confidence: float | None = None


@dataclass(frozen=True, slots=True)
class Transcript:
    id: str
    source_asset_id: str
    language: str | None
    provider: str
    model: str
    provider_version: str | None = None
    words: tuple[TranscriptWord, ...] = field(default_factory=tuple)
    events: tuple[TranscriptEvent, ...] = field(default_factory=tuple)


def transcription_cache_key(
    *,
    asset_checksum: str,
    provider: str,
    model: str,
    settings: dict[str, Any],
    schema_version: str = "1",
) -> str:
    """Return a deterministic cache key for transcription output.

    A filename is deliberately not part of this key. If media bytes, provider,
    model, schema, or relevant settings change, the key changes.
    """

    payload = {
        "asset_checksum": asset_checksum,
        "provider": provider,
        "model": model,
        "schema_version": schema_version,
        "settings": settings,
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()
