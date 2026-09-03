from project_director_media import build_waveform_pyramid


def test_waveform_pyramid_builds_multiple_resolutions() -> None:
    samples = [0.0, 0.5, -1.0, 0.25, 0.75, -0.2, 0.1, 0.0]
    pyramid = build_waveform_pyramid(
        samples, sample_rate=16000, base_bucket_size=2, levels=3
    )
    assert len(pyramid.levels) == 3
    assert pyramid.levels[0].samples_per_bucket == 2
    assert pyramid.levels[0].peaks == (0.5, 1.0, 0.75, 0.1)
    assert pyramid.levels[1].samples_per_bucket == 4
    assert pyramid.levels[1].peaks == (1.0, 0.75)
    assert pyramid.levels[2].peaks == (1.0,)
