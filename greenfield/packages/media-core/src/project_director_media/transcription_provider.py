from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from .transcript import Transcript


@dataclass(frozen=True, slots=True)
class TranscriptionOptions:
    language: str | None = None
    diarize: bool = True
    tag_audio_events: bool = True
    known_speakers: int | None = None
    verbatim: bool = True


@dataclass(frozen=True, slots=True)
class TranscriptionRequest:
    source_asset_id: str
    analysis_audio_uri: str
    asset_checksum: str
    options: TranscriptionOptions


class TranscriptionProvider(Protocol):
    name: str
    model: str

    def transcribe(self, request: TranscriptionRequest) -> Transcript:
        """Return provider-neutral canonical Transcript."""
        ...


@dataclass(frozen=True, slots=True)
class ProviderCapability:
    word_timestamps: bool
    diarization: bool
    audio_events: bool
    multilingual: bool


class TranscriptionProviderRegistry:
    def __init__(self) -> None:
        self._providers: dict[str, TranscriptionProvider] = {}

    def register(self, provider: TranscriptionProvider) -> None:
        if provider.name in self._providers:
            raise ValueError(f"provider already registered: {provider.name}")
        self._providers[provider.name] = provider

    def get(self, name: str) -> TranscriptionProvider:
        try:
            return self._providers[name]
        except KeyError as exc:
            raise KeyError(f"unknown transcription provider: {name}") from exc

    def names(self) -> tuple[str, ...]:
        return tuple(sorted(self._providers))
