from moviepy import AudioClip, VideoClip

from controller.FileHandlerController import readAudioFile, readVideoFile
from model.Effects import AudioEffect, VideoEffect

class TimelineClip:
    title: str
    start_frame: float
    duration_frames: int
    filePath: str 
    
    def __init__(self, title: str, start_frame: float, duration_frames: int, filePath: str):
        self.start_frame = start_frame
        self.duration_frames = duration_frames
        self.title = title
        self.filePath = filePath
        
class TimelineVideoClip(TimelineClip):
    videoClip: VideoClip
    audioClip: AudioClip | None
    fps: int
    effects: list[VideoEffect]
    
    def __init__(self, name: str, start_frame: float, duration_frame, filePath: str):
        super().__init__(name, start_frame, duration_frame, filePath)
        
        self.videoClip, self.audioClip, self.fps = readVideoFile(self.filePath)
        
class TimelineAudioClip(TimelineClip):
    audioClip: AudioClip
    frequency: int
    effects: list[AudioEffect]
    
    def __init__(self, name: str, start: float, duration_frames: int, filePath: str):
        super().__init__(name, start, duration_frames, filePath)
        
        self.audioClip, self.frequency = readAudioFile(self.filePath)