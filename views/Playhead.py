from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtGui import QPainter, QPen, QColor
from PySide6.QtCore import Qt

class Playhead(QWidget):
    """Widget that draws the global playhead above timelines"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(5)
        self.video_duration = 0
        self.current_time = 0
        self.timeline_widgets = []
        self.spacing = 5
        
    def set_current_time(self, time):
        """Update playback time"""
        self.current_time = time
        self.update()
        
    def set_duration(self, duration):
        """Update total duration"""
        self.video_duration = duration
        self.update()
        
    def set_timeline_widgets(self, widgets):
        """Set timeline widgets to calculate total height"""
        self.timeline_widgets = widgets
        self.update()
        
    def set_spacing(self, spacing):
        """Set spacing between timelines"""
        self.spacing = spacing
        self.update()
        
    def resizeEvent(self, event):
        """Resize widget to cover all timelines"""
        super().resizeEvent(event)
        if self.parent() and self.timeline_widgets:
            # Calculate total height of timelines + spacing
            total_height = sum(widget.height() for widget in self.timeline_widgets)
            # Add spacing between timelines (n-1 spaces for n timelines)
            if len(self.timeline_widgets) > 1:
                total_height += (len(self.timeline_widgets) - 1) * self.spacing
            # Position playhead above all timelines
            self.setGeometry(0, 0, self.parent().width(), total_height)
        
    def paintEvent(self, event):
        """Draw the global playhead"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Transparent background
        painter.fillRect(self.rect(), QColor(0, 0, 0, 0))
        
        if self.video_duration > 0:
            # Calculate playhead position
            ratio = self.current_time / self.video_duration
            x = int(ratio * self.width())
            
            # Draw vertical line across the entire widget
            painter.setPen(QPen(QColor(255, 0, 0), 2))
            painter.drawLine(x, 0, x, self.height())
            
            # Draw rectangle on first timeline (at top of widget)
            painter.setPen(QPen(QColor(255, 0, 0), 2))
            painter.setBrush(QColor(255, 0, 0))
            rect_y = 0
            painter.drawRect(x - 5, rect_y, 10, 20)
