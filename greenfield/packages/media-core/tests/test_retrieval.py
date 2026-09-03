from project_director_media.intelligence_graph import (
    EvidenceRef, IntelligenceNode, IntelligenceNodeType, MediaIntelligenceGraph
)
from project_director_media.retrieval import IntelligenceQuery, query_graph
from project_director_media import TimePoint, TimeRange


def ev() -> tuple[EvidenceRef, ...]:
    return (EvidenceRef("a", TimeRange(TimePoint(0, 1), TimePoint(1, 1))),)


def test_query_graph_filters_and_ranks_confidence() -> None:
    nodes = (
        IntelligenceNode("1", "p", IntelligenceNodeType.HOOK, "Secret sauce", confidence=.7, evidence=ev()),
        IntelligenceNode("2", "p", IntelligenceNodeType.HOOK, "Secret recipe revealed", confidence=.95, evidence=ev()),
        IntelligenceNode("3", "p", IntelligenceNodeType.REACTION, "Laugh", confidence=.99, evidence=ev()),
    )
    graph = MediaIntelligenceGraph("p", "1", nodes, ())
    result = query_graph(
        graph,
        IntelligenceQuery(
            node_types=(IntelligenceNodeType.HOOK,),
            text_contains="secret",
            min_confidence=.5,
        ),
    )
    assert [n.id for n in result] == ["2", "1"]
