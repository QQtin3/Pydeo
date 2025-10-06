from PySide6.QtWidgets import QWidget
from PySide6.QtGui import Qt, QPainter, QBrush, QColor


class TimelineWidget(QWidget):
    """Custom widget for the timeline with multiple tracks"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(200)
        self.video_duration = 0
        self.current_time = 0

        # Interaction
        self.dragging = False

        # Zoom & Scroll
        self.zoom_factor = 1.0   # 1.0 = toute la vidéo visible
        self.scroll_offset = 0.0 # en secondes

        # Séparation des pistes
        self.tracks = {
            "video": [],
            "audio": [],
            "text": []
        }

    # ==========================
    # Gestion des clips & temps
    # ==========================
    def addClip(self, clip, track_type="video"):
        """Add a clip to a specific track"""
        if track_type in self.tracks:
            self.tracks[track_type].append(clip)
            self.update()

    def setCurrentTime(self, time):
        """Set the current play position"""
        self.current_time = max(0, min(time, self.video_duration))
        self.update()

    def setCurrentTimeToCursor(self, pos_x):
        """Set the current play position to the cursor position"""
        if self.video_duration > 0:
            self.setCurrentTime(self.xToTime(pos_x))

    def setDuration(self, duration):
        """Set the total video duration"""
        self.video_duration = duration
        self.update()

    # ==========================
    # Conversion temps <-> X
    # ==========================
    def timeToX(self, t):
        """Convertir un temps (s) en position X (px)"""
        visible_duration = self.video_duration / self.zoom_factor
        start_time = self.scroll_offset
        return int(((t - start_time) / visible_duration) * self.width())

    def xToTime(self, x):
        """Convertir une position X (px) en temps (s)"""
        visible_duration = self.video_duration / self.zoom_factor
        start_time = self.scroll_offset
        return (x / self.width()) * visible_duration + start_time

    # ==========================
    # Rendu
    # ==========================
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.TextAntialiasing)

        # Background
        painter.setBrush(QBrush(QColor(40, 40, 40)))
        painter.drawRect(self.rect())

        if self.video_duration <= 0:
            return

        # Graduation temporelle
        painter.setPen(QColor(150, 150, 150))
        step_px = 50  # tous les 50px

        for i in range(0, self.width(), step_px):
            t = self.xToTime(i)
            if t < 0 or t > self.video_duration:
                continue

            painter.drawLine(i, 0, i, 20)
            if i % 100 == 0:  # un texte toutes les 100px
                minutes = int(t // 60)
                seconds = int(t % 60)
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
                start_x = self.timeToX(clip['start'])
                end_x = self.timeToX(clip['end'])
                w = max(10, end_x - start_x)

                painter.setBrush(QBrush(track_colors[track_type]))
                painter.setPen(Qt.NoPen)
                painter.drawRoundedRect(start_x, y_offset, w, track_height - 15, 5, 5)

                # Label
                painter.setPen(QColor(255, 255, 255))
                painter.drawText(start_x + 5, y_offset + track_height // 2, clip['name'])
