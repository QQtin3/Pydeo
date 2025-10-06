from PySide6.QtWidgets import QWidget
from PySide6.QtGui import Qt, QPainter, QBrush, QColor


class TimelineWidget(QWidget):
    """Custom widget for the timeline with multiple tracks"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(200)  # un peu plus haut car plusieurs pistes
        self.video_duration = 0
        self.current_time = 0
        self.dragging = False

        # Séparation des pistes
        self.tracks = {
            "video": [],
            "audio": [],
            "text": []
        }

    def addClip(self, clip, track_type="video"):
        """Add a clip to a specific track"""
        if track_type in self.tracks:
            self.tracks[track_type].append(clip)
            self.update()

    def setCurrentTime(self, time):
        """Set the current play position"""
        self.current_time = time
        self.update()

    def setCurrentTimeToCursor(self, pos_x):
        """Set the current play position to the cursor position"""
        if self.video_duration > 0:
            ratio = pos_x / self.width()
            self.set_current_time(ratio * self.video_duration)

    def setDuration(self, duration):
        """Set the total video duration"""
        self.video_duration = duration
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Background
        painter.setBrush(QBrush(QColor(40, 40, 40)))
        painter.drawRect(self.rect())

        if self.video_duration <= 0:
            return

        # Time ruler
        painter.setPen(QColor(150, 150, 150))
        for i in range(0, self.width(), 50):
            painter.drawLine(i, 0, i, 20)
            if i % 100 == 0:
                time_pos = (i / self.width()) * self.video_duration
                minutes = int(time_pos // 60)
                seconds = int(time_pos % 60)
                painter.drawText(i + 5, 15, f"{minutes}:{seconds:02d}")

        # Dessin des pistes
        track_height = 60
        track_colors = {
            "video": QColor(60, 120, 200, 200),
            "audio": QColor(200, 120, 60, 200),
            "text": QColor(120, 200, 120, 200)
        }

        for idx, (track_type, clips) in enumerate(self.tracks.items()):
            y_offset = 40 + idx * track_height

            # Ligne séparatrice
            painter.setPen(QColor(80, 80, 80))
            painter.drawLine(0, y_offset - 10, self.width(), y_offset - 10)

            # Clips
            for clip in clips:
                start_ratio = clip['start'] / self.video_duration
                end_ratio = clip['end'] / self.video_duration
                x = int(start_ratio * self.width())
                w = max(10, int((end_ratio - start_ratio) * self.width()))

                painter.setBrush(QBrush(track_colors[track_type]))
                painter.setPen(Qt.NoPen)
                painter.drawRect(x, y_offset, w, track_height - 15)

                # Label
                painter.setPen(QColor(255, 255, 255))
                painter.drawText(x + 5, y_offset + track_height // 2, clip['name'])
