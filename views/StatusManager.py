# StatusManager.py
from PySide6.QtWidgets import QLabel

class StatusManager:
    def __init__(self):
        self.status_label = QLabel("État: Aucune vidéo importée")
        self.status_label.setStyleSheet("padding: 5px; background-color: #333; color: #ccc;")
    
    def update_status(self, message):
        """Met à jour le message d'état"""
        self.status_label.setText(message)