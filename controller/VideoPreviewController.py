from PySide6.QtCore import QObject, QTimer, Signal
from moviepy import AudioClip, AudioFileClip, CompositeAudioClip, VideoClip, CompositeVideoClip

from controller.VideoController import cutVideo, apply_video_effects
from model.Timeline import Timeline
from model.TimelineClip import TimelineAudioClip, TimelineClip, TimelineVideoClip
from views.VideoPreviewWidget import VideoPreviewWidget
from model.Source import Source

from controller.FileHandlerController import readVideoFile
import os


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
        return self.clips[i], self.clipIndexes[i]

class VideoPreviewController(QObject):
    """Controller that manages playback and backend interaction."""

    timeChanged = Signal(float)        # current time in seconds
    durationChanged = Signal(float)    # total duration
    playbackStateChanged = Signal(bool)  # True = playing, False = paused
    
    widget: VideoPreviewWidget
    clip: VideoClip | None
    audio: AudioClip | None
    fps: int
    duration: int
    currentTime: float
    isPlaying: bool
    previewFps: int

    def __init__(self, widget: VideoPreviewWidget, fps=24):
        super().__init__()
        self.widget = widget  # VideoPreviewWidget (view)
        self.clip = None
        self.audio = None
        self.fps = fps
        self.duration = 0
        self.currentTime = 0
        self.isPlaying = False
        
        self.previewFps = 12

        # Timer for playback
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_frame)
        
    def getDuration(self):
        return self.duration

    # def loadVideo(self, path: str) -> bool:
    #     try:
    #         laSource = Source()
    #         laSource.name = os.path.basename(path or "")
    #         laSource.filepath = path
    #         self.clip, self.audio, self.fps = readVideoFile(laSource)
    #         self.duration = self.clip.duration
    #         self.currentTime = 0
    #         self.durationChanged.emit(self.duration)
    #         self.seek(0)
    #         return True
    #     except Exception as e:
    #         print(f"Error loading video: {e}")
    #         return False
    
    def loadVideo(self, timelines: list[Timeline]) -> bool:
        self.clip, self.audio = self.render(timelines)
        # self.clip = timelines[1].clips[0].videoClip
        
        # self.clip = self.clip.with_fps(self.fps)
        
        self.duration = int(round(self.clip.duration * self.fps))
        self.currentTime = 0
        self.durationChanged.emit(self.duration)
        self.seek(0)
        return True

    
    def play(self):
        if self.clip and not self.isPlaying:
            self.isPlaying = True
            self.timer.start(int((1 / self.previewFps) * 1000))
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

        frame = self.clip.get_frame(t)
        self.widget.set_frame(frame)
        self.timeChanged.emit(t)

    def _update_frame(self):
        if not self.clip:
            self.pause()
            return

        self.currentTime += (1 / self.previewFps) * self.fps
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
        clips :list[TimelineClip] = []
        subClips = []
        
        for t in timelines:
            clips.extend(t.clips)
            indexes.extend([len(timelines) - timelines.index(t)] * len(t.clips))
            
        clips.sort(key=lambda c: c.start_frame)
        
        if len(clips) == 1:
            subClips.append(SubClip([clips[0]], [indexes[0]], clips[0].start_frame, clips[0].end))
        
        for i in range(len(clips) - 1):
            if clips[i].end > clips[i+1].start_frame:
                subClips.append(SubClip(
                    [clips[i]], 
                    [indexes[i]], 
                    clips[i].start_frame, 
                    clips[i].end
                ))
                
                if clips[i].end < clips[i+1].end:
                    subClips.append(SubClip(
                            [clips[i], clips[i+1]], 
                            [indexes[i], indexes[i+1]], 
                            clips[i+1].start_frame, 
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
                        clips[i+1].start_frame, 
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
                match clip:
                    case TimelineVideoClip():
                        frame = clip.end - clip.start_frame
                        c, _ = cutVideo(clip.videoClip, frame, clip.fps)
                        c.layer_index = index
                        # c.start = clip.start_frame
                        # c.end = clip.end
                        # c.duration = c.end - c.start
                        
                        audioClips.append(c.audio)
                        
                        videoClips.append(c)
                        break
                    
                    case TimelineAudioClip():
                        # TODO
                        # frame = (clip.end - clip.start) * clip.frequency
                        # c = cutVideo(clip, frame, clip.frequency)
                    
                        break
                        
                    case _:
                        pass
        
        videoClip, audioClip = None, None
        if len(videoClips) == 0:
            videoClip = VideoClip()
        else:
            videoClip = CompositeVideoClip(videoClips, (1920, 1080))

        if len(audioClips) == 0:
            audioClip = AudioClip()
        else:
            audioClip = CompositeAudioClip(audioClips)

        return videoClip, audioClip

    def refreshPreview(self, selectedClip):
        """Rebuild the current clip preview when effects are added."""
        if not selectedClip or not hasattr(selectedClip, "videoClip"):
            print("[VideoPreviewController] No valid clip to preview.")
            return

        try:
            processed_clip = apply_video_effects(selectedClip.videoClip, getattr(selectedClip, "effects", []))
            self.clip = processed_clip
            self.duration = processed_clip.duration
            self.seek(0)
            print(f"[VideoPreviewController] Preview refreshed with {len(selectedClip.effects)} effect(s).")
        except Exception as e:
            print(f"[VideoPreviewController] Error refreshing preview: {e}")
