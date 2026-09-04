from __future__ import annotations
from .render_graph import RenderGraph, RenderOperation, RenderOperationKind, RenderProfile
from .timeline import Timeline, TrackKind


def compile_timeline_to_render_graph(timeline:Timeline, *, profile:RenderProfile)->RenderGraph:
    timeline.validate(); ops=[]
    for track in sorted(timeline.tracks,key=lambda t:t.order):
        for item in sorted(track.items,key=lambda i:i.timeline_range.start.fraction):
            if item.source_asset_id:
                kind=RenderOperationKind.SOURCE_CLIP if track.kind in {TrackKind.VIDEO,TrackKind.AUDIO} else RenderOperationKind.OVERLAY
                ops.append(RenderOperation(id=f"render-{item.id}",kind=kind,timeline_range=item.timeline_range,source_asset_id=item.source_asset_id,source_range=item.source_range,params={"track_id":track.id,"track_kind":track.kind.value,**item.params}))
            elif track.kind==TrackKind.CAPTION:
                ops.append(RenderOperation(id=f"render-{item.id}",kind=RenderOperationKind.CAPTION_LAYER,timeline_range=item.timeline_range,params=item.params))
            elif track.kind in {TrackKind.GRAPHIC,TrackKind.VIDEO}:
                ops.append(RenderOperation(id=f"render-{item.id}",kind=RenderOperationKind.OVERLAY,timeline_range=item.timeline_range,params=item.params))
    graph=RenderGraph(schema_version=timeline.schema_version,project_id=timeline.project_id,timeline_id=timeline.id,profile=profile,operations=tuple(ops))
    graph.validate(); return graph
