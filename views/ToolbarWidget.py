from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QHBoxLayout, QToolButton


class ToolbarWidget(QWidget):
    """Toolbar hosting undo/redo, tool mode selection and zoom controls.

    Exposes signals to let the parent window respond to actions without
    coupling to implementation details.
    """

    undoRequested = Signal()
    redoRequested = Signal()
    zoomInRequested = Signal()
    zoomOutRequested = Signal()
    modeChanged = Signal(str)  # 'move' | 'cut' | 'split' | 'select'

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setStyleSheet("background-color: #3a3a3a; border-top: 1px solid #555; border-bottom: 1px solid #555;")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 2, 5, 2)
        layout.setSpacing(8)

        # Undo / Redo
        self.undoBtn = QToolButton()
        self.undoBtn.setText("↩")
        self.undoBtn.setToolTip("Annuler (Ctrl+Z)")
        self.undoBtn.setFixedSize(24, 24)
        self.undoBtn.clicked.connect(self.undoRequested.emit)
        layout.addWidget(self.undoBtn)

        self.redoBtn = QToolButton()
        self.redoBtn.setText("↪")
        self.redoBtn.setToolTip("Refaire (Ctrl+Y)")
        self.redoBtn.setFixedSize(24, 24)
        self.redoBtn.clicked.connect(self.redoRequested.emit)
        layout.addWidget(self.redoBtn)

        layout.addSpacing(15)

        # Editing tools (checkable)
        self.moveBtn = QToolButton()
        self.moveBtn.setCheckable(True)
        self.moveBtn.setChecked(True)
        self.moveBtn.setText("⤢")
        self.moveBtn.setToolTip("Déplacer")
        self.moveBtn.setFixedSize(24, 24)
        self.moveBtn.clicked.connect(lambda: self._setMode('move'))
        layout.addWidget(self.moveBtn)

        self.cutBtn = QToolButton()
        self.cutBtn.setCheckable(True)
        self.cutBtn.setText("✂")
        self.cutBtn.setToolTip("Couper")
        self.cutBtn.setFixedSize(24, 24)
        self.cutBtn.clicked.connect(lambda: self._setMode('cut'))
        layout.addWidget(self.cutBtn)

        self.splitBtn = QToolButton()
        self.splitBtn.setCheckable(True)
        self.splitBtn.setText("⌬")
        self.splitBtn.setToolTip("Scinder")
        self.splitBtn.setFixedSize(24, 24)
        self.splitBtn.clicked.connect(lambda: self._setMode('split'))
        layout.addWidget(self.splitBtn)

        self.selectBtn = QToolButton()
        self.selectBtn.setCheckable(True)
        self.selectBtn.setText("☐")
        self.selectBtn.setToolTip("Sélectionner")
        self.selectBtn.setFixedSize(24, 24)
        self.selectBtn.clicked.connect(lambda: self._setMode('select'))
        layout.addWidget(self.selectBtn)

        layout.addSpacing(15)

        # Zoom
        self.zoomInBtn = QToolButton()
        self.zoomInBtn.setText("+")
        self.zoomInBtn.setToolTip("Zoom avant")
        self.zoomInBtn.setFixedSize(24, 24)
        self.zoomInBtn.clicked.connect(self.zoomInRequested.emit)
        layout.addWidget(self.zoomInBtn)

        self.zoomOutBtn = QToolButton()
        self.zoomOutBtn.setText("-")
        self.zoomOutBtn.setToolTip("Zoom arrière")
        self.zoomOutBtn.setFixedSize(24, 24)
        self.zoomOutBtn.clicked.connect(self.zoomOutRequested.emit)
        layout.addWidget(self.zoomOutBtn)

        layout.addStretch()

        # Current mode string
        self.currentMode = 'move'

    # ----- Public API -----------------------------------------------------
    def setMode(self, mode: str) -> None:
        """Set current mode programmatically and update UI state."""
        self._updateChecks(mode)
        self.currentMode = mode

    # ----- Internal helpers ----------------------------------------------
    def _setMode(self, mode: str) -> None:
        self._updateChecks(mode)
        self.currentMode = mode
        self.modeChanged.emit(mode)

    def _updateChecks(self, mode: str) -> None:
        # Uncheck all
        self.moveBtn.setChecked(False)
        self.cutBtn.setChecked(False)
        self.splitBtn.setChecked(False)
        self.selectBtn.setChecked(False)
        # Check selected
        if mode == 'move':
            self.moveBtn.setChecked(True)
        elif mode == 'cut':
            self.cutBtn.setChecked(True)
        elif mode == 'split':
            self.splitBtn.setChecked(True)
        elif mode == 'select':
            self.selectBtn.setChecked(True)
