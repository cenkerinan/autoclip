from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from .intelligence_graph import IntelligenceNodeType, MediaIntelligenceGraph
from .production_brief import ProductionBrief
from .story import StoryProposal


@dataclass(frozen=True, slots=True)
class ProducerEvidencePack:
    project_id: str
    objective: str
    audience: str
    constraints: tuple[str, ...]
    hook_node_ids: tuple[str, ...]
    question_node_ids: tuple[str, ...]
    claim_node_ids: tuple[str, ...]
    reaction_node_ids: tuple[str, ...]
    reveal_node_ids: tuple[str, ...]
    payoff_node_ids: tuple[str, ...]
    visual_node_ids: tuple[str, ...]
    proof_node_ids: tuple[str, ...]


def build_producer_evidence_pack(
    brief: ProductionBrief,
    graph: MediaIntelligenceGraph,
    *,
    per_type_limit: int = 30,
) -> ProducerEvidencePack:
    if brief.project_id != graph.project_id:
        raise ValueError("brief and graph must belong to the same project")
    if per_type_limit <= 0:
        raise ValueError("per_type_limit must be > 0")

    def ids(type_: IntelligenceNodeType) -> tuple[str, ...]:
        nodes = sorted(
            graph.nodes_of_type(type_),
            key=lambda n: n.confidence if n.confidence is not None else -1.0,
            reverse=True,
        )
        return tuple(n.id for n in nodes[:per_type_limit])

    constraints = (
        tuple(f"must_include:{v}" for v in brief.must_include)
        + tuple(f"must_avoid:{v}" for v in brief.must_avoid)
        + tuple(f"delay_reveal:{v}" for v in brief.delayed_reveals)
        + tuple(f"brand_rule:{v}" for v in brief.brand_rules)
    )

    return ProducerEvidencePack(
        project_id=brief.project_id,
        objective=brief.objective,
        audience=brief.audience,
        constraints=constraints,
        hook_node_ids=ids(IntelligenceNodeType.HOOK),
        question_node_ids=ids(IntelligenceNodeType.QUESTION),
        claim_node_ids=ids(IntelligenceNodeType.CLAIM),
        reaction_node_ids=ids(IntelligenceNodeType.REACTION),
        reveal_node_ids=ids(IntelligenceNodeType.REVEAL),
        payoff_node_ids=ids(IntelligenceNodeType.PAYOFF),
        visual_node_ids=ids(IntelligenceNodeType.VISUAL_EVENT),
        proof_node_ids=ids(IntelligenceNodeType.PROOF),
    )


class StoryGenerator(Protocol):
    def generate(
        self,
        *,
        brief: ProductionBrief,
        graph: MediaIntelligenceGraph,
        evidence_pack: ProducerEvidencePack,
        count: int,
    ) -> tuple[StoryProposal, ...]:
        ...


@dataclass(frozen=True, slots=True)
class ProducerResult:
    brief_id: str
    proposals: tuple[StoryProposal, ...]


def generate_story_proposals(
    *,
    brief: ProductionBrief,
    graph: MediaIntelligenceGraph,
    generator: StoryGenerator,
    count: int = 3,
) -> ProducerResult:
    if count <= 0:
        raise ValueError("count must be > 0")
    graph.validate()
    pack = build_producer_evidence_pack(brief, graph)
    proposals = generator.generate(
        brief=brief,
        graph=graph,
        evidence_pack=pack,
        count=count,
    )
    if not proposals:
        raise ValueError("producer returned no story proposals")
    if len(proposals) > count:
        raise ValueError("producer returned more proposals than requested")
    for proposal in proposals:
        if proposal.project_id != brief.project_id:
            raise ValueError("proposal belongs to another project")
    return ProducerResult(brief.id, proposals)
