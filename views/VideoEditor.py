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

# from ..FileHandlerController import readVideoFile


class VideoEditor(QMainWindow):
    sourceVideoPath: str | None
    sourceVideo: VideoClip | None
    tracks: list #TODO : à préciser ( => list[Object])
    clips: list[TimelineClip]
    currentPlayTime: float
    timelines: list[TimelineWidget] #TODO : à préciser ( => list[Object])
    videoPreview: VideoPreviewWidget
    playBtn: QPushButton
    positionSlider: QSlider
    timeLabel: QLabel
    tabs: QTabWidget
    tracksContainer: QWidget
    tracksLayout: QVBoxLayout
    importVideoBtn: QPushButton
    addTrackBtn: QPushButton
    removeTrackBtn: QPushButton
    currentTool: str
    timeline: TimelineWidget
    secondTimeline: TimelineWidget
    playHead: PlayHead
    statusLabel: QLabel
    playTimer: QTimer
    isPlaying: bool
    moveBtn: QToolButton
    cutBtn: QToolButton
    splitBtn: QToolButton
    selectBtn: QToolButton
    exportBtn: QToolButton
    
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
        
        # Transport controls
        transportLayout = QHBoxLayout()
        self.playBtn = QPushButton("▶")
        self.playBtn.setFixedSize(30, 30)
        self.playBtn.clicked.connect(self.togglePlay)
        transportLayout.addWidget(self.playBtn)
        
        self.positionSlider = QSlider(Qt.Orientation.Horizontal)
        self.positionSlider.setEnabled(False)
        self.positionSlider.sliderPressed.connect(self.onSliderPressed)
        self.positionSlider.sliderReleased.connect(self.onSliderReleased)
        self.positionSlider.sliderMoved.connect(self.onSliderMoved)
        transportLayout.addWidget(self.positionSlider)
		
        self.timeLabel = QLabel("00:00 / 00:00")
        transportLayout.addWidget(self.timeLabel)
		
        previewLayout.addLayout(transportLayout)
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

        # Sources tab
        sourcesTab = QWidget()
        sourcesLayout = QVBoxLayout(sourcesTab)
        sourcesLayout.setContentsMargins(5, 5, 5, 5)

        tracksScroll = QScrollArea()
        tracksScroll.setWidgetResizable(True)
        self.tracksContainer = QWidget()
        self.tracksLayout = QVBoxLayout(self.tracksContainer)
        self.tracksLayout.addStretch()
        tracksScroll.setWidget(self.tracksContainer)

        sourcesLayout.addWidget(tracksScroll)

        # Track controls
        trackBtnLayout = QHBoxLayout()

        self.importVideoBtn = QPushButton("Importer une source")
        self.importVideoBtn.clicked.connect(self.importVideo)
        self.importVideoBtn.setEnabled(True)
        trackBtnLayout.addWidget(self.importVideoBtn)

        """
        self.addTrackBtn = QPushButton("Ajouter une piste")
        self.addTrackBtn.clicked.connect(self.addTrack)
        self.addTrackBtn.setEnabled(False)
        trackBtnLayout.addWidget(self.addTrackBtn)
        
        self.removeTrackBtn = QPushButton("Supprimer piste")
        self.removeTrackBtn.setEnabled(False)
        trackBtnLayout.addWidget(self.removeTrackBtn)
        """
        
        sourcesLayout.addLayout(trackBtnLayout)

        # Effects tab
        effectsTab = EffectsTab()
        
        # Add tabs
        self.tabs.addTab(sourcesTab, "Sources")
        self.tabs.addTab(effectsTab, "Effets")
        
        rightLayout.addWidget(self.tabs)
        mainSplitter.addWidget(rightWidget)
        mainSplitter.setSizes([800, 400])  # Initial sizes
        
        mainSplitter.addWidget(rightWidget)
        mainSplitter.setSizes([800, 400])  # Initial sizes

        self.createToolbar(previewLayout)
        
        # Timeline area
        self.timeline = TimelineWidget()
        self.secondTimeline = TimelineWidget()
        
        # Global playhead that extends over all timelines
        self.playHead = PlayHead()
        
        # Add timelines to the list
        self.timelines.append(self.timeline)
        self.timelines.append(self.secondTimeline)
        
        # Status area
        self.statusLabel = QLabel("État: Aucune vidéo importée")
        
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
        mainLayout.addWidget(self.statusLabel)
        
        # Connect video preview signals
        self.videoController.timeChanged.connect(self.onVideoTimeChanged)
        self.videoController.durationChanged.connect(self.onVideoDurationChanged)
        self.videoController.playbackStateChanged.connect(self.onPlaybackStateChanged)

        self.setCentralWidget(mainWidget)

        # Timer for playback
        self.isPlaying = False
        
    def setToolMode(self, mode: str) -> None:
        """Set the current editing tool mode"""
        # Uncheck all tool buttons
        self.moveBtn.setChecked(False)
        self.cutBtn.setChecked(False)
        self.splitBtn.setChecked(False)
        self.selectBtn.setChecked(False)
        
        # Check the selected tool
        if mode == 'move':
            self.moveBtn.setChecked(True)
        elif mode == 'cut':
            self.cutBtn.setChecked(True)
        elif mode == 'split':
            self.splitBtn.setChecked(True)
        elif mode == 'select':
            self.selectBtn.setChecked(True)
        
        self.currentTool = mode
        self.statusLabel.setText(f"État: Mode d'édition: {mode}")

    def createToolbar(self, layout: QLayout) -> None:
        """Create the top toolbar with editing tools"""
        """Create the toolbar to be placed under the video preview"""
        toolbarWidget = QWidget()
        toolbarWidget.setStyleSheet("background-color: #3a3a3a; border-top: 1px solid #555; border-bottom: 1px solid #555;")
        toolbarLayout = QHBoxLayout(toolbarWidget)
        toolbarLayout.setContentsMargins(5, 2, 5, 2)
        toolbarLayout.setSpacing(8)
        
        # Undo/Redo
        undoBtn = QToolButton()
        undoBtn.setText("↩")
        undoBtn.setToolTip("Annuler (Ctrl+Z)")
        undoBtn.setFixedSize(24, 24)
        undoBtn.clicked.connect(self.undo)
        toolbarLayout.addWidget(undoBtn)
        
        redoBtn = QToolButton()
        redoBtn.setText("↪")
        redoBtn.setToolTip("Refaire (Ctrl+Y)")
        redoBtn.setFixedSize(24, 24)
        redoBtn.clicked.connect(self.redo)
        toolbarLayout.addWidget(redoBtn)
        
        toolbarLayout.addSpacing(15)
        
        # Editing tools (as checkable buttons)
        self.moveBtn = QToolButton()
        self.moveBtn.setCheckable(True)
        self.moveBtn.setChecked(True)
        self.moveBtn.setText("⤢")
        self.moveBtn.setToolTip("Déplacer")
        self.moveBtn.setFixedSize(24, 24)
        self.moveBtn.clicked.connect(lambda: self.setToolMode('move'))
        toolbarLayout.addWidget(self.moveBtn)
        
        self.cutBtn = QToolButton()
        self.cutBtn.setCheckable(True)
        self.cutBtn.setText("✂")
        self.cutBtn.setToolTip("Couper")
        self.cutBtn.setFixedSize(24, 24)
        self.cutBtn.clicked.connect(lambda: self.setToolMode('cut'))
        toolbarLayout.addWidget(self.cutBtn)
        
        self.splitBtn = QToolButton()
        self.splitBtn.setCheckable(True)
        self.splitBtn.setText("⌬")
        self.splitBtn.setToolTip("Scinder")
        self.splitBtn.setFixedSize(24, 24)
        self.splitBtn.clicked.connect(lambda: self.setToolMode('split'))
        toolbarLayout.addWidget(self.splitBtn)
        
        self.selectBtn = QToolButton()
        self.selectBtn.setCheckable(True)
        self.selectBtn.setText("☐")
        self.selectBtn.setToolTip("Sélectionner")
        self.selectBtn.setFixedSize(24, 24)
        self.selectBtn.clicked.connect(lambda: self.setToolMode('select'))
        toolbarLayout.addWidget(self.selectBtn)
        
        toolbarLayout.addSpacing(15)
        
        # Zoom controls
        zoomInBtn = QToolButton()
        zoomInBtn.setText("+")
        zoomInBtn.setToolTip("Zoom avant")
        zoomInBtn.setFixedSize(24, 24)
        zoomInBtn.clicked.connect(self.zoomIn)
        toolbarLayout.addWidget(zoomInBtn)
        
        zoomOutButton = QToolButton()
        zoomOutButton.setText("-")
        zoomOutButton.setToolTip("Zoom arrière")
        zoomOutButton.setFixedSize(24, 24)
        zoomOutButton.clicked.connect(self.zoomOut)
        toolbarLayout.addWidget(zoomOutButton)
        
        toolbarLayout.addStretch()
        
        # Add the toolbar to the provided layout (under video preview)
        layout.addWidget(toolbarWidget)

    def zoomIn(self) -> None:
        """Handle zoom in action"""
        self.statusLabel.setText("État: Zoom avant")
        # In a real implementation, this would zoom in the timeline
    
    def zoomOut(self) -> None:
        """Handle zoom out action"""
        self.statusLabel.setText("État: Zoom arrière")
    
    def importVideo(self, filePath: str):
        filePath, _ = QFileDialog.getOpenFileName(
			self, "Sélectionner une vidéo", "", "Fichiers vidéo (*.mp4 *.avi *.mov *.mkv)"
		)
        if self.videoController.loadVideo(filePath):
			
			# TODO: Revoir pour ne garder que le payload playHead
            """
			# Update timeline with video duration
                self.timeline.set_duration(self.source_video.duration)
                # Update all timelines with duration
                for timeline in self.timelines:
                    timeline.setDuration(self.sourceVideo.duration)
                # Update global play head
                self.playHead.setDuration(self.sourceVideo.duration)
                self.positionSlider.setRange(0, int(self.sourceVideo.duration * 1000))
                self.updateTimeDisplay()
                
                # Display first frame
                self.currentPlayTime = 0
                self.videoPreview.setFrame(None)  # In real app, you'd get the actual frame
                self.videoPreview.videoDuration = self.sourceVideo.duration
                self.videoPreview.currentTime = 0

                #readVideoFile(file_path)

                # Create track item
                trackItem = QWidget()
                trackLayout = QHBoxLayout(trackItem)
                trackLayout.setContentsMargins(5, 2, 5, 2)
                
                # Clip info
                clipInfo = QLabel(f"{os.path.basename(self.sourceVideoPath)}")
                clipInfo.setStyleSheet("background-color: #3a3a3a; padding: 5px; border-radius: 3px;")
                trackLayout.addWidget(clipInfo, 1)
                
                # Duration
                duration = self.sourceVideo.duration
                durationLabel = QLabel(f"{duration:.1f}s")
                durationLabel.setStyleSheet("min-width: 50px; text-align: right;")
                trackLayout.addWidget(durationLabel)
                
                # Add to tracks layout
                self.tracks_layout.insertWidget(self.tracks_layout.count() - 1, track_item)
                self.status_label.setText(f"État: Vidéo ajoutée - {os.path.basename(file_path)}"
			"""

			
            self.sourceVideoPath = filePath
            self.sourceVideo = self.videoController.clip

            # Create track item
            trackItem = QWidget()
            trackLayout = QHBoxLayout(trackItem)
            trackLayout.setContentsMargins(5, 2, 5, 2)
            
            # Clip info
            duration = self.sourceVideo.duration
            clipInfo = QLabel(f"{os.path.basename(self.sourceVideoPath or "")}")
            clipInfo.setStyleSheet("background-color: #3a3a3a; padding: 5px; border-radius: 3px;")
            trackLayout.addWidget(clipInfo, 1)
            
            # Duration
            durationLabel = QLabel(f"{duration:.1f}s")
            durationLabel.setStyleSheet("min-width: 50px; text-align: right;")
            trackLayout.addWidget(durationLabel)
            
            # Add to tracks layout
            self.tracksLayout.insertWidget(self.tracksLayout.count() - 1, trackItem)
            
            self.statusLabel.setText(f"État: Vidéo chargée - {os.path.basename(filePath)}")
        else:
            self.statusLabel.setText("Erreur: Impossible de charger la vidéo")
    
    def addTrack(self) -> None:
        if not self.sourceVideo:
            return
            
        dialog = ClipDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            start, end = dialog.getValues()
            
            # Validate clip range
            if end <= start:
                self.statusLabel.setText("Erreur: La fin doit être après le début")
                return
                
            if end > self.sourceVideo.duration:
                end = self.sourceVideo.duration
                self.statusLabel.setText(f"Avertissement: Fin ajustée à la durée maximale ({self.sourceVideo.duration:.1f}s)")
            
            # Create track item
            trackItem = QWidget()
            trackLayout = QHBoxLayout(trackItem)
            trackLayout.setContentsMargins(5, 2, 5, 2)
            
            # Clip info
            clipInfo = QLabel(f"{os.path.basename(self.sourceVideoPath or "")} [{start:.1f}s - {end:.1f}s]")
            clipInfo.setStyleSheet("background-color: #3a3a3a; padding: 5px; border-radius: 3px;")
            trackLayout.addWidget(clipInfo, 1)
            
            # Duration
            duration = end - start
            durationLabel = QLabel(f"{duration:.1f}s")
            durationLabel.setStyleSheet("min-width: 50px; text-align: right;")
            trackLayout.addWidget(durationLabel)
            
            # Add to tracks layout
            self.tracksLayout.insertWidget(self.tracksLayout.count() - 1, trackItem)
            
            # Add to timeline
            self.clips.append(TimelineClip(os.path.basename(self.sourceVideoPath or ""), start, end))
            self.timeline.addClip(self.clips[-1])
            
            self.statusLabel.setText(f"État: Clip ajouté à la piste [{start:.1f}s - {end:.1f}s]")
    
    def togglePlay(self) -> None:
        if self.sourceVideo is None or not self.sourceVideo:
            return
        self.videoController.togglePlayPause()
        
    
    # TODO: mettre à jour puisque playback n'est plus utilisé
    def updatePlayback(self):
        if not self.sourceVideo:
            return
            
        self.currentPlayTime += 0.03  # 30ms per frame
        if self.currentPlayTime >= self.sourceVideo.duration:
            self.currentPlayTime = 0
            self.playTimer.stop()
            self.playBtn.setText("▶")
            self.isPlaying = False
        
        # Update UI
        self.positionSlider.setValue(int(self.currentPlayTime * 1000))
        self.videoPreview.currentTime = self.currentPlayTime
        self.timeline.setCurrentTime(self.currentPlayTime)
        self.updateTimeDisplay()
        
        # In real app, you'd get the current frame and display it:
        # frame = self.source_video.get_frame(self.current_play_time)
        # self.video_preview.set_frame(frame)
    
    def updateTimeDisplay(self) -> None:
        if not self.sourceVideo:
            self.timeLabel.setText("00:00 / 00:00")
            return
            
        currentMin = int(self.currentPlayTime // 60)
        currentSec = int(self.currentPlayTime % 60)
        totalMin = int(self.sourceVideo.duration // 60)
        totalSec = int(self.sourceVideo.duration % 60)
        
        self.timeLabel.setText(f"{currentMin:02d}:{currentSec:02d} / {totalMin:02d}:{totalSec:02d}")
    
    def undo(self) -> None:
        self.statusLabel.setText("État: Action annulée")
        # Implementation would track changes and revert them
    
    def redo(self) -> None:
        self.statusLabel.setText("État: Action refaite")
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
            self.statusLabel.setText("Erreur: Aucun clip à exporter")
            return
            
        filePath, _ = QFileDialog.getSaveFileName(
            self, "Exporter la vidéo", "", "Fichiers vidéo (*.mp4)"
        )
        
        if filePath:
            try:
                # In a real implementation, this would composite the clips and export
                self.statusLabel.setText(f"État: Export en cours vers {filePath}...")
                
                # Simulate export progress
                QTimer.singleShot(2000, lambda: self.statusLabel.setText(f"État: Vidéo exportée vers {filePath}"))
                
            except Exception as e:
                self.statusLabel.setText(f"Erreur d'export: {str(e)}")
    
    def onVideoTimeChanged(self, time):
        """Called when video time changes during playback"""
        self.currentPlayTime = time
        self.positionSlider.blockSignals(True)
        self.positionSlider.setValue(int(time * 1000))
        self.positionSlider.blockSignals(False)
        self.timeline.setCurrentTime(time)
        self.updateTimeDisplay()
	
    def onVideoDurationChanged(self, duration):
        """Called when a new video is loaded"""
        self.videoPreview.videoDuration = duration
        self.positionSlider.setRange(0, int(duration * 1000))
        self.positionSlider.setEnabled(True)
        self.timeline.setDuration(duration)
        self.updateTimeDisplay()
	
    def onPlaybackStateChanged(self, isPlaying):
        """Called when playback starts or stops"""
        self.isPlaying = isPlaying
        self.playBtn.setText("⏸" if isPlaying else "▶")
	
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