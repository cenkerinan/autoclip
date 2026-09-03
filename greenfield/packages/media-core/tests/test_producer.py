from project_director_media.intelligence_graph import EvidenceRef, IntelligenceNode, IntelligenceNodeType, MediaIntelligenceGraph
from project_director_media.production_brief import Platform, ProductionBrief, ProductionMode
from project_director_media.producer import build_producer_evidence_pack, generate_story_proposals
from project_director_media.story import StoryBeat, StoryBeatKind, StoryProposal, StoryScore
from project_director_media import TimePoint, TimeRange


def ev():
    return (EvidenceRef("a", TimeRange(TimePoint(0, 1), TimePoint(1, 1))),)


def brief():
    return ProductionBrief("b", "p", ProductionMode.CREATOR_STUDIO, "Maximise retention", "UK food lovers", Platform.YOUTUBE, 900)


class FakeGenerator:
    def generate(self, *, brief, graph, evidence_pack, count):
        beat1 = StoryBeat("hook", StoryBeatKind.HOOK, "Create curiosity", ev(), evidence_pack.hook_node_ids)
        beat2 = StoryBeat("pay", StoryBeatKind.PAYOFF, "Resolve curiosity", ev())
        return (StoryProposal("s", "p", "Is it worth it?", "Test the hype", "A clear verdict", (beat1, beat2), StoryScore(.9,.9,.8,.7,.8,.9)),)


def test_evidence_pack_prefers_high_confidence_nodes():
    graph = MediaIntelligenceGraph("p", "1", (
        IntelligenceNode("h1","p",IntelligenceNodeType.HOOK,"low",confidence=.2,evidence=ev()),
        IntelligenceNode("h2","p",IntelligenceNodeType.HOOK,"high",confidence=.9,evidence=ev()),
    ), ())
    pack = build_producer_evidence_pack(brief(), graph)
    assert pack.hook_node_ids == ("h2", "h1")


def test_generate_story_proposals_through_contract():
    graph = MediaIntelligenceGraph("p", "1", (
        IntelligenceNode("h","p",IntelligenceNodeType.HOOK,"hook",confidence=.9,evidence=ev()),
    ), ())
    result = generate_story_proposals(brief=brief(), graph=graph, generator=FakeGenerator(), count=3)
    assert result.proposals[0].title == "Is it worth it?"
