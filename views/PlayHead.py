from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QColor, QResizeEvent

from views.TimelineWidget import TimelineWidget

class PlayHead(QWidget):
    """Widget that draws the global play head above timelines"""
    
    videoDuration: float
    currentTime: float
    timelineWidgets: list[TimelineWidget]
    spacing: int

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(5)
        self.videoDuration = 0
        self.currentTime = 0
        self.timelineWidgets = []
        self.spacing = 5
        
    def setCurrentTime(self, time: float) -> None:
        """Update playback time"""
        self.currentTime = time
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
        
    def resizeEvent(self, event: QResizeEvent) -> None:
        """Resize widget to cover all timelines"""
        super().resizeEvent(event)
        if self.parent() and self.timelineWidgets:
            # Calculate total height of timelines + spacing
            total_height = sum(widget.height() for widget in self.timelineWidgets)
            # Add spacing between timelines (n-1 spaces for n timelines)
            if len(self.timelineWidgets) > 1:
                total_height += (len(self.timelineWidgets) - 1) * self.spacing
            # Position playhead above all timelines
            self.setGeometry(0, 0, self.parent().width(), total_height)
        
    def paintEvent(self, event):
        """Draw the global playhead"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Transparent background
        painter.fillRect(self.rect(), QColor(0, 0, 0, 0))
        
        if self.videoDuration > 0:
            # Calculate playhead position
            ratio = self.currentTime / self.videoDuration
            x = int(ratio * self.width())
            
            # Draw vertical line across the entire widget
            painter.setPen(QPen(QColor(255, 0, 0), 2))
            painter.drawLine(x, 0, x, self.height())
            
            # Draw rectangle on first timeline (at top of widget)
            painter.setPen(QPen(QColor(255, 0, 0), 2))
            painter.setBrush(QColor(255, 0, 0))
            rect_y = 0
            painter.drawRect(x - 5, rect_y, 10, 20)
