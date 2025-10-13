from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QSlider, QLabel


class PlaybackControlsWidget(QWidget):
    """Compact widget hosting transport controls (play/pause, position slider, time label).

    Signals
    -------
    playToggled(bool)
        Emitted when user clicks the play button. The boolean indicates desired play state.
    sliderPressed()
        Emitted when user starts dragging the position slider.
    sliderMoved(int)
        Emitted while the slider is being dragged (value in milliseconds).
    sliderReleased()
        Emitted when user releases the slider handle.
    """

    playToggled = Signal(bool)
    sliderPressed = Signal()
    sliderMoved = Signal(int)
    sliderReleased = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        # UI elements
        self.playBtn = QPushButton("▶")
        self.playBtn.setFixedSize(30, 30)

        self.positionSlider = QSlider(Qt.Orientation.Horizontal)
        self.positionSlider.setEnabled(False)

        self.timeLabel = QLabel("00:00 / 00:00")

        # Layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)
        layout.addWidget(self.playBtn)
        layout.addWidget(self.positionSlider, 1)
        layout.addWidget(self.timeLabel)

        # Wire signals to re-emit
        self.playBtn.clicked.connect(self._onPlayClicked)
        self.positionSlider.sliderPressed.connect(self.sliderPressed.emit)
        self.positionSlider.sliderMoved.connect(self.sliderMoved.emit)
        self.positionSlider.sliderReleased.connect(self.sliderReleased.emit)

    # ----- Public API -----------------------------------------------------
    def setIsPlaying(self, isPlaying: bool) -> None:
        """Update play button icon based on current state."""
        self.playBtn.setText("⏸" if isPlaying else "▶")

    def setDurationMs(self, durationMs: int) -> None:
        """Enable slider and set its range according to duration in ms."""
        self.positionSlider.setEnabled(durationMs > 0)
        if durationMs > 0:
            self.positionSlider.setRange(0, durationMs)

    def setPositionMs(self, positionMs: int) -> None:
        """Update slider position without emitting moved signals."""
        self.positionSlider.blockSignals(True)
        self.positionSlider.setValue(positionMs)
        self.positionSlider.blockSignals(False)

    def setTimeLabel(self, currentSec: float, totalSec: float) -> None:
        """Update the time display label (mm:ss / mm:ss)."""
        def fmt(sec: float) -> str:
            sec = max(0.0, float(sec))
            m = int(sec) // 60
            s = int(sec) % 60
            return f"{m:02d}:{s:02d}"

        self.timeLabel.setText(f"{fmt(currentSec)} / {fmt(totalSec)}")

    # ----- Internal handlers ---------------------------------------------
    def _onPlayClicked(self) -> None:
        # Toggle expected state based on current label text.
        wantPlay = self.playBtn.text() == "▶"
        self.playToggled.emit(wantPlay)
