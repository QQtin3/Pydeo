from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor, QMouseEvent
from PySide6.QtCore import Signal

class TimelineWidget(QWidget):
    """Custom widget for a single timeline with multiple tracks (no time scale)."""

    currentTimeChanged = Signal(float)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(120)
        self.video_duration = 0
        self.current_time = 0

        self.zoom_factor = 1.0
        self.scroll_offset = 0.0

        # Tracks
        self.tracks = {
            "video": [],
            "audio": [],
            "text": []
        }

        # Colors
        self.track_colors = {
            "video": QColor(60, 120, 200, 200),
            "audio": QColor(200, 120, 60, 200),
            "text": QColor(120, 200, 120, 200)
        }

    # ==========================
    # Gestion des clips & temps
    # ==========================
    def addClip(self, clip, track_type="video"):
        """Add a clip to a specific track with validation."""
        if track_type in self.tracks and isinstance(clip, dict) and all(k in clip for k in ['start', 'end', 'name']):
            if 0 <= clip['start'] <= clip['end'] <= self.video_duration:
                self.tracks[track_type].append(clip)
                self.update()
            else:
                print(f"Invalid clip times: {clip}")
        else:
            print(f"Invalid track type {track_type} or clip format: {clip}")

    def setCurrentTime(self, time):
        """Set the current play position."""
        self.current_time = max(0, min(time, self.video_duration))
        self.currentTimeChanged.emit(self.current_time)
        self.update()

    def setDuration(self, duration):
        """Set the total video duration."""
        self.video_duration = duration
        self.update()

    # ==========================
    # Conversion temps <-> X
    # ==========================
    def timeToX(self, t, zoom_factor, scroll_offset):
        if self.width() == 0:
            return 0
        visible_duration = self.video_duration / zoom_factor
        start_time = scroll_offset
        return int(((t - start_time) / visible_duration) * self.width())

    def xToTime(self, x, zoom_factor, scroll_offset):
        if self.width() == 0:
            return 0
        visible_duration = self.video_duration / zoom_factor
        start_time = scroll_offset
        return (x / self.width()) * visible_duration + start_time

    # ==========================
    # Zoom/Scroll
    # ==========================
    def setZoomAndScroll(self, zoom_factor, scroll_offset):
        self.zoom_factor = zoom_factor
        self.scroll_offset = scroll_offset
        self.update()

    # ==========================
    # Rendu
    # ==========================
    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.rect()
        painter.fillRect(rect, QColor("#1e1e1e"))

        if self.video_duration <= 0:
            return

        visible_duration = self.video_duration / self.zoom_factor
        visible_start = self.scroll_offset
        visible_end = visible_start + visible_duration
        total_pixels = rect.width()
        pixels_per_second = total_pixels / visible_duration

        # Dessin des clips (barres colorées par piste)
        track_height = rect.height() // len(self.tracks)
        for i, (track_type, clips) in enumerate(self.tracks.items()):
            y = i * track_height
            color = self.track_colors[track_type]
            for clip in clips:
                if clip["end"] < visible_start or clip["start"] > visible_end:
                    continue  # clip hors champ
                x1 = (clip["start"] - visible_start) * pixels_per_second
                x2 = (clip["end"] - visible_start) * pixels_per_second
                painter.fillRect(int(x1), y, int(x2 - x1), track_height - 2, color)

        # Curseur de lecture (optionnel : rouge)
        if visible_start <= self.current_time <= visible_end:
            x = (self.current_time - visible_start) * pixels_per_second
            painter.setPen(QColor("red"))
            painter.drawLine(int(x), 0, int(x), rect.height())
