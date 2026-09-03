from __future__ import annotations

from dataclasses import dataclass

from .intelligence_graph import MediaIntelligenceGraph
from .production_brief import ProductionBrief
from .story import StoryBeatKind, StoryProposal


@dataclass(frozen=True, slots=True)
class StoryValidationIssue:
    code: str
    message: str
    beat_id: str | None = None


@dataclass(frozen=True, slots=True)
class StoryValidationReport:
    valid: bool
    issues: tuple[StoryValidationIssue, ...]


def validate_story_proposal(
    proposal: StoryProposal,
    *,
    brief: ProductionBrief,
    graph: MediaIntelligenceGraph,
) -> StoryValidationReport:
    issues: list[StoryValidationIssue] = []
    graph_node_ids = {n.id for n in graph.nodes}

    if proposal.project_id != brief.project_id or graph.project_id != brief.project_id:
        issues.append(StoryValidationIssue("project_mismatch", "project identifiers do not match"))

    if not any(beat.kind == StoryBeatKind.HOOK for beat in proposal.beats):
        issues.append(StoryValidationIssue("missing_hook", "story has no hook beat"))

    if not any(beat.kind in {StoryBeatKind.PAYOFF, StoryBeatKind.REVEAL} for beat in proposal.beats):
        issues.append(StoryValidationIssue("missing_payoff", "story has no reveal/payoff beat"))

    for beat in proposal.beats:
        for node_id in beat.candidate_node_ids:
            if node_id not in graph_node_ids:
                issues.append(
                    StoryValidationIssue(
                        "unknown_evidence_node",
                        f"beat references unknown intelligence node {node_id}",
                        beat.id,
                    )
                )
        for evidence in beat.evidence:
            if evidence.range is None and not evidence.transcript_word_ids and not evidence.frame_ids:
                issues.append(
                    StoryValidationIssue(
                        "weak_evidence",
                        "evidence has no temporal/transcript/frame grounding",
                        beat.id,
                    )
                )

    title_and_premise = f"{proposal.title} {proposal.premise}".casefold()
    for forbidden in brief.must_avoid:
        if forbidden.casefold() in title_and_premise:
            issues.append(
                StoryValidationIssue(
                    "violates_must_avoid",
                    f"proposal contains forbidden concept: {forbidden}",
                )
            )

    return StoryValidationReport(valid=not issues, issues=tuple(issues))
