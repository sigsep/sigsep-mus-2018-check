from pathlib import Path as P
import pytest
import musdb
import soundfile as sf
import numpy as np
import sox
mus = musdb.DB()

tracks = mus.load_mus_tracks(subsets='test')
submissions_dir = '/Volumes/Samsung_T5/sisec/'


def submissions():
    p = P(submissions_dir)
    for submission_dir in p.iterdir():
        if submission_dir.is_dir():
            yield submission_dir, get_tracks(submission_dir)


def get_tracks(x):
    p = P(x)
    if p.exists():
        for sub_path in p.glob('test/*'):
            if sub_path.is_dir():
                yield sub_path


def get_audio(x):
    p = P(x)
    if p.exists():
        for sub_path in p.glob('*.wav'):
            yield sub_path


def check_equal(L1, L2):
    return len(L1) == len(L2) and sorted(L1) == sorted(L2)


@pytest.fixture(
    params=[(k, v) for k, l in submissions() for v in l],
    ids=['%s-%s' % (k.stem, v.stem) for k, l in submissions() for v in l]
)
def submission_tracks(request):
    return request.param


@pytest.fixture(
    params=submissions(),
    ids=['%s' % k.stem for k, l in submissions()]
)
def submission(request):
    return request.param[0]


@pytest.fixture
def track(submission_tracks):
    return submission_tracks[1]


def test_submission(submission):
    submission_tracks = list(get_tracks(submission))
    assert len(list(submission_tracks)) == len(tracks)
    assert check_equal(
        sorted([track.name for track in submission_tracks]),
        sorted([track.name for track in tracks])
    )

    for track_path in submission_tracks:
        for audio_path in get_audio(track_path):
            info = sox.file_info.info(str(audio_path.absolute()))
            assert(info['bitrate'] == 16)
            assert(info['channels'] == 2)
            assert(info['sample_rate'] == 44100)
