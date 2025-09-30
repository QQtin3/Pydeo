from PySide6.QtWidgets import QWidget
from PySide6.QtGui import Qt, QPainter, QBrush, QPen, QColor

class TimelineWidget(QWidget):
    """Custom widget for the timeline"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(100)
        self.video_duration = 0
        self.current_time = 0
        self.dragging = False
        self.clips = []  # List of clips to display on timeline
        
    def add_clip(self, clip):
        """Add a clip to the timeline"""
        self.clips.append(clip)
        self.update()


    def press_mouse_event(self, event):
        if event.button() == Qt.LeftButton :
            self.dragging = True
            self.set_current_time_to_cursor(event.position().x())

    def release_mouse_event(self, event):
        if event.button() == Qt.LeftButton :
            self.dragging = False
            self.set_current_time_to_cursor(event.position().x())

    def move_mouse_event(self, event):
        if self.dragging :
            self.set_current_time_to_cursor(event.position().x())

        
    def set_current_time(self, time):
        """Set the current play position"""
        self.current_time = time
        self.update()

    def set_current_time_to_cursor(self, pos_x):
        """Set the current play position to the cursor position"""
        if self.video_duration > 0:
            ratio = pos_x / self.width()
            self.set_current_time(ratio * self.video_duration)
        
    def set_duration(self, duration):
        """Set the total video duration"""
        self.video_duration = duration
        self.update()
        
    def paintEvent(self, event):
        """Draw the timeline"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Background
        painter.setBrush(QBrush(QColor(40, 40, 40)))
        painter.drawRect(self.rect())
        
        # Time ruler
        painter.setPen(QColor(150, 150, 150))
        for i in range(0, self.width(), 50):
            painter.drawLine(i, 0, i, 20)
            if i % 100 == 0 and self.video_duration > 0:
                time_pos = (i / self.width()) * self.video_duration
                minutes = int(time_pos // 60)
                seconds = int(time_pos % 60)
                painter.drawText(i + 5, 15, f"{minutes}:{seconds:02d}")
        
        # Clips on timeline
        clip_height = 60
        y = (self.height() - clip_height) // 2
        for clip in self.clips:
            if self.video_duration > 0:
                start_ratio = clip['start'] / self.video_duration
                end_ratio = clip['end'] / self.video_duration
                x = int(start_ratio * self.width())
                w = max(10, int((end_ratio - start_ratio) * self.width()))
                
                # Draw clip rectangle
                painter.setBrush(QBrush(QColor(60, 120, 200, 200)))
                painter.drawRect(x, y, w, clip_height)
                
                # Draw clip label
                painter.setPen(QColor(255, 255, 255))
                text = clip['name']
                text_rect = painter.fontMetrics().boundingRect(text)
                if text_rect.width() < w - 10:
                    painter.drawText(x + 5, y + clip_height // 2 + 5, text)
        
        # Playhead
        if self.video_duration > 0:
            ratio = self.current_time / self.video_duration
            x = int(ratio * self.width())
            painter.setPen(QPen(QColor(255, 0, 0), 2))
            painter.drawLine(x, 0, x, self.height())
            painter.setBrush(QBrush(QColor(255, 0, 0)))
            painter.drawRect(x - 5, 0, 10, 20)