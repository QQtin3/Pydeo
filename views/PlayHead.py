from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QColor, QResizeEvent
from views.TimelineWidget import TimelineWidget

class PlayHead(QWidget):
    """Widget that draws the global play head above timelines"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(5)
        self.videoDuration = 0
        self.currentTime = 0
        self.timelineWidgets = []
        self.spacing = 5
        self.zoom_factor = 1.0
        self.scroll_offset = 0.0

    def setCurrentTime(self, time: float) -> None:
        """Update playback time"""
        self.currentTime = max(0, min(time, self.videoDuration))
        self.update()

    def setDuration(self, duration: int) -> None:
        """Update total duration"""
        self.videoDuration = duration
        self.update()

    def setTimelineWidgets(self, widgets: list[TimelineWidget]) -> None:
        """Set timeline widgets to calculate total height"""
        self.timelineWidgets = widgets
        self.update()

    def setSpacing(self, spacing: int) -> None:
        """Set spacing between timelines"""
        self.spacing = spacing
        self.update()

    def setZoomAndScroll(self, zoom_factor: float, scroll_offset: float) -> None:
        """Set zoom and scroll parameters"""
        self.zoom_factor = zoom_factor
        self.scroll_offset = scroll_offset
        self.update()

    def resizeEvent(self, event: QResizeEvent) -> None:
        """Resize widget to cover all timelines"""
        super().resizeEvent(event)
        if self.parent() and self.timelineWidgets:
            total_height = sum(widget.height() for widget in self.timelineWidgets)
            if len(self.timelineWidgets) > 1:
                total_height += (len(self.timelineWidgets) - 1) * self.spacing
            self.setGeometry(0, 0, self.parent().width(), total_height)

    def paintEvent(self, event):
        """Draw the global playhead"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Transparent background
        painter.fillRect(self.rect(), QColor(0, 0, 0, 0))

        if self.videoDuration > 0 and self.timelineWidgets:
            # Use timeline's timeToX with zoom and scroll
            x = self.timelineWidgets[0].timeToX(self.currentTime, self.zoom_factor, self.scroll_offset)

            # Draw vertical line across the entire widget
            painter.setPen(QPen(QColor(255, 0, 0), 2))
            painter.drawLine(x, 0, x, self.height())

            # Draw rectangle indicator at top
            painter.setPen(QPen(QColor(255, 0, 0), 2))
            painter.setBrush(QColor(255, 0, 0))
            painter.drawRect(x - 5, 0, 10, 20)