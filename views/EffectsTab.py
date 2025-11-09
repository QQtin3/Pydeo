from PySide6.QtWidgets import (QWidget, QVBoxLayout,
                               QPushButton, QLabel)

from model.Effects import VideoEffect, VideoEffectEnum


class EffectsTab(QWidget):
    """Tab for video effects"""

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)

        self.timelineController = None  # défini par VideoEditor

        # Add some placeholder effect controls
        effects_label = QLabel("Liste des effets disponibles:")
        effects_label.setStyleSheet("font-weight: bold; color: #ccc;")
        layout.addWidget(effects_label)

        self.effects = {
            "N&B": VideoEffectEnum.BLACK_AND_WHITE,
            "Rotation": VideoEffectEnum.ROTATION,
            "Contraste": VideoEffectEnum.CONTRAST,
            "Saturation": VideoEffectEnum.SATURATION,
            "Zoom": VideoEffectEnum.SPEED,
            "Fondu": None,
            "Dissolution": None,
            "Luminosité": None,
        }

        for effect_name, effect_enum in self.effects.items():
            btn = QPushButton(effect_name)
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
            btn.clicked.connect(lambda _, name=effect_name, eff=effect_enum: self.apply_effect(name, eff))
            layout.addWidget(btn)

        layout.addStretch()
        self.setLayout(layout)

    def apply_effect(self, name, effect_enum):
        """Store selected effect in the selected clip"""
        if not self.timelineController:
            print("[EffectsTab] No timeline controller connected.")
            return

        clip = getattr(self.timelineController, "selectedClip", None)
        if not clip:
            print("[EffectsTab] No clip selected.")
            return

        if effect_enum is None:
            print(f"[EffectsTab] Effect '{name}' not implemented yet.")
            return

        # Store the effect in the clip's model
        clip.effects.append(VideoEffect(effect_enum, {}))
        print(f"[EffectsTab] Applied {name} to clip '{clip.title}'")

        self.timelineController.videoPreviewController.refreshPreview(clip)
