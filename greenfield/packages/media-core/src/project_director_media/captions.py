from __future__ import annotations

from dataclasses import dataclass

from .timecode import TimePoint, TimeRange
from .transcript import TranscriptWord


@dataclass(frozen=True, slots=True)
class CaptionCue:
    id: str
    range: TimeRange
    text: str
    source_word_ids: tuple[str, ...]


def _offset_point(point: TimePoint, delta_seconds) -> TimePoint:
    value = point.fraction + delta_seconds
    return TimePoint(value.numerator, value.denominator)


def remap_words_to_timeline(
    *,
    words: tuple[TranscriptWord, ...],
    source_range: TimeRange,
    timeline_start: TimePoint,
) -> tuple[TranscriptWord, ...]:
    """Map source transcript words into output timeline coordinates.

    Only words that overlap the source selection are returned. Word boundaries are
    clipped to the selected source range before the source->timeline offset is applied.
    """
    offset = timeline_start.fraction - source_range.start.fraction
    out: list[TranscriptWord] = []
    for word in words:
        intersection = word.range.intersection(source_range)
        if intersection is None or intersection.is_empty:
            continue
        out.append(
            TranscriptWord(
                id=word.id,
                text=word.text,
                range=TimeRange(
                    _offset_point(intersection.start, offset),
                    _offset_point(intersection.end, offset),
                ),
                confidence=word.confidence,
                speaker_id=word.speaker_id,
            )
        )
    return tuple(out)


def build_caption_cues(
    words: tuple[TranscriptWord, ...],
    *,
    max_words: int = 4,
    max_gap_seconds: float = 0.45,
) -> tuple[CaptionCue, ...]:
    if max_words <= 0:
        raise ValueError("max_words must be > 0")
    if max_gap_seconds < 0:
        raise ValueError("max_gap_seconds must be >= 0")

    ordered = sorted(words, key=lambda w: w.range.start.fraction)
    groups: list[list[TranscriptWord]] = []
    current: list[TranscriptWord] = []

    for word in ordered:
        if current:
            gap = float(word.range.start.fraction - current[-1].range.end.fraction)
            punctuation_break = current[-1].text.rstrip().endswith((".", "!", "?"))
            if len(current) >= max_words or gap > max_gap_seconds or punctuation_break:
                groups.append(current)
                current = []
        current.append(word)
    if current:
        groups.append(current)

    cues: list[CaptionCue] = []
    for index, group in enumerate(groups):
        text = " ".join(w.text.strip() for w in group if w.text.strip())
        cues.append(
            CaptionCue(
                id=f"cue-{index:06d}",
                range=TimeRange(group[0].range.start, group[-1].range.end),
                text=text,
                source_word_ids=tuple(w.id for w in group),
            )
        )
    return tuple(cues)
