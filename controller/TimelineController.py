from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtGui import Qt, QPainter, QBrush, QColor, QWheelEvent, QMouseEvent
from PySide6.QtCore import QEvent
import math

from views.TimelineWidget import TimelineWidget
from views.PlayHead import PlayHead

class TimelineController(QWidget):
    """Controller managing a list of timelines, shared zoom, scroll, and time scale."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.video_duration = 0.0
        self.current_time = 0.0
        self.zoom_factor = 1.0   # 1.0 = full video visible
        self.scroll_offset = 0.0 # in seconds

        # Zoom feedback
        self._zoom_feedback_text = None
        self._zoom_feedback_opacity = 0.0
        self._zoom_feedback_timer = None

        # Interaction
        self.dragging = False
        self.last_mouse_x = None

        # List of timelines
        self.timelines = []

        # Layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Playhead widget (global)
        self.playhead = PlayHead(self)
        self.layout.addWidget(self.playhead)

        # Time scale widget (affiche la graduation du temps)
        self.time_scale_widget = QWidget(self)
        self.time_scale_widget.setFixedHeight(40)
        self.time_scale_widget.paintEvent = self.paint_time_scale
        self.layout.addWidget(self.time_scale_widget)

        # Container for timelines
        self.timelines_container = QWidget(self)
        self.timelines_layout = QVBoxLayout(self.timelines_container)
        self.timelines_layout.setContentsMargins(0, 0, 0, 0)
        self.timelines_layout.setSpacing(5)  # Match PlayHead spacing
        self.layout.addWidget(self.timelines_container)

        # Event filter pour capter la molette sur l'échelle et la zone des timelines
        self.time_scale_widget.installEventFilter(self)
        self.timelines_container.installEventFilter(self)

        # Zoom limits
        self._min_zoom = 1.0
        self._max_zoom = 100.0

    # --------------------------
    # Gestion des timelines
    # --------------------------
    def addTimeline(self):
        """Add a new unique timeline."""
        timeline = TimelineWidget(self.timelines_container)
        timeline.setDuration(self.video_duration)
        timeline.currentTimeChanged.connect(self.sync_current_time)
        self.timelines.append(timeline)
        self.timelines_layout.addWidget(timeline)
        self.playhead.setTimelineWidgets(self.timelines)
        self.playhead.setDuration(self.video_duration)
        self.update_all()
        return timeline

    def setDuration(self, duration):
        """Set the total video duration for all timelines and playhead."""
        self.video_duration = float(duration)
        self.playhead.setDuration(self.video_duration)
        for timeline in self.timelines:
            timeline.setDuration(self.video_duration)
        # clamp scroll_offset if needed
        self._clamp_scroll()
        self.update_all()

    def sync_current_time(self, time):
        """Sync current time across all timelines and playhead."""
        self.current_time = time
        self.playhead.setCurrentTime(time)
        for timeline in self.timelines:
            timeline.current_time = time  # Direct set to avoid signal loop
        self.update_all()

    # ==========================
    # Contrôles Zoom & Scroll
    # ==========================
    def zoomIn(self, center_time=None, center_px=None, width=None):
        old_zoom = self.zoom_factor
        self.zoom_factor = min(self.zoom_factor * 1.25, self._max_zoom)
        if center_time is not None and width:
            self._recenter_after_zoom(center_time, center_px, width, old_zoom, self.zoom_factor)
        self.show_zoom_feedback()   # <<< feedback
        self.update_all()

    def zoomOut(self, center_time=None, center_px=None, width=None):
        old_zoom = self.zoom_factor
        self.zoom_factor = max(self.zoom_factor / 1.25, self._min_zoom)
        if center_time is not None and width:
            self._recenter_after_zoom(center_time, center_px, width, old_zoom, self.zoom_factor)
        self.show_zoom_feedback()   # <<< feedback
        self.update_all()

    def _recenter_after_zoom(self, center_time, center_px, width, old_zoom, new_zoom):
        """Adjust scroll_offset so that center_time stays under center_px after zoom."""
        if width <= 0 or self.video_duration <= 0:
            return
        new_visible = self.video_duration / new_zoom
        rel = (center_px / width)  # relative position [0..1]
        new_start = center_time - rel * new_visible
        # clamp
        max_offset = max(0.0, self.video_duration - new_visible)
        self.scroll_offset = max(0.0, min(new_start, max_offset))
        self._clamp_scroll()

    def scrollLeft(self, factor=0.1):
        visible_duration = self.video_duration / self.zoom_factor if self.zoom_factor > 0 else self.video_duration
        self.scroll_offset = max(0.0, self.scroll_offset - visible_duration * factor)
        self._clamp_scroll()
        self.update_all()

    def scrollRight(self, factor=0.1):
        visible_duration = self.video_duration / self.zoom_factor if self.zoom_factor > 0 else self.video_duration
        max_offset = max(0.0, self.video_duration - visible_duration)
        self.scroll_offset = min(max_offset, self.scroll_offset + visible_duration * factor)
        self._clamp_scroll()
        self.update_all()

    def _clamp_scroll(self):
        if self.video_duration <= 0:
            self.scroll_offset = 0.0
            return
        visible = self.video_duration / self.zoom_factor
        max_offset = max(0.0, self.video_duration - visible)
        self.scroll_offset = max(0.0, min(self.scroll_offset, max_offset))

    # ==========================
    # Événements souris & molette
    # ==========================
    def eventFilter(self, obj, event):
        """Catch wheel events coming from child widgets (time scale or timelines)."""
        if event.type() == QEvent.Wheel:
            # On récupère la position locale où la molette se produit
            pos = event.position()  # QPointF
            width = obj.width() if obj is not None else self.width()
            # Déléguer au handler central (ctrl+wheel -> zoom autour du pointeur, sinon scroll)
            self._handle_wheel(event, local_x=pos.x(), widget=obj, widget_width=width)
            return True  # on consomme l'événement
        return super().eventFilter(obj, event)

    def _handle_wheel(self, event: QWheelEvent, local_x: float, widget, widget_width: int):
        """Wheel handling: Ctrl+wheel = zoom around cursor; else pan horizontally."""
        if self.video_duration <= 0 or widget_width <= 0:
            return

        delta = event.angleDelta().y()
        steps = delta / 120.0  # standard step unit

        if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            # zoom centered on mouse position
            # calculer le temps sous le pointeur avant zoom
            time_at_cursor = self.xToTime(local_x, width=widget_width)
            if steps > 0:
                # zoom in multiple steps
                for _ in range(int(abs(steps))):
                    self.zoomIn(center_time=time_at_cursor, center_px=local_x, width=widget_width)
            else:
                for _ in range(int(abs(steps))):
                    self.zoomOut(center_time=time_at_cursor, center_px=local_x, width=widget_width)
            # update_all est appelé dans zoomIn/Out
        else:
            # simple scroll/pan: plus la valeur de zoom, plus un pas correspond à beaucoup de secondes
            visible_duration = self.video_duration / self.zoom_factor if self.zoom_factor > 0 else self.video_duration
            # utiliser fraction des ticks déjà utilisés ailleurs (10% du visible par step)
            shift = -steps * visible_duration * 0.1
            self.scroll_offset = max(0.0, min(self.video_duration - visible_duration, self.scroll_offset + shift))
            self.update_all()

    def wheelEvent(self, event: QWheelEvent):
        """Fallback: si le controller reçoit la molette (rare, car on utilise eventFilter)."""
        self._handle_wheel(event, local_x=event.position().x(), widget=self, widget_width=self.width())

    def mousePressEvent(self, event: QMouseEvent):
        """Drag for pan, left-click for playhead."""
        if event.button() == Qt.MouseButton.MiddleButton:
            self.dragging = True
            self.last_mouse_x = event.x()
        elif event.button() == Qt.MouseButton.LeftButton:
            pos = self.timelines_container.mapFromParent(event.pos())
            for timeline in self.timelines:
                if timeline.underMouse():
                    local_x = timeline.mapFromParent(pos).x()
                    time = timeline.xToTime(local_x, self.zoom_factor, self.scroll_offset)
                    self.sync_current_time(time)
                    break
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.dragging and self.last_mouse_x is not None:
            dx = event.x() - self.last_mouse_x
            visible_duration = self.video_duration / self.zoom_factor if self.zoom_factor > 0 else self.video_duration
            seconds_per_px = visible_duration / self.width() if self.width() > 0 else 0
            self.scroll_offset = max(0.0, self.scroll_offset - dx * seconds_per_px)
            self._clamp_scroll()
            self.last_mouse_x = event.x()
            self.update_all()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.MiddleButton:
            self.dragging = False
            self.last_mouse_x = None

    # ==========================
    # Rendu de l’échelle du temps
    # ==========================
    def paint_time_scale(self, event):
        painter = QPainter(self.time_scale_widget)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.TextAntialiasing)
        rect = self.time_scale_widget.rect()

        # Fond
        painter.setBrush(QBrush(QColor(40, 40, 40)))
        painter.drawRect(rect)

        if self.video_duration <= 0 or rect.width() <= 0:
            return

        total_pixels = rect.width()

        # Durée visible à l'écran (en secondes)
        visible_duration = self.video_duration / self.zoom_factor
        visible_start = self.scroll_offset
        visible_end = visible_start + visible_duration

        if visible_duration <= 0:
            return

        pixels_per_second = total_pixels / visible_duration

        # Choisir un intervalle "propre" (1,2,5,10,15,30,60,120,300...)
        target_px_per_tick = 80  # visé ~80px entre ticks
        seconds_target = target_px_per_tick / pixels_per_second
        tick = self._nice_time_interval(seconds_target)

        painter.setPen(QColor(200, 200, 200))

        # trouver premier tick aligné
        first_tick = math.floor(visible_start / tick) * tick
        # itérer en utilisant des steps = tick
        t = int(first_tick)
        # dessiner ticks et labels
        while t <= int(math.ceil(visible_end)):
            if t >= visible_start:
                x = (t - visible_start) * pixels_per_second
                ix = int(round(x))
                # ligne courte pour tick, plus longue pour ticks majeurs (par ex. divisibles par 60)
                if t % (tick * 5) == 0:
                    painter.drawLine(ix, rect.height() - 28, ix, rect.height())
                else:
                    painter.drawLine(ix, rect.height() - 20, ix, rect.height())

                # label tous les ticks majeurs (par ex. toutes les minutes ou tous les 5 ticks)
                if tick >= 60:
                    # si tick >= 1 minute, afficher en mm:ss
                    minutes = int(t // 60)
                    seconds = int(t % 60)
                    painter.drawText(ix + 3, rect.height() - 32, f"{minutes}:{seconds:02d}")
                else:
                    # small ticks -> afficher sec
                    if (t % (tick * 5)) == 0:
                        painter.drawText(ix + 3, rect.height() - 32, f"{t}s")
            t += int(tick)

        # repère du playhead sur l'échelle de temps
        if visible_start <= self.current_time <= visible_end:
            x_play = (self.current_time - visible_start) * pixels_per_second
            painter.setPen(QColor("red"))
            ixp = int(round(x_play))
            painter.drawLine(ixp, 0, ixp, rect.height())

        # --- Feedback Zoom ---
        if self._zoom_feedback_text and self._zoom_feedback_opacity > 0:
            painter.setPen(QColor(255, 255, 255, int(255 * self._zoom_feedback_opacity)))
            font = painter.font()
            font.setPointSize(12)
            font.setBold(True)
            painter.setFont(font)
            text_rect = rect
            painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, self._zoom_feedback_text)

    def _nice_time_interval(self, seconds_target):
        """Choisit un intervalle 'résonnable' >= seconds_target parmi une liste."""
        if seconds_target <= 0:
            return 1
        candidates = [1, 2, 5, 10, 15, 30, 60, 120, 300, 600, 900, 1800, 3600]
        for c in candidates:
            if c >= seconds_target:
                return c
        return candidates[-1]
    

    # --------------------------
    # Feedback Zoom
    # --------------------------
    def show_zoom_feedback(self):
        """Affiche un texte temporaire avec le niveau de zoom."""
        self._zoom_feedback_text = f"Zoom: {self.zoom_factor:.2f}x"
        self._zoom_feedback_opacity = 1.0

        if self._zoom_feedback_timer is not None:
            self._zoom_feedback_timer.stop()

        self._zoom_feedback_timer = QTimer(self)
        self._zoom_feedback_timer.setInterval(50)  # 20 FPS fade
        self._zoom_feedback_timer.timeout.connect(self._fade_zoom_feedback)
        self._zoom_feedback_timer.start()

        self.time_scale_widget.update()

    def _fade_zoom_feedback(self):
        """Diminue progressivement l'opacité du feedback."""
        self._zoom_feedback_opacity -= 0.05
        if self._zoom_feedback_opacity <= 0:
            self._zoom_feedback_opacity = 0.0
            self._zoom_feedback_text = None
            if self._zoom_feedback_timer:
                self._zoom_feedback_timer.stop()
                self._zoom_feedback_timer = None
        self.time_scale_widget.update()

    # ==========================
    # Conversion X <-> temps
    # ==========================
    def xToTime(self, x, width=None):
        """Convert X (px) to time (s). width par défaut = width du widget d'échelle si possible."""
        if width is None:
            width = self.time_scale_widget.width() if self.time_scale_widget is not None else self.width()
        if width == 0 or self.zoom_factor <= 0:
            return 0.0
        visible_duration = self.video_duration / self.zoom_factor
        start_time = self.scroll_offset
        return (x / width) * visible_duration + start_time

    def timeToX(self, t, width=None):
        if width is None:
            width = self.time_scale_widget.width() if self.time_scale_widget is not None else self.width()
        if self.video_duration == 0 or self.zoom_factor <= 0:
            return 0
        visible_duration = self.video_duration / self.zoom_factor
        start_time = self.scroll_offset
        return int(round(((t - start_time) / visible_duration) * width))

    # ==========================
    # Mise à jour globale
    # ==========================
    def update_all(self):
        """Update playhead, time scale, and all timelines."""
        # D'abord propager la durée/zoom/scroll aux timelines
        for timeline in self.timelines:
            timeline.setZoomAndScroll(self.zoom_factor, self.scroll_offset)
        # puis redessiner playhead et time scale
        self.playhead.update()
        self.time_scale_widget.update()
        # et enfin redessiner les timelines
        for timeline in self.timelines:
            timeline.update()
