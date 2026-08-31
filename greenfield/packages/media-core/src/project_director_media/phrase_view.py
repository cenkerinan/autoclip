from __future__ import annotations

from dataclasses import dataclass

from .timecode import TimePoint, TimeRange
from .transcript import Transcript, TranscriptEvent, TranscriptWord


@dataclass(frozen=True, slots=True)
class Phrase:
    range: TimeRange
    text: str
    speaker_id: str | None
    word_ids: tuple[str, ...]
    event_ids: tuple[str, ...] = ()


def _gap_seconds(previous_end: TimePoint, next_start: TimePoint) -> float:
    return float(next_start.fraction - previous_end.fraction)


def build_phrase_view(
    transcript: Transcript,
    *,
    silence_threshold_seconds: float = 0.5,
    include_events: bool = True,
) -> tuple[Phrase, ...]:
    """Build a compact semantic transcript view without losing evidence links.

    Phrases split on meaningful silence or speaker change. The canonical
    transcript remains word-level; this representation is derived and disposable.
    """

    if silence_threshold_seconds < 0:
        raise ValueError("silence_threshold_seconds must be >= 0")

    words = sorted(transcript.words, key=lambda w: w.range.start.fraction)
    events = sorted(transcript.events, key=lambda e: e.range.start.fraction)

    phrases: list[Phrase] = []
    current: list[TranscriptWord] = []

    def flush() -> None:
        nonlocal current
        if not current:
            return
        start = current[0].range.start
        end = current[-1].range.end
        speaker = current[0].speaker_id
        phrase_events: list[TranscriptEvent] = []
        if include_events:
            phrase_range = TimeRange(start, end)
            phrase_events.extend(e for e in events if e.range.intersects(phrase_range))
        pieces = [w.text.strip() for w in current if w.text.strip()]
        if include_events:
            pieces.extend(f"({e.label})" for e in phrase_events)
        phrases.append(
            Phrase(
                range=TimeRange(start, end),
                text=" ".join(pieces),
                speaker_id=speaker,
                word_ids=tuple(w.id for w in current),
                event_ids=tuple(e.id for e in phrase_events),
            )
        )
        current = []

    for word in words:
        if current:
            previous = current[-1]
            speaker_changed = (
                previous.speaker_id is not None
                and word.speaker_id is not None
                and previous.speaker_id != word.speaker_id
            )
            long_gap = _gap_seconds(previous.range.end, word.range.start) >= silence_threshold_seconds
            if speaker_changed or long_gap:
                flush()
        current.append(word)

    flush()
    return tuple(phrases)
