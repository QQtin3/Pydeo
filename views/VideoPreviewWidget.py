from PySide6.QtWidgets import (QWidget, QSizePolicy)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QBrush, QPen, QColor


class VideoPreviewWidget(QWidget):
    """Widget to display video preview"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(400, 300)
        self.setStyleSheet("background-color: #000000;")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.current_frame = None
        self.video_duration = 0
        self.current_time = 0
        
    def set_frame(self, frame):
        """Set the current frame to display"""
        self.current_frame = frame
        self.update()
        
    def paintEvent(self, event):
        """Draw the current frame"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(QColor(0, 0, 0)))
        painter.drawRect(self.rect())
        
        if self.current_frame:
            # Here you would draw the actual video frame
            # This is a placeholder - in real implementation you'd convert the frame to QImage
            painter.setBrush(QBrush(QColor(50, 50, 50)))
            painter.drawRect(10, 10, self.width()-20, self.height()-20)
            painter.setPen(QColor(200, 200, 200))
            painter.drawText(self.rect(), Qt.AlignCenter, "Video Preview")
        
        # Draw playhead
        if self.video_duration > 0:
            ratio = self.current_time / self.video_duration
            x = int(ratio * self.width())
            painter.setPen(QPen(QColor(255, 0, 0), 2))
            painter.drawLine(x, 0, x, self.height())