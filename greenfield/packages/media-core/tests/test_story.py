import pytest

from project_director_media import TimePoint, TimeRange
from project_director_media.intelligence_graph import EvidenceRef
from project_director_media.story import StoryBeat, StoryBeatKind, StoryProposal, StoryScore


def test_story_proposal_is_evidence_grounded() -> None:
    evidence = (EvidenceRef("a", TimeRange(TimePoint(0, 1), TimePoint(2, 1))),)
    beat = StoryBeat("b1", StoryBeatKind.HOOK, "Create curiosity", evidence)
    score = StoryScore(.9, .8, .7, .8, .9, .8)
    proposal = StoryProposal("s1", "p", "Secret sauce", "Find out why it matters", "A satisfying reveal", (beat,), score)
    assert proposal.beats[0].kind == StoryBeatKind.HOOK


def test_story_scores_are_bounded() -> None:
    with pytest.raises(ValueError):
        StoryScore(1.1, .8, .7, .8, .9, .8)
