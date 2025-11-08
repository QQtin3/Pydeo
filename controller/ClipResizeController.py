from PySide6.QtCore import QObject, Signal
from views.widgets.QtEditorialTimelineWidget import ClipData
from model.TimelineClip import TimelineClip

class ClipResizeController(QObject):
    clipResized = Signal(object, int, int) # clip, old_duration, new_duration
    clipMoved = Signal(object, int, int) # clip, old_start, new_start
    resizeFailed = Signal(object, str) # clip, reason    
    
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def resize_clip(self, clip, new_duration, max_duration=None):
        if isinstance(clip, ClipData):
            return self._resize_clip_data(clip, new_duration, max_duration)
        elif isinstance(clip, TimelineClip):
            return self._resize_timeline_clip(clip, new_duration, max_duration)
        return False
    
    def _resize_clip_data(self, clip: ClipData, new_duration_frames: int, max_duration_frames: int = None):
        old_duration = clip.duration_frames
        
        if new_duration_frames <= 0:
            self.resizeFailed.emit(clip, f"Durée invalide: {new_duration_frames} frames (minimum: 1)")
            return False
        
        if max_duration_frames and new_duration_frames > max_duration_frames:
            self.resizeFailed.emit(clip, f"Durée trop grande: {new_duration_frames} frames (maximum: {max_duration_frames})")
            return False
        
        clip.duration_frames = new_duration_frames
        self.clipResized.emit(clip, old_duration, new_duration_frames)
        return True
    
    def _resize_timeline_clip(self, clip: TimelineClip, new_duration_sec: float, max_duration_sec: float = None):
        old_duration = clip.duration
        
        if new_duration_sec <= 0:
            self.resizeFailed.emit(clip, f"Durée invalide: {new_duration_sec:.2f}s (minimum: 0.1s)")
            return False
        
        if max_duration_sec and new_duration_sec > max_duration_sec:
            self.resizeFailed.emit(clip, f"Durée trop grande: {new_duration_sec:.2f}s (maximum: {max_duration_sec:.2f}s)")
            return False
        
        clip.end = clip.start + new_duration_sec
        clip.duration = new_duration_sec
        self.clipResized.emit(clip, int(old_duration * 24), int(new_duration_sec * 24))  # conversion en frames pour le signal
        return True
    
    def move_clip(self, clip, new_start, min_start=0):
        if isinstance(clip, ClipData):
            return self._move_clip_data(clip, new_start, min_start)
        elif isinstance(clip, TimelineClip):
            return self._move_timeline_clip(clip, new_start, min_start)
        return False
    
    def _move_clip_data(self, clip: ClipData, new_start_frame: int, min_start: int = 0):
        old_start = clip.start_frame
        
        if new_start_frame < min_start:
            self.resizeFailed.emit(clip, f"Position invalide: {new_start_frame} frames (minimum: {min_start})")
            return False
        
        clip.start_frame = new_start_frame
        self.clipMoved.emit(clip, old_start, new_start_frame)
        return True
    
    def _move_timeline_clip(self, clip: TimelineClip, new_start_sec: float, min_start_sec: float = 0):
        old_start = clip.start
        
        if new_start_sec < min_start_sec:
            self.resizeFailed.emit(clip, f"Position invalide: {new_start_sec:.2f}s (minimum: {min_start_sec:.2f}s)")
            return False
        
        duration = clip.duration
        clip.start = new_start_sec
        clip.end = new_start_sec + duration
        self.clipMoved.emit(clip, int(old_start * 24), int(new_start_sec * 24)) # Convertir en frames pour le signal
        return True
    
    def resize_clip_from_left(self, clip, new_start, max_duration=None):
        if isinstance(clip, ClipData):
            return self._resize_clip_data_from_left(clip, new_start, max_duration)
        elif isinstance(clip, TimelineClip):
            return self._resize_timeline_clip_from_left(clip, new_start, max_duration)
        return False
    
    def _resize_clip_data_from_left(self, clip: ClipData, new_start_frame: int, max_duration_frames: int = None):
        old_start = clip.start_frame
        old_duration = clip.duration_frames
        
        new_duration = old_duration - (new_start_frame - old_start)
        
        if new_duration <= 0:
            self.resizeFailed.emit(clip, "Impossible de redimensionner: durée négative")
            return False
        
        if max_duration_frames and new_duration > max_duration_frames:
            self.resizeFailed.emit(clip, f"Durée trop grande après redimensionnement: {new_duration} frames")
            return False
        
        clip.start_frame = new_start_frame
        clip.duration_frames = new_duration
        
        self.clipMoved.emit(clip, old_start, new_start_frame)
        self.clipResized.emit(clip, old_duration, new_duration)
        return True
    
    def _resize_timeline_clip_from_left(self, clip: TimelineClip, new_start_sec: float, max_duration_sec: float = None):
        old_start = clip.start
        old_duration = clip.duration
        
        new_duration = old_duration - (new_start_sec - old_start)
        
        if new_duration <= 0:
            self.resizeFailed.emit(clip, "Impossible de redimensionner: durée négative")
            return False
        
        if max_duration_sec and new_duration > max_duration_sec:
            self.resizeFailed.emit(clip, f"Durée trop grande après redimensionnement: {new_duration:.2f}s")
            return False
        
        clip.start = new_start_sec
        clip.duration = new_duration
        clip.end = new_start_sec + new_duration
        
        self.clipMoved.emit(clip, int(old_start * 24), int(new_start_sec * 24))
        self.clipResized.emit(clip, int(old_duration * 24), int(new_duration * 24))
        return True
    
    def resize_clip_from_right(self, clip, new_duration, max_duration=None):
        return self.resize_clip(clip, new_duration, max_duration)
