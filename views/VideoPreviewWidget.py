from PySide6.QtWidgets import QWidget, QSizePolicy
from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QPainter, QBrush, QColor, QImage, QPixmap


class VideoPreviewWidget(QWidget):
    currentFrame: None
    currentPixmap: QPixmap | None
    videoDuration: float
    currentTime: float
    
    """Widget to display video preview"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(768, 432)
        self.setStyleSheet("background-color: #000;")
        self.currentPixmap = None

    def set_frame(self, frame):
        """Receive a numpy frame (from MoviePy) and convert to QPixmap."""
        if frame is None:
            self.currentPixmap = None
            self.update()
            return

        h, w, ch = frame.shape
        bytes_per_line = ch * w

        if ch == 3:
            q_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        elif ch == 4:
            q_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format.Format_RGBA8888)
        else:
            return

        self.currentPixmap = QPixmap.fromImage(q_image)
        self.update()
        
    def paintEvent(self, event: QEvent) -> None:
        """Draw the current frame"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        painter.setBrush(QBrush(QColor(0, 0, 0)))
        painter.drawRect(self.rect())

        if self.currentPixmap:
            scaled = self.currentPixmap.scaled(
                self.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            x = (self.width() - scaled.width()) // 2
            y = (self.height() - scaled.height()) // 2
            painter.drawPixmap(x, y, scaled)
        else:
            painter.setPen(QColor(100, 100, 100))
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "Aucune vidéo chargée")
