from model.TimelineClip import TimelineClip
from views.widgets.QtEditorialTimelineWidget import DEFAULT_CONSTANTS


class Timeline:
    name: str
    height: int
    clips: list[TimelineClip]
    
    def __init__(self, name, height) -> None:
        self.name = name
        self.height = (
            height 
            if height is not None 
            else DEFAULT_CONSTANTS["DEFAULT_TRACK_HEIGHT"]
        )
        self.clips = []  # list of ClipData

    def add_clip(self, clip):
        self.clips.append(clip)
    
    def addClip(self, file) -> None:
        # todo
        pass