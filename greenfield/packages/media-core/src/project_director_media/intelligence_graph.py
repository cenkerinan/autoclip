from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any, Iterable

from .timecode import TimeRange


class IntelligenceNodeType(StrEnum):
    TRANSCRIPT_SPAN = "transcript_span"
    SPEAKER = "speaker"
    SHOT = "shot"
    SCENE = "scene"
    TOPIC = "topic"
    ENTITY = "entity"
    QUESTION = "question"
    CLAIM = "claim"
    REACTION = "reaction"
    VISUAL_EVENT = "visual_event"
    AUDIO_EVENT = "audio_event"
    HOOK = "hook"
    OPEN_LOOP = "open_loop"
    REVEAL = "reveal"
    PAYOFF = "payoff"
    CTA = "cta"
    STORY_BEAT = "story_beat"
    PRODUCT = "product"
    OFFER = "offer"
    OBJECTION = "objection"
    PROOF = "proof"


class IntelligenceEdgeType(StrEnum):
    SPOKEN_BY = "spoken_by"
    OCCURS_IN = "occurs_in"
    SHOWS = "shows"
    ANSWERS = "answers"
    SUPPORTS = "supports"
    CONTRADICTS = "contradicts"
    REVEALS = "reveals"
    PAYS_OFF = "pays_off"
    REFERS_TO = "refers_to"
    VISUALLY_SUPPORTS = "visually_supports"
    SAME_TOPIC = "same_topic"
    SAME_ENTITY = "same_entity"
    RESPONDS_TO = "responds_to"
    EVIDENCE_FOR = "evidence_for"


@dataclass(frozen=True, slots=True)
class Provenance:
    producer: str
    model: str | None = None
    version: str | None = None
    config_hash: str | None = None


@dataclass(frozen=True, slots=True)
class EvidenceRef:
    asset_id: str
    range: TimeRange | None = None
    transcript_word_ids: tuple[str, ...] = ()
    frame_ids: tuple[str, ...] = ()
    derived_asset_ids: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class IntelligenceNode:
    id: str
    project_id: str
    type: IntelligenceNodeType
    label: str
    range: TimeRange | None = None
    confidence: float | None = None
    attributes: dict[str, Any] = field(default_factory=dict)
    evidence: tuple[EvidenceRef, ...] = ()
    provenance: Provenance | None = None

    def __post_init__(self) -> None:
        if not self.label:
            raise ValueError("node label cannot be empty")
        if self.confidence is not None and not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")
        if self.type not in {IntelligenceNodeType.SPEAKER, IntelligenceNodeType.TOPIC, IntelligenceNodeType.ENTITY}:
            if not self.evidence:
                raise ValueError(f"{self.type} node requires evidence")


@dataclass(frozen=True, slots=True)
class IntelligenceEdge:
    id: str
    project_id: str
    type: IntelligenceEdgeType
    from_node_id: str
    to_node_id: str
    confidence: float | None = None
    attributes: dict[str, Any] = field(default_factory=dict)
    provenance: Provenance | None = None

    def __post_init__(self) -> None:
        if self.from_node_id == self.to_node_id:
            raise ValueError("self edges are not allowed")
        if self.confidence is not None and not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")


@dataclass(frozen=True, slots=True)
class MediaIntelligenceGraph:
    project_id: str
    schema_version: str
    nodes: tuple[IntelligenceNode, ...] = ()
    edges: tuple[IntelligenceEdge, ...] = ()

    def validate(self) -> None:
        node_ids: set[str] = set()
        edge_ids: set[str] = set()

        for node in self.nodes:
            if node.project_id != self.project_id:
                raise ValueError("node belongs to another project")
            if node.id in node_ids:
                raise ValueError(f"duplicate node id: {node.id}")
            node_ids.add(node.id)

        for edge in self.edges:
            if edge.project_id != self.project_id:
                raise ValueError("edge belongs to another project")
            if edge.id in edge_ids:
                raise ValueError(f"duplicate edge id: {edge.id}")
            edge_ids.add(edge.id)
            if edge.from_node_id not in node_ids or edge.to_node_id not in node_ids:
                raise ValueError(f"edge {edge.id} references unknown node")

    def nodes_of_type(self, *types: IntelligenceNodeType) -> tuple[IntelligenceNode, ...]:
        wanted = set(types)
        return tuple(node for node in self.nodes if node.type in wanted)

    def temporal_nodes(self, range_: TimeRange) -> tuple[IntelligenceNode, ...]:
        return tuple(
            node for node in self.nodes
            if node.range is not None and node.range.intersects(range_)
        )

    def neighbors(
        self,
        node_id: str,
        *,
        edge_types: Iterable[IntelligenceEdgeType] | None = None,
    ) -> tuple[IntelligenceNode, ...]:
        by_id = {node.id: node for node in self.nodes}
        allowed = set(edge_types) if edge_types is not None else None
        ids: list[str] = []
        for edge in self.edges:
            if allowed is not None and edge.type not in allowed:
                continue
            if edge.from_node_id == node_id:
                ids.append(edge.to_node_id)
            elif edge.to_node_id == node_id:
                ids.append(edge.from_node_id)
        return tuple(by_id[i] for i in ids if i in by_id)
