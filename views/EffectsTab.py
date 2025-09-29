from PySide6.QtWidgets import (QWidget, QVBoxLayout,
                              QPushButton, QLabel)

class EffectsTab(QWidget):
    """Tab for video effects"""
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Add some placeholder effect controls
        effects_label = QLabel("Liste des effets disponibles:")
        effects_label.setStyleSheet("font-weight: bold; color: #ccc;")
        layout.addWidget(effects_label)
        
        # Add some example effects
        effects = [
            "Fondu", "Dissolution", "Zoom", "Rotation", 
            "N&B", "Contraste", "Luminosité", "Saturation"
        ]
        
        for effect in effects:
            btn = QPushButton(effect)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #4a4a4a;
                    border: 1px solid #5a5a5a;
                    border-radius: 4px;
                    padding: 5px;
                    margin: 2px 0;
                }
                QPushButton:hover {
                    background-color: #5a5a5a;
                }
            """)
            layout.addWidget(btn)
        
        layout.addStretch()
        self.setLayout(layout)