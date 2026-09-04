from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any, Protocol

from .intelligence_graph import MediaIntelligenceGraph
from .production_brief import ProductionBrief
from .story import StoryProposal
from .timecode import TimeRange


class EditDecisionKind(StrEnum):
    PRIMARY_CLIP = "primary_clip"
    BROLL = "broll"
    REACTION = "reaction"
    CUTAWAY = "cutaway"
    GRAPHIC = "graphic"
    GENERATED_VISUAL = "generated_visual"
    MUSIC_CUE = "music_cue"
    PAUSE = "pause"


@dataclass(frozen=True, slots=True)
class EditDecision:
    id: str
    kind: EditDecisionKind
    story_beat_id: str
    source_asset_id: str | None
    source_range: TimeRange | None
    target_duration_seconds: float | None = None
    intelligence_node_ids: tuple[str, ...] = ()
    rationale: str = ""
    params: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        source_kinds = {EditDecisionKind.PRIMARY_CLIP, EditDecisionKind.BROLL, EditDecisionKind.REACTION, EditDecisionKind.CUTAWAY}
        if self.kind in source_kinds and (not self.source_asset_id or self.source_range is None):
            raise ValueError(f"{self.kind} requires source asset and source range")
        if self.target_duration_seconds is not None and self.target_duration_seconds <= 0:
            raise ValueError("target_duration_seconds must be > 0")


@dataclass(frozen=True, slots=True)
class DirectionPlan:
    id: str
    project_id: str
    story_proposal_id: str
    decisions: tuple[EditDecision, ...]
    pacing_notes: tuple[str, ...] = ()
    visual_language: tuple[str, ...] = ()
    audio_language: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.decisions:
            raise ValueError("direction plan requires at least one edit decision")


class DirectorAgent(Protocol):
    def direct(self, *, brief: ProductionBrief, story: StoryProposal, graph: MediaIntelligenceGraph) -> DirectionPlan: ...


def generate_direction_plan(*, brief: ProductionBrief, story: StoryProposal, graph: MediaIntelligenceGraph, director: DirectorAgent) -> DirectionPlan:
    if not (brief.project_id == story.project_id == graph.project_id):
        raise ValueError("brief, story and graph must belong to the same project")
    graph.validate()
    plan = director.direct(brief=brief, story=story, graph=graph)
    if plan.project_id != brief.project_id or plan.story_proposal_id != story.id:
        raise ValueError("direction plan references wrong project/story")
    return plan
