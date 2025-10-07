from PySide6.QtWidgets import QWidget
from PySide6.QtGui import Qt, QPainter, QBrush, QColor, QMouseEvent, QFontMetrics
from PySide6.QtCore import Signal

class TimelineWidget(QWidget):
    """Custom widget for a single timeline with multiple tracks."""

    currentTimeChanged = Signal(float)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(200)
        self.video_duration = 0
        self.current_time = 0

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

    def setCurrentTimeToCursor(self, pos_x, zoom_factor, scroll_offset):
        """Set the current play position to the cursor position."""
        if self.video_duration > 0:
            self.setCurrentTime(self.xToTime(pos_x, zoom_factor, scroll_offset))

    def setDuration(self, duration):
        """Set the total video duration."""
        self.video_duration = duration
        self.update()

    # ==========================
    # Conversion temps <-> X
    # ==========================
    def timeToX(self, t, zoom_factor, scroll_offset):
        """Convert time (s) to position X (px)."""
        if self.width() == 0:
            return 0
        visible_duration = self.video_duration / zoom_factor
        start_time = scroll_offset
        return int(((t - start_time) / visible_duration) * self.width())

    def xToTime(self, x, zoom_factor, scroll_offset):
        """Convert position X (px) to time (s)."""
        if self.width() == 0:
            return 0
        visible_duration = self.video_duration / zoom_factor
        start_time = scroll_offset
        return (x / self.width()) * visible_duration + start_time

    # ==========================
    # Événements souris
    # ==========================
    def mousePressEvent(self, event: QMouseEvent):
        """Handle mouse press for playhead setting (delegated to controller)."""
        super().mousePressEvent(event)

    # ==========================
    # Rendu
    # ==========================
    def paintEvent(self, event, zoom_factor, scroll_offset):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.TextAntialiasing)

        # Background
        painter.setBrush(QBrush(QColor(40, 40, 40)))
        painter.drawRect(self.rect())

        if self.video_duration <= 0:
            return

        # Visible range for optimization
        visible_duration = self.video_duration / zoom_factor
        visible_start = scroll_offset
        visible_end = visible_start + visible_duration

        # Dynamic track height
        track_height = (self.height()) // len(self.tracks) if self.tracks else 60

        for idx, (track_type, clips) in enumerate(self.tracks.items()):
            y_offset = idx * track_height

            # Ligne séparatrice
            painter.setPen(QColor(80, 80, 80))
            painter.drawLine(0, y_offset - 10, self.width(), y_offset - 10)

            # Clips (optimized)
            for clip in clips:
                if clip['end'] >= visible_start and clip['start'] <= visible_end:
                    start_x = self.timeToX(clip['start'], zoom_factor, scroll_offset)
                    end_x = self.timeToX(clip['end'], zoom_factor, scroll_offset)
                    w = max(10, end_x - start_x)

                    painter.setBrush(QBrush(self.track_colors[track_type]))
                    painter.setPen(Qt.NoPen)
                    painter.drawRoundedRect(start_x, y_offset, w, track_height - 15, 5, 5)

                    # Label with truncation
                    painter.setPen(QColor(255, 255, 255))
                    font_metrics = QFontMetrics(painter.font())
                    truncated_name = font_metrics.elidedText(clip['name'], Qt.ElideRight, w - 10)
                    painter.drawText(start_x + 5, y_offset + track_height // 2, truncated_name)