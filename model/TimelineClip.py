from moviepy import AudioClip, VideoClip

from controller.FileHandlerController import readAudioFile, readVideoFile
from controller.VideoController import seconds_to_frames
from model.Effects import AudioEffect, VideoEffect
from model.Source import Source

class TimelineClip:
    title: str
    start_frame: int
    duration_frames: int
    source: Source
    
    def __init__(self, title: str, source: Source, start_frame: int):
        self.source = source
        self.title = title
        self.start_frame = start_frame
        
class TimelineVideoClip(TimelineClip):
    videoClip: VideoClip
    audioClip: AudioClip | None
    fps: int
    effects: list[VideoEffect]
    
    def __init__(self, name: str, source: Source, start_frame: int, duration_frame = -1):
        super().__init__(name, source, start_frame)
        
        self.videoClip, self.audioClip, self.fps = readVideoFile(source)
        
        if duration_frame < 0:
            self.duration_frames = seconds_to_frames(self.videoClip.duration)
        else:
            self.duration_frames = duration_frame

        self.effects = []
            
        
class TimelineAudioClip(TimelineClip):
    audioClip: AudioClip
    frequency: int
    effects: list[AudioEffect]
    
    def __init__(self, name: str, source: Source, start_frame: int, duration_frame = -1):
        super().__init__(name, source, start_frame)
        
        self.audioClip, self.frequency = readAudioFile(source)
        
        # TODO : a revoir
        if duration_frame < 0:
            self.duration_frames = seconds_to_frames(self.audioClip.duration)
        else:
            self.duration_frames = duration_frame

        self.effects = []