from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QPushButton, 
                               QLabel, QDoubleSpinBox, QDialog)


class ClipDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Paramètres de la vidéo")
        self.setGeometry(200, 200, 400, 200)
        
        layout = QVBoxLayout()
        
        # Start time
        start_layout = QHBoxLayout()
        start_layout.addWidget(QLabel("Début (s):"))
        self.start_spin = QDoubleSpinBox()
        self.start_spin.setRange(0, 3600)
        self.start_spin.setSingleStep(0.1)
        start_layout.addWidget(self.start_spin)
        layout.addLayout(start_layout)
        
        # End time
        end_layout = QHBoxLayout()
        end_layout.addWidget(QLabel("Fin (s):"))
        self.end_spin = QDoubleSpinBox()
        self.end_spin.setRange(0, 3600)
        self.end_spin.setSingleStep(0.1)
        end_layout.addWidget(self.end_spin)
        layout.addLayout(end_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.ok_btn = QPushButton("OK")
        self.ok_btn.clicked.connect(self.accept)
        self.cancel_btn = QPushButton("Annuler")
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.ok_btn)
        button_layout.addWidget(self.cancel_btn)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
    def get_values(self):
        return self.start_spin.value(), self.end_spin.value()