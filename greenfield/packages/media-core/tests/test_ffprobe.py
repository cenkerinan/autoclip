from project_director_media import StreamKind, normalize_ffprobe


def test_normalize_ffprobe_video_audio_and_rotation() -> None:
    payload = {
        "streams": [
            {
                "index": 0,
                "codec_type": "video",
                "codec_name": "h264",
                "width": 1920,
                "height": 1080,
                "avg_frame_rate": "30000/1001",
                "time_base": "1/90000",
                "duration_ts": "900000",
                "pix_fmt": "yuv420p",
                "color_primaries": "bt709",
                "side_data_list": [{"rotation": -90}],
                "tags": {"language": "und"},
            },
            {
                "index": 1,
                "codec_type": "audio",
                "codec_name": "aac",
                "sample_rate": "48000",
                "channels": 2,
                "channel_layout": "stereo",
                "duration": "10.0",
                "tags": {"language": "eng"},
            },
        ],
        "format": {
            "format_name": "mov,mp4,m4a,3gp,3g2,mj2",
            "duration": "10.010",
            "bit_rate": "5000000",
        },
    }

    result = normalize_ffprobe(payload)
    assert result.duration is not None
    assert result.duration.ticks == 10_010_000
    assert len(result.streams) == 2
    video, audio = result.streams
    assert video.kind == StreamKind.VIDEO
    assert video.frame_rate.numerator == 30000
    assert video.frame_rate.denominator == 1001
    assert video.rotation_degrees == -90
    assert audio.kind == StreamKind.AUDIO
    assert audio.sample_rate == 48000
    assert audio.language == "eng"
