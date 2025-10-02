from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QBrush, QColor, QImage, QPixmap


class VideoPreviewWidget(QWidget):
    """Widget that just draws frames (no MoviePy logic)."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(768, 432)
        self.setStyleSheet("background-color: #000;")
        self.current_pixmap = None

    def set_frame(self, frame):
        """Receive a numpy frame (from MoviePy) and convert to QPixmap."""
        if frame is None:
            self.current_pixmap = None
            self.update()
            return

        h, w, ch = frame.shape
        bytes_per_line = ch * w

        if ch == 3:
            q_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        elif ch == 4:
            q_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGBA8888)
        else:
            return

        self.current_pixmap = QPixmap.fromImage(q_image)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)

        painter.setBrush(QBrush(QColor(0, 0, 0)))
        painter.drawRect(self.rect())

        if self.current_pixmap:
            scaled = self.current_pixmap.scaled(
                self.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            x = (self.width() - scaled.width()) // 2
            y = (self.height() - scaled.height()) // 2
            painter.drawPixmap(x, y, scaled)
        else:
            painter.setPen(QColor(100, 100, 100))
            painter.drawText(self.rect(), Qt.AlignCenter, "Aucune vidéo chargée")
