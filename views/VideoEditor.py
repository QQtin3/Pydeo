from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                              QPushButton, QFileDialog, QLabel, QToolButton, QSplitter, 
                              QScrollArea, QSlider, QDialog, QTabWidget, QLayout)
from PySide6.QtCore import Qt, QTimer
from moviepy import VideoClip
from moviepy.video.io.VideoFileClip import VideoFileClip
import sys
import os

from controller.VideoPreviewController import VideoPreviewController
from model.TimelineClip import TimelineClip
from .ClipDialog import ClipDialog
from .EffectsTab import EffectsTab
from .TimelineWidget import TimelineWidget
from .PlayHead import PlayHead
from .VideoPreviewWidget import VideoPreviewWidget
from .StatusManager import StatusManager
from .PlaybackControlsWidget import PlaybackControlsWidget
from .ToolbarWidget import ToolbarWidget
from .SourcesTabWidget import SourcesTabWidget

# from ..FileHandlerController import readVideoFile


# VideoEditor main window
# This refactored class composes several modular widgets:
# - VideoPreviewWidget for displaying frames
# - PlaybackControlsWidget for transport controls
# - ToolbarWidget for edit tools
# - SourcesTabWidget for listing/importing media
# - TimelineWidget + PlayHead for basic timeline visualization
# The code uses camelCase and includes comments for maintainability.
class VideoEditor(QMainWindow):
    sourceVideoPath: str | None
    sourceVideo: VideoClip | None
    tracks: list #TODO : à préciser ( => list[Object])
    clips: list[TimelineClip]
    currentPlayTime: float
    timelines: list[TimelineWidget] #TODO : à préciser ( => list[Object])
    videoPreview: VideoPreviewWidget
    playbackControls: PlaybackControlsWidget
    toolbar: ToolbarWidget
    tabs: QTabWidget
    sourcesTab: SourcesTabWidget
    currentTool: str
    timeline: TimelineWidget
    secondTimeline: TimelineWidget
    playHead: PlayHead
    statusManager: StatusManager
    playTimer: QTimer
    isPlaying: bool

    videoController: VideoPreviewController

    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyDEO - Éditeur Vidéo Simple")
        self.setGeometry(100, 100, 1200, 800)
        self.sourceVideoPath = None
        self.sourceVideo = None
        self.tracks = []
        self.clips = []  # Store clip information for timeline
        self.currentPlayTime = 0
        self.timelines = []  # List to manage all timelines dynamically
        
        # Create main widget and layout
        mainWidget = QWidget()
        mainLayout = QVBoxLayout(mainWidget)
        mainLayout.setContentsMargins(5, 5, 5, 5)
        mainLayout.setSpacing(5)
        
        # Create splitter for main content (left: preview, right: tracks)
        mainSplitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left side - video preview
        previewWidget = QWidget()
        previewLayout = QVBoxLayout(previewWidget)
        previewLayout.setContentsMargins(0, 0, 0, 0)
        
        self.videoPreview = VideoPreviewWidget()
        previewLayout.addWidget(self.videoPreview)
        self.videoController = VideoPreviewController(self.videoPreview, 24)
        
        # Transport controls (modularized)
        self.playbackControls = PlaybackControlsWidget()
        # Wire playback control signals
        self.playbackControls.playToggled.connect(lambda wantPlay: self.videoController.play() if wantPlay else self.videoController.pause())
        self.playbackControls.sliderPressed.connect(self.onSliderPressed)
        self.playbackControls.sliderReleased.connect(self.onSliderReleased)
        self.playbackControls.sliderMoved.connect(self.onSliderMoved)
        previewLayout.addWidget(self.playbackControls)
        mainSplitter.addWidget(previewWidget)
		
		# Right side - track list and controls
        rightWidget = QWidget()
        rightLayout = QVBoxLayout(rightWidget)
        rightLayout.setContentsMargins(0, 0, 0, 0)
		
		# Track list area with scroll
		# === Create tabs for Sources and Effects ===
        self.tabs = QTabWidget()
        self.tabs.setTabBarAutoHide(False)
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #555;
                background: #333;
            }
            QTabBar {
                background: #444;
            }
            QTabBar::tab {
                background: #555;
                border: 1px solid #444;
                padding: 5px 10px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background: #666;
                border-bottom-color: #333;
            }
            QTabBar::tab:hover {
                background: #606060;
            }
        """)

        # Tabs on the right side: Sources (custom widget) & Effects
        self.sourcesTab = SourcesTabWidget()
        self.sourcesTab.importRequested.connect(self.importVideo)

        effectsTab = EffectsTab()

        self.tabs.addTab(self.sourcesTab, "Sources")
        self.tabs.addTab(effectsTab, "Effets")

        rightLayout.addWidget(self.tabs)
        mainSplitter.addWidget(rightWidget)
        mainSplitter.setSizes([800, 400])  # Initial sizes

        # Toolbar under the preview (modularized)
        self.toolbar = ToolbarWidget()
        self.toolbar.undoRequested.connect(self.undo)
        self.toolbar.redoRequested.connect(self.redo)
        self.toolbar.zoomInRequested.connect(self.zoomIn)
        self.toolbar.zoomOutRequested.connect(self.zoomOut)
        self.toolbar.modeChanged.connect(self.setToolMode)
        previewLayout.addWidget(self.toolbar)
        
        # Timeline area
        self.timeline = TimelineWidget()
        self.secondTimeline = TimelineWidget()
        
        # Global playhead that extends over all timelines
        self.playHead = PlayHead()
        
        # Add timelines to the list
        self.timelines.append(self.timeline)
        self.timelines.append(self.secondTimeline)
        
        # Status area
        self.statusManager = StatusManager()
        
        # Add everything to main layout
        mainLayout.addWidget(mainSplitter)
        
        # Create container for playhead and timelines
        timelineContainer = QWidget()
        timelineLayout = QVBoxLayout(timelineContainer)
        timelineLayout.setContentsMargins(0, 0, 0, 0)
        timelineLayout.setSpacing(5)
        
        # Add timelines first
        timelineLayout.addWidget(self.timeline)
        timelineLayout.addWidget(self.secondTimeline)
        
        # Configure global playhead to extend over all timelines
        self.playHead.setParent(timelineContainer)
        self.playHead.setTimelineWidgets([self.timeline, self.secondTimeline])
        
        mainLayout.addWidget(timelineContainer)
        mainLayout.addWidget(self.statusManager.status_label)
        
        # Connect video preview signals
        self.videoController.timeChanged.connect(self.onVideoTimeChanged)
        self.videoController.durationChanged.connect(self.onVideoDurationChanged)
        self.videoController.playbackStateChanged.connect(self.onPlaybackStateChanged)

        self.setCentralWidget(mainWidget)

        # Timer for playback
        self.isPlaying = False
        
    def setToolMode(self, mode: str) -> None:
        """Update current editing tool mode and sync toolbar UI.
        This replaces the previous inline button management with a
        dedicated ToolbarWidget.
        """
        # Reflect selection in toolbar UI
        if hasattr(self, 'toolbar'):
            self.toolbar.setMode(mode)
        # Store current mode and report status
        self.currentTool = mode
        self.statusManager.update_status(f"État: Mode d'édition: {mode}")


    def zoomIn(self) -> None:
        """Handle zoom in action"""
        self.statusManager.update_status("État: Zoom avant")
        # In a real implementation, this would zoom in the timeline
    
    def zoomOut(self) -> None:
        """Handle zoom out action"""
        self.statusManager.update_status("État: Zoom arrière")
    
    def importVideo(self) -> None:
        """Open a file dialog, load a video, and reflect it in the UI."""
        filePath, _ = QFileDialog.getOpenFileName(
            self, "Sélectionner une vidéo", "", "Fichiers vidéo (*.mp4 *.avi *.mov *.mkv)"
        )
        if not filePath:
            return
        if self.videoController.loadVideo(filePath):
            # Keep source references
            self.sourceVideoPath = filePath
            self.sourceVideo = self.videoController.clip

            # Add to the Sources tab list
            try:
                duration = float(self.sourceVideo.duration)
            except Exception:
                duration = 0.0
            self.sourcesTab.addSourceItem(os.path.basename(self.sourceVideoPath or ""), duration)

            # Inform status bar; the rest of the UI (slider, play button)
            # is updated via VideoPreviewController signals we connect below.
            self.statusManager.update_status(f"État: Vidéo chargée - {os.path.basename(filePath)}")
        else:
            self.statusManager.update_status("Erreur: Impossible de charger la vidéo")
    
    def addTrack(self) -> None:
        if not self.sourceVideo:
            return

        dialog = ClipDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            start, end = dialog.getValues()

            # Validate clip range
            if end <= start:
                self.statusManager.update_status("Erreur: La fin doit être après le début")
                return

            if end > self.sourceVideo.duration:
                end = self.sourceVideo.duration
                self.statusManager.update_status(f"Avertissement: Fin ajustée à la durée maximale ({self.sourceVideo.duration:.1f}s)")

            # Reflect in sources list (as a derived clip item)
            baseName = os.path.basename(self.sourceVideoPath or "")
            self.sourcesTab.addSourceItem(f"{baseName} [{start:.1f}s - {end:.1f}s]", end - start)

            # Add to timeline model & view
            self.clips.append(TimelineClip(baseName, start, end))
            self.timeline.addClip(self.clips[-1])

            self.statusManager.update_status(f"État: Clip ajouté à la piste [{start:.1f}s - {end:.1f}s]")
    
    def togglePlay(self) -> None:
        if self.sourceVideo is None or not self.sourceVideo:
            return
        self.videoController.togglePlayPause()
        
    
    # Legacy helper kept for reference; playback is driven by VideoPreviewController
    def updatePlayback(self):
        if not self.sourceVideo:
            return

        # Simulate time progression (would normally be driven by the controller)
        self.currentPlayTime += 0.03  # ~30ms per tick
        if self.currentPlayTime >= self.sourceVideo.duration:
            self.currentPlayTime = 0
            # Stop via controller to keep state consistent
            self.videoController.pause()
            self.isPlaying = False

        # Update UI via the modular controls
        self.playbackControls.setPositionMs(int(self.currentPlayTime * 1000))
        self.videoPreview.currentTime = self.currentPlayTime
        self.timeline.setCurrentTime(self.currentPlayTime)
        self.updateTimeDisplay()

        # In a complete implementation we would fetch and display the current frame.
    
    def updateTimeDisplay(self) -> None:
        """Refresh the time label in playback controls."""
        if not self.sourceVideo:
            self.playbackControls.setTimeLabel(0, 0)
            return
        self.playbackControls.setTimeLabel(self.currentPlayTime, self.sourceVideo.duration)
    
    def undo(self) -> None:
        self.statusManager.update_status("État: Action annulée")
        # Implementation would track changes and revert them
    
    def redo(self) -> None:
        self.statusManager.update_status("État: Action refaite")
        # Implementation would redo previously undone actions
    
    def addTimeline(self) -> TimelineWidget:
        """Add a new timeline"""
        newTimeline = TimelineWidget()
        self.timelines.append(newTimeline)
        
        # Update duration if video is loaded
        if self.sourceVideo:
            newTimeline.setDuration(self.sourceVideo.duration)
        
        return newTimeline

    def exportVideo(self) -> None:
        if not self.clips:
            self.statusManager.update_status("Erreur: Aucun clip à exporter")
            return
            
        filePath, _ = QFileDialog.getSaveFileName(
            self, "Exporter la vidéo", "", "Fichiers vidéo (*.mp4)"
        )
        
        if filePath:
            try:
                # In a real implementation, this would composite the clips and export
                self.statusManager.update_status(f"État: Export en cours vers {filePath}...")
                
                # Simulate export progress
                QTimer.singleShot(2000, lambda: self.statusManager.update_status(f"État: Vidéo exportée vers {filePath}"))
                
            except Exception as e:
                self.statusManager.update_status(f"Erreur d'export: {str(e)}")
    
    def onVideoTimeChanged(self, time):
        """Called when video time changes during playback"""
        self.currentPlayTime = time
        # Update slider without causing feedback
        self.playbackControls.setPositionMs(int(time * 1000))
        self.timeline.setCurrentTime(time)
        self.updateTimeDisplay()
	
    def onVideoDurationChanged(self, duration):
        """Called when a new video is loaded"""
        self.videoPreview.videoDuration = duration
        self.playbackControls.setDurationMs(int(duration * 1000))
        self.timeline.setDuration(duration)
        self.updateTimeDisplay()
	
    def onPlaybackStateChanged(self, isPlaying):
        """Called when playback starts or stops"""
        self.isPlaying = isPlaying
        self.playbackControls.setIsPlaying(isPlaying)
	
    def onSliderPressed(self):
        """Pause when user grabs the slider"""
        if self.isPlaying:
            self.videoController.pause()
            self.__wasPlaying__ = True
        else:
            self.__wasPlaying__ = False
	
    def onSliderMoved(self, value):
        """Update video position as slider moves"""
        time = value / 1000.0
        self.videoController.seek(time)
	
    def onSliderReleased(self):
        """Resume playback if it was playing before"""
        if hasattr(self, '__wasPlaying__') and self.__wasPlaying__:
            self.videoController.play()