from PySide6.QtCore import QObject, QTimer, Signal
from .FileHandlerController import readVideoFile


class VideoPreviewController(QObject):
    """Controller that manages playback and backend interaction."""

    timeChanged = Signal(float)        # current time in seconds
    durationChanged = Signal(float)    # total duration
    playbackStateChanged = Signal(bool)  # True = playing, False = paused

    def __init__(self, widget, fps=24):
        super().__init__()
        self.widget = widget  # VideoPreviewWidget (view)
        self.clip = None
        self.audio = None
        self.fps = fps
        self.duration = 0
        self.current_time = 0
        self.is_playing = False

        # Timer for playback
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_frame)

    def loadVideo(self, path: str) -> bool:
        try:
            self.clip, self.audio, self.fps = readVideoFile(path)
            self.duration = self.clip.duration
            self.current_time = 0
            self.durationChanged.emit(self.duration)
            self.seek(0)
            return True
        except Exception as e:
            print(f"Error loading video: {e}")
            return False

    def play(self):
        if self.clip and not self.is_playing:
            self.is_playing = True
            self.timer.start(int(1000 / self.fps))
            self.playbackStateChanged.emit(True)

    def pause(self):
        if self.is_playing:
            self.is_playing = False
            self.timer.stop()
            self.playbackStateChanged.emit(False)

    def togglePlayPause(self):
        if self.is_playing:
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
        self.current_time = t
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

        self.current_time += 1.0 / self.fps
        if self.current_time >= self.duration:
            self.current_time = self.duration
            self.pause()
            self.timeChanged.emit(self.current_time)
            return
        self.seek(self.current_time)

    def close(self):
        self.pause()
        if self.clip:
            self.clip.close()
