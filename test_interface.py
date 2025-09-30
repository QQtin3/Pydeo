from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                              QPushButton, QFileDialog, QLabel, QSpinBox, QDoubleSpinBox,
                              QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView,
                              QToolBar, QToolButton, QSplitter, QScrollArea, QFrame, QSlider,
                              QDialog, QSizePolicy, QTabWidget)
from PySide6.QtCore import Qt, QSize, QRectF, QTimer
from PySide6.QtGui import QAction, QIcon, QPainter, QBrush, QPen, QColor
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
import sys
import os
from styles import PydeoStyles


class VideoPreviewWidget(QWidget):
    """Widget to display video preview"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(400, 300)
        self.setObjectName("video_preview")
        self.setStyleSheet("background-color: #000000;")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.current_frame = None
        self.video_duration = 0
        self.current_time = 0
        
    def set_frame(self, frame):
        """Set the current frame to display"""
        self.current_frame = frame
        self.update()
        
    def paintEvent(self, event):
        """Draw the current frame"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(QColor(0, 0, 0)))
        painter.drawRect(self.rect())
        
        if self.current_frame:
            # Here you would draw the actual video frame
            # This is a placeholder - in real implementation you'd convert the frame to QImage
            painter.setBrush(QBrush(QColor(50, 50, 50)))
            painter.drawRect(10, 10, self.width()-20, self.height()-20)
            painter.setPen(QColor(200, 200, 200))
            painter.drawText(self.rect(), Qt.AlignCenter, "Video Preview")
        
        # Draw playhead
        if self.video_duration > 0:
            ratio = self.current_time / self.video_duration
            x = int(ratio * self.width())
            painter.setPen(QPen(QColor(255, 0, 0), 2))
            painter.drawLine(x, 0, x, self.height())


