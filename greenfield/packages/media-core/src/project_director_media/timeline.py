from __future__ import annotations
from dataclasses import dataclass, field
from enum import StrEnum
from fractions import Fraction
from typing import Any
from .timecode import TimeRange

class TrackKind(StrEnum):
    VIDEO="video"; AUDIO="audio"; CAPTION="caption"; GRAPHIC="graphic"

@dataclass(frozen=True, slots=True)
class TimelineItem:
    id:str; track_id:str; timeline_range:TimeRange
    source_asset_id:str|None=None; source_range:TimeRange|None=None
    intelligence_node_ids:tuple[str,...]=(); story_beat_id:str|None=None; decision_id:str|None=None
    params:dict[str,Any]=field(default_factory=dict)
    def __post_init__(self):
        if (self.source_asset_id is None) != (self.source_range is None): raise ValueError("source asset/range must be supplied together")

@dataclass(frozen=True, slots=True)
class TimelineTrack:
    id:str; kind:TrackKind; name:str; order:int; items:tuple[TimelineItem,...]=()

@dataclass(frozen=True, slots=True)
class Timeline:
    id:str; project_id:str; schema_version:str; tracks:tuple[TimelineTrack,...]; parent_timeline_id:str|None=None
    def validate(self):
        track_ids=set(); item_ids=set()
        for track in self.tracks:
            if track.id in track_ids: raise ValueError(f"duplicate track id: {track.id}")
            track_ids.add(track.id); previous_end=None
            for item in sorted(track.items,key=lambda i:i.timeline_range.start.fraction):
                if item.id in item_ids: raise ValueError(f"duplicate item id: {item.id}")
                item_ids.add(item.id)
                if item.track_id != track.id: raise ValueError(f"item {item.id} references wrong track")
                if previous_end is not None and item.timeline_range.start.fraction < previous_end: raise ValueError(f"overlapping items on track {track.id}")
                previous_end=item.timeline_range.end.fraction
    @property
    def duration(self)->Fraction:
        return max((i.timeline_range.end.fraction for t in self.tracks for i in t.items),default=Fraction(0,1))
