from typing import TYPE_CHECKING

from model.Source import Source
from model.Timeline import Timeline, TimelineType
from model.TimelineClip import TimelineAudioClip, TimelineClip, TimelineVideoClip

if TYPE_CHECKING:
    # import only for type checking to avoid circular imports at runtime
    from views.widgets.QtEditorialTimelineWidget import TimelineView


class TimelineController:
    # use a forward-reference string so the name isn't required at import time
    view: "TimelineView"
    timelines: list[Timeline]
    
    def __init__(self, view) -> None:
        # keep a reference to the view instance (injected by the view)
        self.view = view
        self.timelines = []
        
    def createTimeline(self, name: str, type: TimelineType) -> Timeline:
        timeline = Timeline(name, None, type)
        self.timelines.append(timeline)
        self.view.updateLayout()
        
        return timeline
        
    def addClip(self, timeline: Timeline, name: str, source: Source) -> TimelineClip:
        clip = None
        start_frame = 0
        
        if timeline.typee == TimelineType.VIDEO:
            clip = TimelineVideoClip(name, source, start_frame)
        else: #timeline.type == AUDIO
            clip = TimelineAudioClip(name, source, start_frame)
        
        self.view.updateLayout()
        return clip