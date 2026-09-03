from project_director_media import build_analysis_audio_ffmpeg_args


def test_analysis_audio_command_is_fixed_and_mono_16k() -> None:
    args = build_analysis_audio_ffmpeg_args(input_path="input.mp4", output_path="analysis.wav")
    assert args == [
        "ffmpeg", "-y", "-i", "input.mp4", "-vn", "-ac", "1",
        "-ar", "16000", "-c:a", "pcm_s16le", "analysis.wav"
    ]
