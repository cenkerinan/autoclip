import pytest

from project_director_media.intelligence_graph import (
    EvidenceRef,
    IntelligenceEdge,
    IntelligenceEdgeType,
    IntelligenceNode,
    IntelligenceNodeType,
    MediaIntelligenceGraph,
)
from project_director_media import TimePoint, TimeRange


def tr(a: int, b: int) -> TimeRange:
    return TimeRange(TimePoint(a, 1000), TimePoint(b, 1000))


def evidence(a: int, b: int) -> tuple[EvidenceRef, ...]:
    return (EvidenceRef(asset_id="asset1", range=tr(a, b)),)


def test_graph_validates_edges_and_temporal_query() -> None:
    hook = IntelligenceNode(
        id="hook1", project_id="p", type=IntelligenceNodeType.HOOK,
        label="Unexpected price", range=tr(0, 1000), confidence=.9, evidence=evidence(0, 1000)
    )
    reaction = IntelligenceNode(
        id="r1", project_id="p", type=IntelligenceNodeType.REACTION,
        label="Presenter surprised", range=tr(800, 1400), confidence=.8, evidence=evidence(800, 1400)
    )
    edge = IntelligenceEdge(
        id="e1", project_id="p", type=IntelligenceEdgeType.RESPONDS_TO,
        from_node_id="r1", to_node_id="hook1"
    )
    graph = MediaIntelligenceGraph("p", "1", (hook, reaction), (edge,))
    graph.validate()
    assert {n.id for n in graph.temporal_nodes(tr(900, 1100))} == {"hook1", "r1"}
    assert graph.neighbors("hook1")[0].id == "r1"


def test_non_entity_nodes_require_evidence() -> None:
    with pytest.raises(ValueError):
        IntelligenceNode(
            id="x", project_id="p", type=IntelligenceNodeType.HOOK, label="hook"
        )


def test_graph_rejects_dangling_edges() -> None:
    node = IntelligenceNode(
        id="n1", project_id="p", type=IntelligenceNodeType.TOPIC, label="food"
    )
    edge = IntelligenceEdge(
        id="e", project_id="p", type=IntelligenceEdgeType.SUPPORTS,
        from_node_id="n1", to_node_id="missing"
    )
    graph = MediaIntelligenceGraph("p", "1", (node,), (edge,))
    with pytest.raises(ValueError):
        graph.validate()
