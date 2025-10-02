from PySide6.QtWidgets import QWidget
from PySide6.QtGui import Qt, QPainter, QBrush, QPen, QColor

from model.TimelineClip import TimelineClip

class TimelineWidget(QWidget):
    videoDuration: int
    currentTime: int
    dragging: bool
    clips: list[TimelineClip]
    
    """Custom widget for the timeline"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(100)
        self.videoDuration = 0
        self.c = 0
        self.dragging = False
        self.clips = []  # List of clips to display on timeline
        
    def addClip(self, clip: TimelineClip) -> None:
        """Add a clip to the timeline"""
        self.clips.append(clip)
        self.update()


    def pressMouseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton :
            self.dragging = True
            self.setCurrentTimeToCursor(event.position().x())

    def releaseMouseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton :
            self.dragging = False
            self.setCurrentTimeToCursor(event.position().x())

    def moveMouseEvent(self, event):
        if self.dragging :
            self.setCurrentTimeToCursor(event.position().x())

        
    def setCurrentTime(self, time):
        """Set the current play position"""
        self.currentTime = time
        self.update()

    def setCurrentTimeToCursor(self, pos_x):
        """Set the current play position to the cursor position"""
        if self.videoDuration > 0:
            ratio = pos_x / self.width()
            self.setCurrentTime(ratio * self.videoDuration)
        
    def setDuration(self, duration):
        """Set the total video duration"""
        self.videoDuration = duration
        self.update()
        
    def paintEvent(self, event):
        """Draw the timeline"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Background
        painter.setBrush(QBrush(QColor(40, 40, 40)))
        painter.drawRect(self.rect())
        
        # Time ruler
        painter.setPen(QColor(150, 150, 150))
        for i in range(0, self.width(), 50):
            painter.drawLine(i, 0, i, 20)
            if i % 100 == 0 and self.videoDuration > 0:
                time_pos = (i / self.width()) * self.videoDuration
                minutes = int(time_pos // 60)
                seconds = int(time_pos % 60)
                painter.drawText(i + 5, 15, f"{minutes}:{seconds:02d}")
        
        # Clips on timeline
        clip_height = 60
        y = (self.height() - clip_height) // 2
        for clip in self.clips:
            if self.videoDuration > 0:
                start_ratio = clip.start / self.videoDuration
                end_ratio = clip.end / self.videoDuration
                x = int(start_ratio * self.width())
                w = max(10, int((end_ratio - start_ratio) * self.width()))
                
                # Draw clip rectangle
                painter.setBrush(QBrush(QColor(60, 120, 200, 200)))
                painter.drawRect(x, y, w, clip_height)
                
                # Draw clip label
                painter.setPen(QColor(255, 255, 255))
                text = clip.name
                text_rect = painter.fontMetrics().boundingRect(text)
                if text_rect.width() < w - 10:
                    painter.drawText(x + 5, y + clip_height // 2 + 5, text)
