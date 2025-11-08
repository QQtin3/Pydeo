from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QPushButton, QHBoxLayout, QLabel

from controller.SourceController import SourceController
from controller.TimelineController import TimelineController

from model.Source import Source
from model.Timeline import Timeline

from model.TimelineClip import TimelineClip, TimelineVideoClip

from views.ChooseTrackDialog import ChooseTrackDialog

class SourcesTabWidget(QWidget):
    """Widget used inside the tab bar for managing media sources.

    Provides a scrollable area to list imported sources and a button to
    trigger import. The parent window is responsible for opening the file
    dialog and actual media loading.
    """

    importRequested = Signal()
    
    timeline_controller: TimelineController

    def __init__(self, timeline_controller, source_controller, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        # Root layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(6)

        # Scrollable list of sources
        self.tracksScroll = QScrollArea()
        self.tracksScroll.setWidgetResizable(True)
        self.tracksContainer = QWidget()
        self.tracksLayout = QVBoxLayout(self.tracksContainer)
        self.tracksLayout.setContentsMargins(0, 0, 0, 0)
        self.tracksLayout.setSpacing(4)
        self.tracksLayout.addStretch()
        self.tracksScroll.setWidget(self.tracksContainer)
        layout.addWidget(self.tracksScroll, 1)

        # Buttons row
        btnRow = QHBoxLayout()
        self.importVideoBtn = QPushButton("Importer une source")
        self.importVideoBtn.clicked.connect(self.importRequested.emit)
        btnRow.addWidget(self.importVideoBtn)
        layout.addLayout(btnRow)

        self.source_controller = source_controller
        self.timeline_controller = timeline_controller

    # ----- Public API -----------------------------------------------------
    def addSourceItem(self, fileName: str, durationSec: float, filePath: str) -> None:
        """Append a simple row widget describing an imported source."""
        laSource = Source()
        laSource.name = fileName
        laSource.filepath = filePath

        row = QPushButton()
        rowLayout = QHBoxLayout(row)
        rowLayout.setContentsMargins(5, 2, 5, 2)

        nameLabel = QLabel(fileName)
        nameLabel.setStyleSheet("background-color: #3a3a3a; padding: 5px; border-radius: 3px;")
        rowLayout.addWidget(nameLabel, 1)

        durationLabel = QLabel(f"{durationSec:.1f}s")
        durationLabel.setStyleSheet("min-width: 50px; text-align: right;")
        rowLayout.addWidget(durationLabel)

        row.clicked.connect(lambda : self.selectTimelineAndAddClipToTrack(laSource))

        # Insert before the final stretch
        self.tracksLayout.insertWidget(self.tracksLayout.count() - 1, row)

        self.source_controller.sources.append(laSource)

    def selectTimelineAndAddClipToTrack(self, laSource: Source):
        chooseTrack = ChooseTrackDialog(self.timeline_controller, laSource)
        chooseTrack.exec()
        self.addClipToTrack(
                laSource,
                chooseTrack.getLaTimeline()
            )
        self.timeline_controller.view.timeline.timeline_view.updateLayout()

    def addClipToTrack(self, source: Source, target_timeline: Timeline):
        """
        Lorsque la source est cliquée
        """
        clip = self.timeline_controller.addClip(target_timeline, source.name, source)
        target_timeline.add_clip(clip)
        
        if clip is TimelineVideoClip:
            self.selectTimelineAndAddClipToTrack(Source(c))
        
        self.timeline_controller.view.videoController.loadVideo(self.timeline_controller.timelines)
