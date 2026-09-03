from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ProductionMode(StrEnum):
    CREATOR_STUDIO = "creator_studio"
    AI_AD_FACTORY = "ai_ad_factory"


class Platform(StrEnum):
    YOUTUBE = "youtube"
    TIKTOK = "tiktok"
    INSTAGRAM = "instagram"
    FACEBOOK = "facebook"
    LINKEDIN = "linkedin"
    OTHER = "other"


@dataclass(frozen=True, slots=True)
class ProductionBrief:
    id: str
    project_id: str
    mode: ProductionMode
    objective: str
    audience: str
    platform: Platform
    target_duration_seconds: int | None = None
    tone: tuple[str, ...] = ()
    must_include: tuple[str, ...] = ()
    must_avoid: tuple[str, ...] = ()
    delayed_reveals: tuple[str, ...] = ()
    brand_rules: tuple[str, ...] = ()
    language: str | None = None

    def __post_init__(self) -> None:
        if not self.objective.strip():
            raise ValueError("objective cannot be empty")
        if not self.audience.strip():
            raise ValueError("audience cannot be empty")
        if self.target_duration_seconds is not None and self.target_duration_seconds <= 0:
            raise ValueError("target_duration_seconds must be > 0")
