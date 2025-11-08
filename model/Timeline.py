from enum import Enum
from model.TimelineClip import TimelineClip
from model.WidgetConfig import DEFAULT_CONSTANTS

from model.TimelineClip import TimelineClip, TimelineVideoClip, TimelineAudioClip
from controller.utils.fileExtensions import isFileVideo

class TimelineType(Enum):
    VIDEO = 1
    AUDIO = 2

class Timeline:
    name: str
    height: int
    typee: TimelineType
    clips: list[TimelineClip]
        
    def __init__(self, name, height = None, typee = TimelineType.VIDEO) -> None:
        self.name = name
        self.height = (
            height 
            if height is not None 
            else DEFAULT_CONSTANTS["DEFAULT_TRACK_HEIGHT"]
        )
        self.typee = typee
        self.clips = []

    def add_clip(self, clip):
        self.clips.append(clip)
        