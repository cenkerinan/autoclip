from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

from .intelligence_graph import EvidenceRef


class StoryBeatKind(StrEnum):
    HOOK = "hook"
    SETUP = "setup"
    CURIOSITY = "curiosity"
    CONFLICT = "conflict"
    ESCALATION = "escalation"
    PROOF = "proof"
    REVEAL = "reveal"
    PAYOFF = "payoff"
    CTA = "cta"


@dataclass(frozen=True, slots=True)
class StoryBeat:
    id: str
    kind: StoryBeatKind
    intent: str
    evidence: tuple[EvidenceRef, ...]
    candidate_node_ids: tuple[str, ...] = ()
    target_duration_seconds: int | None = None

    def __post_init__(self) -> None:
        if not self.intent:
            raise ValueError("story beat intent cannot be empty")
        if not self.evidence and not self.candidate_node_ids:
            raise ValueError("story beat requires evidence or candidate nodes")


@dataclass(frozen=True, slots=True)
class StoryScore:
    hook: float
    coherence: float
    novelty: float
    emotional_interest: float
    visual_potential: float
    payoff: float

    def __post_init__(self) -> None:
        for name, value in (
            ("hook", self.hook),
            ("coherence", self.coherence),
            ("novelty", self.novelty),
            ("emotional_interest", self.emotional_interest),
            ("visual_potential", self.visual_potential),
            ("payoff", self.payoff),
        ):
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{name} must be between 0 and 1")


@dataclass(frozen=True, slots=True)
class StoryProposal:
    id: str
    project_id: str
    title: str
    premise: str
    audience_promise: str
    beats: tuple[StoryBeat, ...]
    score: StoryScore
    risks: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.title or not self.premise or not self.audience_promise:
            raise ValueError("story proposal requires title, premise and audience promise")
        if not self.beats:
            raise ValueError("story proposal requires at least one beat")
