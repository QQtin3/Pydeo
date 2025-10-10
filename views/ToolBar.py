# Toolbar.py
from PySide6.QtWidgets import QWidget, QHBoxLayout, QToolButton

class Toolbar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Configure l'interface de la barre d'outils"""
        self.setStyleSheet("background-color: #3a3a3a; border-top: 1px solid #555; border-bottom: 1px solid #555;")
        toolbar_layout = QHBoxLayout(self)
        toolbar_layout.setContentsMargins(5, 2, 5, 2)
        toolbar_layout.setSpacing(8)
        
        # Undo/Redo
        undo_btn = QToolButton()
        undo_btn.setText("↩")
        undo_btn.setToolTip("Annuler (Ctrl+Z)")
        undo_btn.setFixedSize(24, 24)
        toolbar_layout.addWidget(undo_btn)
        
        redo_btn = QToolButton()
        redo_btn.setText("↪")
        redo_btn.setToolTip("Refaire (Ctrl+Y)")
        redo_btn.setFixedSize(24, 24)
        toolbar_layout.addWidget(redo_btn)
        
        toolbar_layout.addSpacing(15)
        
        # Outils d'édition
        self.move_btn = QToolButton()
        self.move_btn.setCheckable(True)
        self.move_btn.setChecked(True)
        self.move_btn.setText("⤢")
        self.move_btn.setToolTip("Déplacer")
        self.move_btn.setFixedSize(24, 24)
        toolbar_layout.addWidget(self.move_btn)
        
        self.cut_btn = QToolButton()
        self.cut_btn.setCheckable(True)
        self.cut_btn.setText("✂")
        self.cut_btn.setToolTip("Couper")
        self.cut_btn.setFixedSize(24, 24)
        toolbar_layout.addWidget(self.cut_btn)
        
        self.split_btn = QToolButton()
        self.split_btn.setCheckable(True)
        self.split_btn.setText("⌬")
        self.split_btn.setToolTip("Scinder")
        self.split_btn.setFixedSize(24, 24)
        toolbar_layout.addWidget(self.split_btn)
        
        self.select_btn = QToolButton()
        self.select_btn.setCheckable(True)
        self.select_btn.setText("☐")
        self.select_btn.setToolTip("Sélectionner")
        self.select_btn.setFixedSize(24, 24)
        toolbar_layout.addWidget(self.select_btn)
        
        toolbar_layout.addSpacing(15)
        
        # Contrôles de zoom
        zoom_in_btn = QToolButton()
        zoom_in_btn.setText("+")
        zoom_in_btn.setToolTip("Zoom avant")
        zoom_in_btn.setFixedSize(24, 24)
        toolbar_layout.addWidget(zoom_in_btn)
        
        zoom_out_btn = QToolButton()
        zoom_out_btn.setText("-")
        zoom_out_btn.setToolTip("Zoom arrière")
        zoom_out_btn.setFixedSize(24, 24)
        toolbar_layout.addWidget(zoom_out_btn)
        
        toolbar_layout.addStretch()