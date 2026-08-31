from project_director_media import (
    TimePoint,
    TimeRange,
    Transcript,
    TranscriptWord,
    build_phrase_view,
    transcription_cache_key,
)


def r(a: int, b: int) -> TimeRange:
    return TimeRange(TimePoint(a, 1000), TimePoint(b, 1000))


def test_cache_key_changes_when_settings_change() -> None:
    base = dict(asset_checksum="abc", provider="scribe", model="v1")
    a = transcription_cache_key(**base, settings={"language": "en"})
    b = transcription_cache_key(**base, settings={"language": "tr"})
    assert a != b


def test_cache_key_is_order_independent_for_settings() -> None:
    base = dict(asset_checksum="abc", provider="scribe", model="v1")
    a = transcription_cache_key(**base, settings={"language": "en", "diarize": True})
    b = transcription_cache_key(**base, settings={"diarize": True, "language": "en"})
    assert a == b


def test_phrase_view_splits_on_silence_and_speaker() -> None:
    transcript = Transcript(
        id="tr1",
        source_asset_id="asset1",
        language="en",
        provider="test",
        model="test",
        words=(
            TranscriptWord("w1", "Hello", r(0, 200), speaker_id="a"),
            TranscriptWord("w2", "there", r(250, 450), speaker_id="a"),
            TranscriptWord("w3", "New", r(1100, 1250), speaker_id="a"),
            TranscriptWord("w4", "speaker", r(1300, 1500), speaker_id="b"),
        ),
    )
    phrases = build_phrase_view(transcript, silence_threshold_seconds=0.5)
    assert [p.text for p in phrases] == ["Hello there", "New", "speaker"]
    assert phrases[0].word_ids == ("w1", "w2")
