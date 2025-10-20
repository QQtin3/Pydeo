# views/ChooseTrackDialog.py

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QListWidget,
    QPushButton,
    QMessageBox
)
from model.Source import Source
from controller.TimelineController import TimelineController
from controller.utils.fileExtensions import isFileAudio, isFileVideo
from model.Timeline import Timeline, TimelineType


class ChooseTrackDialog(QDialog):
    """
    Fenêtre permettant de choisir la timeline sur laquelle ajouter une source.
    Seules les timelines compatibles (audio ou vidéo) sont proposées.
    """

    def __init__(self, controller: TimelineController, source: Source, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.source = source
        self.laTimeline = None

        self.setWindowTitle("Choisir une timeline")
        self.setMinimumWidth(300)

        layout = QVBoxLayout(self)

        # Déterminer le type de la source
        self.is_audio = isFileAudio(self.source.filepath)
        self.is_video = isFileVideo(self.source.filepath)

        # Texte d’intro
        type_str = "audio" if self.is_audio else "vidéo" if self.is_video else "inconnu"
        label = QLabel(f"Ajouter la source « {self.source.name} » ({type_str}) à une timeline :")
        layout.addWidget(label)

        # Liste des timelines compatibles
        self.listWidget = QListWidget()
        self.populateTimelines()
        layout.addWidget(self.listWidget)

        # Boutons
        self.okButton = QPushButton("Ajouter")
        self.cancelButton = QPushButton("Annuler")

        self.okButton.clicked.connect(self.accept)
        self.cancelButton.clicked.connect(self.reject)

        layout.addWidget(self.okButton)
        layout.addWidget(self.cancelButton)

    def populateTimelines(self):
        """Remplit la liste avec les timelines compatibles."""
        for timeline in self.controller.timelines:
            if self.is_audio and timeline.type == TimelineType.AUDIO:
                self.listWidget.addItem(timeline.name)
            elif self.is_video and timeline.type == TimelineType.VIDEO:
                self.listWidget.addItem(timeline.name)

    def accept(self):
        """Valide le choix de timeline."""
        current_item = self.listWidget.currentItem()
        if current_item:
            name = current_item.text()
            # On retrouve l'objet Timeline correspondant
            for timeline in self.controller.timelines:
                if timeline.name == name:
                    self.laTimeline = timeline
                    break
            super().accept()
        else:
            QMessageBox.warning(self, "Aucune sélection", "Veuillez choisir une timeline avant de continuer.")

    def getLaTimeline(self):
        """Retourne la timeline choisie."""
        return self.laTimeline
