from moviepy import AudioClip, VideoClip

from controller.FileHandlerController import readAudioFile, readVideoFile
from model.Effects import AudioEffect, VideoEffect

class TimelineClip:
    name: str
    start: float
    end: float
    filePath: str 
    originalDuration: float
    
    def __init__(self, name: str, start: float, end: float, filePath: str):
        self.name = name
        self.start = start
        self.end = end
        self.filePath = filePath
        self.originalDuration = readVideoFile(filePath)[0].duration
        self.duration = end - start

class TimelineVideoClip(TimelineClip):
    videoClip: VideoClip
    audioClip: AudioClip | None
    fps: int
    effects: list[VideoEffect]
    
    def __init__(self, name: str, start: float, end: float, filePath: str):
        super().__init__(name, start, end, filePath)
        
        self.videoClip, self.audioClip, self.fps = readVideoFile(self.filePath)
        
class TimelineAudioClip(TimelineClip):
    audioClip: AudioClip
    frequency: int
    effects: list[AudioEffect]
    
    def __init__(self, name: str, start: float, end: float, filePath: str):
        super().__init__(name, start, end, filePath)
        
        self.audioClip, self.frequency = readAudioFile(self.filePath)