class TimelineWidget(QWidget):
    """Custom widget for the timeline"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(100)
        self.video_duration = 0
        self.current_time = 0
        self.clips = []  # List of clips to display on timeline
        
    def add_clip(self, clip):
        """Add a clip to the timeline"""
        self.clips.append(clip)
        self.update()
        
    def set_current_time(self, time):
        """Set the current play position"""
        self.current_time = time
        self.update()
        
    def set_duration(self, duration):
        """Set the total video duration"""
        self.video_duration = duration
        self.update()
        
    def paintEvent(self, event):
        """Draw the timeline"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Background
        painter.setBrush(QBrush(QColor(40, 40, 40)))
        painter.drawRect(self.rect())
        
        # Time ruler
        painter.setPen(QColor(150, 150, 150))
        for i in range(0, self.width(), 50):
            painter.drawLine(i, 0, i, 20)
            if i % 100 == 0 and self.video_duration > 0:
                time_pos = (i / self.width()) * self.video_duration
                minutes = int(time_pos // 60)
                seconds = int(time_pos % 60)
                painter.drawText(i + 5, 15, f"{minutes}:{seconds:02d}")
        
        # Clips on timeline
        clip_height = 60
        y = (self.height() - clip_height) // 2
        for clip in self.clips:
            if self.video_duration > 0:
                start_ratio = clip['start'] / self.video_duration
                end_ratio = clip['end'] / self.video_duration
                x = int(start_ratio * self.width())
                w = max(10, int((end_ratio - start_ratio) * self.width()))
                
                # Draw clip rectangle
                painter.setBrush(QBrush(QColor(60, 120, 200, 200)))
                painter.drawRect(x, y, w, clip_height)
                
                # Draw clip label
                painter.setPen(QColor(255, 255, 255))
                text = clip['name']
                text_rect = painter.fontMetrics().boundingRect(text)
                if text_rect.width() < w - 10:
                    painter.drawText(x + 5, y + clip_height // 2 + 5, text)
        
        # Playhead
        if self.video_duration > 0:
            ratio = self.current_time / self.video_duration
            x = int(ratio * self.width())
            painter.setPen(QPen(QColor(255, 0, 0), 2))
            painter.drawLine(x, 0, x, self.height())
            painter.setBrush(QBrush(QColor(255, 0, 0)))
            painter.drawRect(x - 5, 0, 10, 20)

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
            layout.addWidget(btn)
        
        layout.addStretch()
        self.setLayout(layout)


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


class VideoEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Éditeur Vidéo Simple")
        self.setGeometry(100, 100, 1200, 800)
        self.source_video_path = None
        self.source_video = None
        self.tracks = []
        self.clips = []  # Store clip information for timeline
        self.current_play_time = 0
        
        # Apply styles from external stylesheet
        self.setStyleSheet(PydeoStyles.get_all_styles())
        
        # Create main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(5)
        
        # Create splitter for main content (left: preview, right: tracks)
        main_splitter = QSplitter(Qt.Horizontal)
        
        # Left side - video preview
        preview_widget = QWidget()
        preview_layout = QVBoxLayout(preview_widget)
        preview_layout.setContentsMargins(0, 0, 0, 0)
        
        self.video_preview = VideoPreviewWidget()
        preview_layout.addWidget(self.video_preview)
        
        # Transport controls
        transport_layout = QHBoxLayout()
        self.play_btn = QPushButton("▶")
        self.play_btn.setObjectName("play_button")
        self.play_btn.setFixedSize(30, 30)
        self.play_btn.clicked.connect(self.toggle_play)
        transport_layout.addWidget(self.play_btn)
        
        self.position_slider = QSlider(Qt.Horizontal)
        self.position_slider.setEnabled(False)
        transport_layout.addWidget(self.position_slider)
        
        self.time_label = QLabel("00:00 / 00:00")
        transport_layout.addWidget(self.time_label)
        
        preview_layout.addLayout(transport_layout)
        main_splitter.addWidget(preview_widget)
        
        # Right side - track list and controls
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        # Track list area with scroll
        # === Create tabs for Sources and Effects ===
        self.tabs = QTabWidget()
        self.tabs.setTabBarAutoHide(False)
        
        # Sources tab
        sources_tab = QWidget()
        sources_layout = QVBoxLayout(sources_tab)
        sources_layout.setContentsMargins(5, 5, 5, 5)

        tracks_scroll = QScrollArea()
        tracks_scroll.setWidgetResizable(True)
        self.tracks_container = QWidget()
        self.tracks_layout = QVBoxLayout(self.tracks_container)
        self.tracks_layout.addStretch()
        tracks_scroll.setWidget(self.tracks_container)

        sources_layout.addWidget(tracks_scroll)

        # Track controls
        track_btn_layout = QHBoxLayout()

        self.import_video_btn = QPushButton("Importer une source")
        self.import_video_btn.clicked.connect(self.import_video)
        self.import_video_btn.setEnabled(True)
        track_btn_layout.addWidget(self.import_video_btn)

        self.add_track_btn = QPushButton("Ajouter une piste")
        self.add_track_btn.clicked.connect(self.add_track)
        self.add_track_btn.setEnabled(False)
        track_btn_layout.addWidget(self.add_track_btn)
        
        self.remove_track_btn = QPushButton("Supprimer piste")
        self.remove_track_btn.setEnabled(False)
        track_btn_layout.addWidget(self.remove_track_btn)
        sources_layout.addLayout(track_btn_layout)

        # Effects tab
        effects_tab = EffectsTab()
        
        # Add tabs
        self.tabs.addTab(sources_tab, "Sources")
        self.tabs.addTab(effects_tab, "Effets")
        
        right_layout.addWidget(self.tabs)
        main_splitter.addWidget(right_widget)
        main_splitter.setSizes([800, 400])  # Initial sizes
        
        main_splitter.addWidget(right_widget)
        main_splitter.setSizes([800, 400])  # Initial sizes

        self.create_toolbar(preview_layout)
        
        # Timeline area
        self.timeline = TimelineWidget()
        self.timeline.setObjectName("timeline")
        self.second_timeline = TimelineWidget()
        self.second_timeline.setObjectName("timeline")
        
        # Status area
        self.status_label = QLabel("État: Aucune vidéo importée")
        
        # Add everything to main layout
        main_layout.addWidget(main_splitter)
        main_layout.addWidget(self.timeline)
        main_layout.addWidget(self.second_timeline)
        main_layout.addWidget(self.status_label)
        
        self.setCentralWidget(main_widget)
        
        # Timer for playback
        self.play_timer = QTimer()
        self.play_timer.timeout.connect(self.update_playback)
        self.is_playing = False
        
    def set_tool_mode(self, mode):
        """Set the current editing tool mode"""
        # Uncheck all tool buttons
        self.move_btn.setChecked(False)
        self.cut_btn.setChecked(False)
        self.split_btn.setChecked(False)
        self.select_btn.setChecked(False)
        
        # Check the selected tool
        if mode == 'move':
            self.move_btn.setChecked(True)
        elif mode == 'cut':
            self.cut_btn.setChecked(True)
        elif mode == 'split':
            self.split_btn.setChecked(True)
        elif mode == 'select':
            self.select_btn.setChecked(True)
        
        self.current_tool = mode
        self.status_label.setText(f"État: Mode d'édition: {mode}")
    def create_toolbar(self, layout):
        """Create the top toolbar with editing tools"""
        """Create the toolbar to be placed under the video preview"""
        toolbar_widget = QWidget()
        toolbar_widget.setObjectName("toolbar_widget")
        toolbar_layout = QHBoxLayout(toolbar_widget)
        toolbar_layout.setContentsMargins(5, 2, 5, 2)
        toolbar_layout.setSpacing(8)
        
        # Undo/Redo
        undo_btn = QToolButton()
        undo_btn.setText("↩")
        undo_btn.setToolTip("Annuler (Ctrl+Z)")
        undo_btn.setFixedSize(32, 32)
        undo_btn.clicked.connect(self.undo)
        toolbar_layout.addWidget(undo_btn)
        
        redo_btn = QToolButton()
        redo_btn.setText("↪")
        redo_btn.setToolTip("Refaire (Ctrl+Y)")
        redo_btn.setFixedSize(32, 32)
        redo_btn.clicked.connect(self.redo)
        toolbar_layout.addWidget(redo_btn)
        
        toolbar_layout.addSpacing(15)
        
        # Editing tools (as checkable buttons)
        self.move_btn = QToolButton()
        self.move_btn.setCheckable(True)
        self.move_btn.setChecked(True)
        self.move_btn.setText("⤢")
        self.move_btn.setToolTip("Déplacer")
        self.move_btn.setFixedSize(32, 32)
        self.move_btn.clicked.connect(lambda: self.set_tool_mode('move'))
        toolbar_layout.addWidget(self.move_btn)
        
        self.cut_btn = QToolButton()
        self.cut_btn.setCheckable(True)
        self.cut_btn.setText("✂")
        self.cut_btn.setToolTip("Couper")
        self.cut_btn.setFixedSize(32, 32)
        self.cut_btn.clicked.connect(lambda: self.set_tool_mode('cut'))
        toolbar_layout.addWidget(self.cut_btn)
        
        self.split_btn = QToolButton()
        self.split_btn.setCheckable(True)
        self.split_btn.setText("⌬")
        self.split_btn.setToolTip("Scinder")
        self.split_btn.setFixedSize(32, 32)
        self.split_btn.clicked.connect(lambda: self.set_tool_mode('split'))
        toolbar_layout.addWidget(self.split_btn)
        
        self.select_btn = QToolButton()
        self.select_btn.setCheckable(True)
        self.select_btn.setText("☐")
        self.select_btn.setToolTip("Sélectionner")
        self.select_btn.setFixedSize(32, 32)
        self.select_btn.clicked.connect(lambda: self.set_tool_mode('select'))
        toolbar_layout.addWidget(self.select_btn)
        
        toolbar_layout.addSpacing(15)
        
        # Zoom controls
        zoom_in_btn = QToolButton()
        zoom_in_btn.setText("+")
        zoom_in_btn.setToolTip("Zoom avant")
        zoom_in_btn.setFixedSize(32, 32)
        zoom_in_btn.clicked.connect(self.zoom_in)
        toolbar_layout.addWidget(zoom_in_btn)
        
        zoom_out_btn = QToolButton()
        zoom_out_btn.setText("-")
        zoom_out_btn.setToolTip("Zoom arrière")
        zoom_out_btn.setFixedSize(32, 32)
        zoom_out_btn.clicked.connect(self.zoom_out)
        toolbar_layout.addWidget(zoom_out_btn)
        
        toolbar_layout.addStretch()
        
        # Add the toolbar to the provided layout (under video preview)
        layout.addWidget(toolbar_widget)

    def zoom_in(self):
        """Handle zoom in action"""
        self.status_label.setText("État: Zoom avant")
        # In a real implementation, this would zoom in the timeline
    
    def zoom_out(self):
        """Handle zoom out action"""
        self.status_label.setText("État: Zoom arrière")
    
    def import_video(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Sélectionner une vidéo", "", "Fichiers vidéo (*.mp4 *.avi *.mov *.mkv)"
        )
        
        if file_path:
            try:
                self.source_video_path = file_path
                self.source_video = VideoFileClip(file_path)
                self.status_label.setText(f"État: Vidéo chargée - {os.path.basename(file_path)}")
                self.add_track_btn.setEnabled(True)
                self.export_btn.setEnabled(True)
                self.position_slider.setEnabled(True)
                
                # Update timeline with video duration
                self.timeline.set_duration(self.source_video.duration)
                self.position_slider.setRange(0, int(self.source_video.duration * 1000))
                self.update_time_display()
                
                # Display first frame
                self.current_play_time = 0
                self.video_preview.set_frame(None)  # In real app, you'd get the actual frame
                self.video_preview.video_duration = self.source_video.duration
                self.video_preview.current_time = 0
                
            except Exception as e:
                self.status_label.setText(f"Erreur: {str(e)}")
    
    def add_track(self):
        if not self.source_video:
            return
            
        dialog = ClipDialog(self)
        if dialog.exec() == QDialog.Accepted:
            start, end = dialog.get_values()
            
            # Validate clip range
            if end <= start:
                self.status_label.setText("Erreur: La fin doit être après le début")
                return
                
            if end > self.source_video.duration:
                end = self.source_video.duration
                self.status_label.setText(f"Avertissement: Fin ajustée à la durée maximale ({self.source_video.duration:.1f}s)")
            
            # Create track item
            track_item = QWidget()
            track_layout = QHBoxLayout(track_item)
            track_layout.setContentsMargins(5, 2, 5, 2)
            
            # Clip info
            clip_info = QLabel(f"{os.path.basename(self.source_video_path)} [{start:.1f}s - {end:.1f}s]")
            clip_info.setStyleSheet("background-color: #3a3a3a; padding: 5px; border-radius: 3px;")
            track_layout.addWidget(clip_info, 1)
            
            # Duration
            duration = end - start
            duration_label = QLabel(f"{duration:.1f}s")
            duration_label.setStyleSheet("min-width: 50px; text-align: right;")
            track_layout.addWidget(duration_label)
            
            # Add to tracks layout
            self.tracks_layout.insertWidget(self.tracks_layout.count() - 1, track_item)
            
            # Add to timeline
            self.clips.append({
                'name': os.path.basename(self.source_video_path),
                'start': start,
                'end': end
            })
            self.timeline.add_clip(self.clips[-1])
            
            self.status_label.setText(f"État: Clip ajouté à la piste [{start:.1f}s - {end:.1f}s]")
    
    def toggle_play(self):
        if not self.source_video:
            return
            
        if self.is_playing:
            self.play_timer.stop()
            self.play_btn.setText("▶")
            self.is_playing = False
        else:
            self.play_timer.start(30)  # ~33fps
            self.play_btn.setText("⏸")
            self.is_playing = True
    
    def update_playback(self):
        if not self.source_video:
            return
            
        self.current_play_time += 0.03  # 30ms per frame
        if self.current_play_time >= self.source_video.duration:
            self.current_play_time = 0
            self.play_timer.stop()
            self.play_btn.setText("▶")
            self.is_playing = False
        
        # Update UI
        self.position_slider.setValue(int(self.current_play_time * 1000))
        self.video_preview.current_time = self.current_play_time
        self.timeline.set_current_time(self.current_play_time)
        self.update_time_display()
        
        # In real app, you'd get the current frame and display it:
        # frame = self.source_video.get_frame(self.current_play_time)
        # self.video_preview.set_frame(frame)
    
    def update_time_display(self):
        if not self.source_video:
            self.time_label.setText("00:00 / 00:00")
            return
            
        current_min = int(self.current_play_time // 60)
        current_sec = int(self.current_play_time % 60)
        total_min = int(self.source_video.duration // 60)
        total_sec = int(self.source_video.duration % 60)
        
        self.time_label.setText(f"{current_min:02d}:{current_sec:02d} / {total_min:02d}:{total_sec:02d}")
    
    def undo(self):
        self.status_label.setText("État: Action annulée")
        # Implementation would track changes and revert them
    
    def redo(self):
        self.status_label.setText("État: Action refaite")
        # Implementation would redo previously undone actions
    
    def export_video(self):
        if not self.clips:
            self.status_label.setText("Erreur: Aucun clip à exporter")
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Exporter la vidéo", "", "Fichiers vidéo (*.mp4)"
        )
        
        if file_path:
            try:
                # In a real implementation, this would composite the clips and export
                self.status_label.setText(f"État: Export en cours vers {file_path}...")
                
                # Simulate export progress
                QTimer.singleShot(2000, lambda: self.status_label.setText(f"État: Vidéo exportée vers {file_path}"))
                
            except Exception as e:
                self.status_label.setText(f"Erreur d'export: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = VideoEditor()
    
    # Create menu bar
    menu_bar = editor.menuBar()
    
    # File menu
    file_menu = menu_bar.addMenu("Fichier")
    import_action = file_menu.addAction("Importer une vidéo")
    import_action.triggered.connect(editor.import_video)
    
    export_action = file_menu.addAction("Exporter la vidéo")
    export_action.triggered.connect(editor.export_video)
    export_action.setEnabled(False)
    editor.export_btn = export_action  # Store reference for enabling later
    
    file_menu.addSeparator()
    exit_action = file_menu.addAction("Quitter")
    exit_action.triggered.connect(app.quit)
    
    editor.show()
    sys.exit(app.exec())