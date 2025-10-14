from model.Source import Source
from model.Timeline import Timeline, TimelineType
from model.TimelineClip import TimelineAudioClip, TimelineClip, TimelineVideoClip
from views.widgets.QtEditorialTimelineWidget import TimelineView


class TimelineController:
    view: TimelineView
    timelines: list[Timeline]
    
    def __init__(self, view) -> None:
        self.timelines = []
        
    def createTimeline(self, name: str, type: TimelineType) -> Timeline:
        timeline = Timeline(name, None, type)
        self.timelines.append(timeline)
        self.view.updateLayout()
        
        return timeline
        
    def addClip(self, timeline: Timeline, name: str, source: Source) -> TimelineClip:
        clip = None
        start_frame = 0
        
        if timeline.type == TimelineType.VIDEO:
            clip = TimelineVideoClip(name, source, start_frame)
        else: #timeline.type == AUDIO
            clip = TimelineAudioClip(name, source, start_frame)
        
        self.view.updateLayout()
        return clip