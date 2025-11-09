from typing import TYPE_CHECKING

from controller.VideoPreviewController import VideoPreviewController
from model.Source import Source
from model.Timeline import Timeline, TimelineType
from model.TimelineClip import TimelineAudioClip, TimelineClip, TimelineVideoClip

if TYPE_CHECKING:
    # import only for type checking to avoid circular imports at runtime
    from views.VideoEditor import VideoEditor


class TimelineController:
    # use a forward-reference string so the name isn't required at import time
    view: "VideoEditor"
    timelines: list[Timeline]
    
    def __init__(self, view) -> None:
        # keep a reference to the view instance (injected by the view)
        self.selectedClip = None
        self.view = view
        self.timelines = []

        if hasattr(self.view, "clipClicked"):
            self.view.clipClicked.connect(self.onClipClicked)
        
    def createTimeline(self, name: str, type: TimelineType) -> Timeline:
        timeline = Timeline(name, None, type)
        self.timelines.append(timeline)
        self.view.timeline.timeline_view.updateLayout()
        
        return timeline
        
    def addClip(self, timeline: Timeline, name: str, source: Source) -> TimelineClip:
        clip = None
        start_frame = 0
        
        if timeline.typee == TimelineType.VIDEO:
            clip = TimelineVideoClip(name, source, start_frame, fps=24)
        else: #timeline.type == AUDIO
            clip = TimelineAudioClip(name, source, start_frame)
        self.view.timeline.timeline_view.updateLayout()
        return clip


    def onClipClicked(self, clip):
        self.selectedClip = clip
        print(f"[TimelineController] Selected clip: {clip.title}")