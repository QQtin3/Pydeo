from PySide6.QtWidgets import (QWidget, QSizePolicy)
from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QPainter, QBrush, QPen, QColor


class VideoPreviewWidget(QWidget):
    currentFrame: None
    videoDuration: float
    currentTime: float
    
    """Widget to display video preview"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(400, 300)
        self.setStyleSheet("background-color: #000000;")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.currentFrame = None
        self.videoDuration = 0
        self.currentTime = 0
        
    def setFrame(self, frame: None) -> None:
        """Set the current frame to display"""
        self.currentFrame = frame
        self.update()
        
    def paintEvent(self, event: QEvent) -> None:
        """Draw the current frame"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QBrush(QColor(0, 0, 0)))
        painter.drawRect(self.rect())
        
        if self.currentFrame:
            # Here you would draw the actual video frame
            # This is a placeholder - in real implementation you'd convert the frame to QImage
            painter.setBrush(QBrush(QColor(50, 50, 50)))
            painter.drawRect(10, 10, self.width()-20, self.height()-20)
            painter.setPen(QColor(200, 200, 200))
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "Video Preview")
        
        # Draw playhead
        if self.videoDuration > 0:
            ratio = self.currentTime / self.videoDuration
            x = int(ratio * self.width())
            painter.setPen(QPen(QColor(255, 0, 0), 2))
            painter.drawLine(x, 0, x, self.height())