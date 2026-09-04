from __future__ import annotations
from dataclasses import dataclass
from enum import StrEnum
from .timecode import TimePoint
from .transcript import TranscriptWord

class SnapDirection(StrEnum):
    NEAREST="nearest"; BEFORE="before"; AFTER="after"

@dataclass(frozen=True, slots=True)
class CutSnapResult:
    requested:TimePoint; snapped:TimePoint; word_id:str|None; boundary:str|None


def snap_cut_to_word_boundary(requested:TimePoint, words:tuple[TranscriptWord,...], *, direction:SnapDirection=SnapDirection.NEAREST, max_distance_seconds:float=.35)->CutSnapResult:
    if max_distance_seconds < 0: raise ValueError("max_distance_seconds must be >= 0")
    candidates=[]
    for w in words:
        candidates.append((w.range.start,w.id,"start")); candidates.append((w.range.end,w.id,"end"))
    eligible=[]
    for point,wid,boundary in candidates:
        delta=float(point.fraction-requested.fraction)
        if abs(delta)>max_distance_seconds: continue
        if direction==SnapDirection.BEFORE and delta>0: continue
        if direction==SnapDirection.AFTER and delta<0: continue
        eligible.append((abs(delta),point,wid,boundary))
    if not eligible: return CutSnapResult(requested,requested,None,None)
    _,point,wid,boundary=min(eligible,key=lambda x:x[0])
    return CutSnapResult(requested,point,wid,boundary)
