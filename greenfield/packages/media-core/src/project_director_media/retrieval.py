from __future__ import annotations

from dataclasses import dataclass

from .intelligence_graph import IntelligenceNode, IntelligenceNodeType, MediaIntelligenceGraph
from .timecode import TimeRange


@dataclass(frozen=True, slots=True)
class IntelligenceQuery:
    node_types: tuple[IntelligenceNodeType, ...] = ()
    temporal_range: TimeRange | None = None
    min_confidence: float | None = None
    text_contains: str | None = None
    limit: int = 50


def query_graph(
    graph: MediaIntelligenceGraph,
    query: IntelligenceQuery,
) -> tuple[IntelligenceNode, ...]:
    if query.limit <= 0:
        raise ValueError("limit must be > 0")
    if query.min_confidence is not None and not 0.0 <= query.min_confidence <= 1.0:
        raise ValueError("min_confidence must be between 0 and 1")

    nodes = graph.nodes
    if query.node_types:
        allowed = set(query.node_types)
        nodes = tuple(n for n in nodes if n.type in allowed)
    if query.temporal_range is not None:
        nodes = tuple(
            n for n in nodes
            if n.range is not None and n.range.intersects(query.temporal_range)
        )
    if query.min_confidence is not None:
        nodes = tuple(
            n for n in nodes
            if n.confidence is not None and n.confidence >= query.min_confidence
        )
    if query.text_contains:
        needle = query.text_contains.casefold()
        nodes = tuple(
            n for n in nodes
            if needle in n.label.casefold()
            or any(needle in str(v).casefold() for v in n.attributes.values())
        )

    ranked = sorted(
        nodes,
        key=lambda n: (
            n.confidence is not None,
            n.confidence if n.confidence is not None else -1.0,
        ),
        reverse=True,
    )
    return tuple(ranked[:query.limit])
