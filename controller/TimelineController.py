from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtGui import Qt, QPainter, QBrush, QColor, QWheelEvent, QMouseEvent
from views.TimelineWidget import TimelineWidget
from views.PlayHead import PlayHead

class TimelineController(QWidget):
    """Controller managing a list of timelines, shared zoom, scroll, and time scale."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.video_duration = 0
        self.current_time = 0
        self.zoom_factor = 1.0   # 1.0 = full video visible
        self.scroll_offset = 0.0 # in seconds

        # Interaction
        self.dragging = False
        self.last_mouse_x = None

        # List of timelines
        self.timelines = []

        # Layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Playhead widget (global)
        self.playhead = PlayHead(self)
        self.layout.addWidget(self.playhead)

        # Time scale widget
        self.time_scale_widget = QWidget(self)
        self.time_scale_widget.setFixedHeight(40)
        self.time_scale_widget.paintEvent = self.paint_time_scale
        self.layout.addWidget(self.time_scale_widget)

        # Container for timelines
        self.timelines_container = QWidget(self)
        self.timelines_layout = QVBoxLayout(self.timelines_container)
        self.timelines_layout.setContentsMargins(0, 0, 0, 0)
        self.timelines_layout.setSpacing(5)  # Match PlayHead spacing
        self.layout.addWidget(self.timelines_container)

    def addTimeline(self):
        """Add a new unique timeline."""
        timeline = TimelineWidget(self.timelines_container)
        timeline.setDuration(self.video_duration)
        timeline.currentTimeChanged.connect(self.sync_current_time)
        self.timelines.append(timeline)
        self.timelines_layout.addWidget(timeline)
        self.playhead.setTimelineWidgets(self.timelines)
        self.playhead.setDuration(self.video_duration)
        self.update_all()
        return timeline

    def setDuration(self, duration):
        """Set the total video duration for all timelines and playhead."""
        self.video_duration = duration
        self.playhead.setDuration(duration)
        for timeline in self.timelines:
            timeline.setDuration(duration)
        self.update_all()

    def sync_current_time(self, time):
        """Sync current time across all timelines and playhead."""
        self.current_time = time
        self.playhead.setCurrentTime(time)
        for timeline in self.timelines:
            timeline.current_time = time  # Direct set to avoid signal loop
        self.update_all()

    # ==========================
    # Contrôles Zoom & Scroll
    # ==========================
    def zoomIn(self):
        self.zoom_factor = min(self.zoom_factor * 1.25, 50.0)
        self.update_all()

    def zoomOut(self):
        self.zoom_factor = max(self.zoom_factor / 1.25, 1.0)
        self.update_all()

    def scrollLeft(self):
        visible_duration = self.video_duration / self.zoom_factor
        self.scroll_offset = max(0, self.scroll_offset - visible_duration * 0.1)
        self.update_all()

    def scrollRight(self):
        visible_duration = self.video_duration / self.zoom_factor
        max_offset = max(0, self.video_duration - visible_duration)
        self.scroll_offset = min(max_offset, self.scroll_offset + visible_duration * 0.1)
        self.update_all()

    # ==========================
    # Événements souris
    # ==========================
    def wheelEvent(self, event: QWheelEvent):
        """Wheel = zoom (Ctrl) or scroll."""
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            if event.angleDelta().y() > 0:
                self.zoomIn()
            else:
                self.zoomOut()
        else:
            if event.angleDelta().y() > 0:
                self.scrollLeft()
            else:
                self.scrollRight()

    def mousePressEvent(self, event: QMouseEvent):
        """Drag for pan, left-click for playhead."""
        if event.button() == Qt.MouseButton.MiddleButton:
            self.dragging = True
            self.last_mouse_x = event.x()
        elif event.button() == Qt.MouseButton.LeftButton:
            pos = self.timelines_container.mapFromParent(event.pos())
            for timeline in self.timelines:
                if timeline.underMouse():
                    local_x = timeline.mapFromParent(pos).x()
                    time = timeline.xToTime(local_x, self.zoom_factor, self.scroll_offset)
                    self.sync_current_time(time)
                    break
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.dragging and self.last_mouse_x is not None:
            dx = event.x() - self.last_mouse_x
            visible_duration = self.video_duration / self.zoom_factor
            seconds_per_px = visible_duration / self.width() if self.width() > 0 else 0
            self.scroll_offset = max(0, self.scroll_offset - dx * seconds_per_px)
            max_offset = max(0, self.video_duration - visible_duration)
            self.scroll_offset = min(self.scroll_offset, max_offset)
            self.last_mouse_x = event.x()
            self.update_all()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.MiddleButton:
            self.dragging = False
            self.last_mouse_x = None

    # ==========================
    # Rendu de la graduation
    # ==========================
    def paint_time_scale(self, event):
        painter = QPainter(self.time_scale_widget)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.TextAntialiasing)

        # Background
        painter.setBrush(QBrush(QColor(40, 40, 40)))
        painter.drawRect(self.time_scale_widget.rect())

        if self.video_duration <= 0:
            return

        # Graduation temporelle
        painter.setPen(QColor(150, 150, 150))
        step_px = 50

        for i in range(0, self.width(), step_px):
            t = self.xToTime(i)
            if t < 0 or t > self.video_duration:
                continue

            painter.drawLine(i, 20, i, 40)
            if i % 100 == 0:
                minutes = int(t // 60)
                seconds = int(t % 60)
                painter.drawText(i + 5, 15, f"{minutes}:{seconds:02d}")

    def xToTime(self, x):
        """Convert X to time (shared)."""
        if self.width() == 0:
            return 0
        visible_duration = self.video_duration / self.zoom_factor
        start_time = self.scroll_offset
        return (x / self.width()) * visible_duration + start_time

    def update_all(self):
        """Update playhead, time scale, and all timelines."""
        self.playhead.update()
        self.time_scale_widget.update()
        for timeline in self.timelines:
            timeline.paintEvent(None)
            timeline.setZoomAndScroll(self.zoom_factor, self.scroll_offset)
            timeline.update()