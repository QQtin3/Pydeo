from PySide6.QtCore import QObject, QTimer, Signal
from moviepy import AudioClip, CompositeAudioClip, VideoClip, CompositeVideoClip

from controller.VideoController import cutVideo
from model.TimelineClip import TimelineClip
from model.Timeline import Timeline
from views.VideoPreviewWidget import VideoPreviewWidget
from .FileHandlerController import readVideoFile

class SubClip:
    """Sous-classe représentant un sous-clip, c-à-d un ensemble de clips de timeline qui se chevauchent"""
    
    clips: list[TimelineClip]
    clipIndexes: list[int]
    start: float
    end: float
    
    def __init__(self, clips: list[TimelineClip], clipIndexes: list[int], start: float, end: float) -> None:
        self.clips = clips
        self.clipIndexes = clipIndexes
        self.start = start
        self.end = end
        
    def __len__(self) -> int:
        return len(self.clips)
    
    def getClipAndIndex(self, i) -> tuple[TimelineClip, int]:
        return (self.clips[i], self.clipIndexes[i])


class VideoPreviewController(QObject):
    """Controller that manages playback and backend interaction."""

    timeChanged = Signal(float)        # current time in seconds
    durationChanged = Signal(float)    # total duration
    playbackStateChanged = Signal(bool)  # True = playing, False = paused
    
    widget: VideoPreviewWidget
    clip: VideoClip | None
    audio: AudioClip | None
    fps: int
    duration: float
    currentTime: float
    isPlaying: bool

    def __init__(self, widget: VideoPreviewWidget, fps=24):
        super().__init__()
        self.widget = widget  # VideoPreviewWidget (view)
        self.clip = None
        self.audio = None
        self.fps = fps
        self.duration = 0
        self.currentTime = 0
        self.isPlaying = False

        # Timer for playback
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_frame)

    # def loadVideo(self, path: str) -> bool:
    #     try:
    #         self.clip, self.audio, self.fps = readVideoFile(path)
    #         self.duration = self.clip.duration
    #         self.currentTime = 0
    #         self.durationChanged.emit(self.duration)
    #         self.seek(0)
    #         return True
    #     except Exception as e:
    #         print(f"Error loading video: {e}")
    #         return False
    def loadVideo(self, timelines: list[Timeline]) -> bool:
        try:
            self.clip, self.audio = self.render(timelines)
            self.duration = self.clip.duration
            self.currentTime = 0
            self.durationChanged.emit(self.duration)
            self.seek(0)
            return True
        except Exception as e:
            print(f"Error loading video: {e}")
            return False

    def play(self):
        if self.clip and not self.isPlaying:
            self.isPlaying = True
            self.timer.start(int(1000 / self.fps))
            self.playbackStateChanged.emit(True)

    def pause(self):
        if self.isPlaying:
            self.isPlaying = False
            self.timer.stop()
            self.playbackStateChanged.emit(False)

    def togglePlayPause(self):
        if self.isPlaying:
            self.pause()
        else:
            self.play()

    def stop(self):
        self.pause()
        self.seek(0)

    def seek(self, t: float):
        if not self.clip:
            return
        t = max(0, min(t, self.duration))
        self.currentTime = t
        try:
            frame = self.clip.get_frame(t)
            self.widget.set_frame(frame)
            self.timeChanged.emit(t)
        except Exception as e:
            print(f"Seek error: {e}")

    def _update_frame(self):
        if not self.clip:
            self.pause()
            return

        self.currentTime += 1.0 / self.fps
        if self.currentTime >= self.duration:
            self.currentTime = self.duration
            self.pause()
            self.timeChanged.emit(self.currentTime)
            return
        self.seek(self.currentTime)

    def close(self):
        self.pause()
        if self.clip:
            self.clip.close()
            
    def getClips(self, timelines: list[Timeline]) -> list[SubClip]: 
        indexes = []
        clips = []
        subClips = []
        
        for t in timelines:
            clips.extend(t.clips)
            indexes.extend([timelines.index(t)] * len(t.clips))
            
        clips.sort(key=lambda c: c.start)
        
        for i in range(len(clips) - 1):
            if clips[i].end > clips[i+1].start:
                subClips.append(SubClip(
                    [clips[i]], 
                    [indexes[i]], 
                    clips[i].start, 
                    clips[i].end
                ))
                
                if clips[i].end < clips[i+1].end:
                    subClips.append(SubClip(
                            [clips[i], clips[i+1]], 
                            [indexes[i], indexes[i+1]], 
                            clips[i+1].start, 
                            clips[i].end
                    ))
                    subClips.append(SubClip(
                        [clips[i+1]], 
                        [indexes[i+1]], 
                        clips[i].end, 
                        clips[i+1].end
                    ))
                else:
                    subClips.append(SubClip(
                        [clips[i], clips[i+1]], 
                        [indexes[i], indexes[i+1]], 
                        clips[i+1].start, 
                        clips[i].end
                    ))
                    subClips.append(SubClip(
                        [clips[i+1]], 
                        [indexes[i+1]], 
                        clips[i].end, 
                        clips[i+1].end
                    ))
                    
        return subClips
        
    def render(self, timelines: list[Timeline]) -> tuple[VideoClip, AudioClip]:
        subClips = self.getClips(timelines)
        videoClips = []
        audioClips = []
        
        for subClip in subClips:
            for i in range(len(subClip)):
                clip, index = subClip.getClipAndIndex(i)
                match type(clip):
                    case "VideoTimelineClip":
                        frame = (clip.end - clip.start) * clip.fps
                        _, c = cutVideo(clip, frame, clip.fps)
                        c.layer_index = index
                        c.start = clip.start
                        c.end = clip.end
                        
                        videoClips.append(c)
                        break
                    
                    case "AudioTimelineClip":
                        # TODO
                        # frame = (clip.end - clip.start) * clip.frequency
                        # c = cutVideo(clip, frame, clip.frequency)
                    
                        break
                        
                    case _:
                        pass

                        
        return CompositeVideoClip(videoClips), CompositeAudioClip(audioClips)