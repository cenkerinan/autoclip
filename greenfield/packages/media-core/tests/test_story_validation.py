from project_director_media import TimePoint, TimeRange
from project_director_media.intelligence_graph import EvidenceRef, IntelligenceNode, IntelligenceNodeType, MediaIntelligenceGraph
from project_director_media.production_brief import Platform, ProductionBrief, ProductionMode
from project_director_media.story import StoryBeat, StoryBeatKind, StoryProposal, StoryScore
from project_director_media.story_validation import validate_story_proposal


def ev():
    return (EvidenceRef("a", TimeRange(TimePoint(0,1), TimePoint(1,1))),)


def test_validation_rejects_missing_payoff():
    brief = ProductionBrief("b","p",ProductionMode.CREATOR_STUDIO,"retention","food fans",Platform.YOUTUBE)
    graph = MediaIntelligenceGraph("p","1",(
        IntelligenceNode("h","p",IntelligenceNodeType.HOOK,"hook",evidence=ev()),
    ),())
    proposal = StoryProposal("s","p","Title","Premise","Promise",(
        StoryBeat("b1",StoryBeatKind.HOOK,"hook",ev(),("h",)),
    ),StoryScore(.8,.8,.8,.8,.8,.8))
    report = validate_story_proposal(proposal, brief=brief, graph=graph)
    assert not report.valid
    assert "missing_payoff" in {i.code for i in report.issues}


def test_validation_accepts_grounded_hook_and_payoff():
    brief = ProductionBrief("b","p",ProductionMode.CREATOR_STUDIO,"retention","food fans",Platform.YOUTUBE)
    graph = MediaIntelligenceGraph("p","1",(
        IntelligenceNode("h","p",IntelligenceNodeType.HOOK,"hook",evidence=ev()),
        IntelligenceNode("p1","p",IntelligenceNodeType.PAYOFF,"verdict",evidence=ev()),
    ),())
    proposal = StoryProposal("s","p","Title","Premise","Promise",(
        StoryBeat("b1",StoryBeatKind.HOOK,"hook",ev(),("h",)),
        StoryBeat("b2",StoryBeatKind.PAYOFF,"payoff",ev(),("p1",)),
    ),StoryScore(.8,.8,.8,.8,.8,.8))
    assert validate_story_proposal(proposal, brief=brief, graph=graph).valid
