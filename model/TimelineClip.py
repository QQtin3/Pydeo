from moviepy import AudioClip, VideoClip

from controller.FileHandlerController import readAudioFile, readVideoFile
from model.Effects import AudioEffect, VideoEffect

class TimelineClip:
    name: str
    start: float
    end: float
    filePath: str 
    
    def __init__(self, name: str, start: float, end: float, filePath: str):
        self.name = name
        self.start = start
        self.end = end
        self.filePath = filePath
        
class TimelineVideoClip(TimelineClip):
    videoClip: VideoClip
    audioClip: AudioClip | None
    fps: int
    effects: list[VideoEffect]
    
    def __init__(self, name: str, start: float, filePath: str):
        super().__init__(name, start, 0, filePath)
        
        self.videoClip, self.audioClip, self.fps = readVideoFile(self.filePath)
        self.end = self.videoClip.duration  # Change la fin mise par défaut à 0
        
        
class TimelineAudioClip(TimelineClip):
    audioClip: AudioClip
    frequency: int
    effects: list[AudioEffect]
    
    def __init__(self, name: str, start: float, filePath: str):
        super().__init__(name, start, 0, filePath)
        
        self.audioClip, self.frequency = readAudioFile(self.filePath)
        self.end = self.audioClip.duration  # Change la fin mise par défaut à 0
