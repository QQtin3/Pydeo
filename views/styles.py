"""
Styles for Pydeo Video Editor
Contains all CSS styles and color definitions
"""

class PydeoStyles:
    """Class containing all styles for the Pydeo application"""
    
    # Color palette
    COLORS = {
        'primary': '#1a1a2e',      # Main background
        'secondary': '#16213e',    # Secondary background
        'accent': '#0f3460',       # Accent blue
        'highlight': '#e94560',    # Red/pink highlight
        'text': '#ffffff',         # White text
        'text_secondary': '#b0b0b0', # Secondary text
        'success': '#4caf50',      # Green success
        'warning': '#ff9800',      # Orange warning
        'error': '#f44336',        # Red error
        'border': '#2a2a3e',       # Borders
        'hover': '#2a2a4e',        # Hover effects
        'timeline_bg': '#1a1a2e',  # Timeline background
        'timeline_clip': '#16213e', # Timeline clips
        'playhead': '#81B6E6',     # Playhead color
        'button_blue': '#2E3F69',  # Button background
        'button_border': '#4551AB', # Button border
        'button_hover': '#81B6E6', # Button hover
    }
    
    @staticmethod
    def get_main_stylesheet() -> str:
        """Returns the main application stylesheet"""
        return f"""
        /* Main Application */
        QMainWindow {{
            background-color: {PydeoStyles.COLORS['primary']};
            color: {PydeoStyles.COLORS['text']};
        }}
        
        QWidget {{
            background-color: {PydeoStyles.COLORS['primary']};
            color: {PydeoStyles.COLORS['text']};
        }}
        
        /* Buttons */
        QPushButton {{
            background-color: {PydeoStyles.COLORS['button_blue']};
            border: 2px solid {PydeoStyles.COLORS['button_border']};
            border-radius: 8px;
            padding: 8px 16px;
            font-weight: bold;
            color: {PydeoStyles.COLORS['text']};
        }}
        
        QPushButton:hover {{
            background-color: {PydeoStyles.COLORS['button_border']};
            border-color: {PydeoStyles.COLORS['button_hover']};
        }}
        
        QPushButton:pressed {{
            background-color: {PydeoStyles.COLORS['button_hover']};
        }}
        
        QPushButton:disabled {{
            background-color: {PydeoStyles.COLORS['border']};
            border-color: {PydeoStyles.COLORS['border']};
            color: {PydeoStyles.COLORS['text_secondary']};
        }}
        
        /* Play Button */
        QPushButton#play_button {{
            background-color: {PydeoStyles.COLORS['button_hover']};
            border-color: {PydeoStyles.COLORS['button_hover']};
            font-size: 12px;
            min-width: 10px;
            min-height: 10px;
            border-radius: 8px;
        }}
        
        QPushButton#play_button:hover {{
            background-color: #92B2D9;
            border-color: #92B2D9;
        }}
        
        /* Toolbar */
        QToolBar {{
            background-color: {PydeoStyles.COLORS['button_blue']};
            border: 2px solid {PydeoStyles.COLORS['button_border']};
            border-radius: 8px;
            spacing: 3px;
            padding: 5px;
        }}
        
        QWidget#toolbar_widget {{
            background-color: {PydeoStyles.COLORS['button_blue']};
            border-top: 1px solid {PydeoStyles.COLORS['button_border']};
            border-bottom: 1px solid {PydeoStyles.COLORS['button_border']};
            border-radius: 8px;
            padding: 5px;
        }}
        
        QToolButton {{
            background-color: transparent;
            border: 1px solid transparent;
            border-radius: 6px;
            padding: 8px;
            margin: 2px;
            color: {PydeoStyles.COLORS['text']};
            font-size: 14px;
            font-weight: bold;
        }}
        
        QToolButton:hover {{
            background-color: {PydeoStyles.COLORS['button_border']};
            border-color: {PydeoStyles.COLORS['button_hover']};
            color: {PydeoStyles.COLORS['text']};
        }}
        
        QToolButton:pressed {{
            background-color: {PydeoStyles.COLORS['button_hover']};
            color: {PydeoStyles.COLORS['text']};
        }}
        
        QToolButton:checked {{
            background-color: {PydeoStyles.COLORS['button_hover']};
            border-color: {PydeoStyles.COLORS['button_hover']};
            color: {PydeoStyles.COLORS['text']};
        }}
        
        /* Labels */
        QLabel {{
            color: {PydeoStyles.COLORS['text']};
        }}
        
        /* Sliders */
        QSlider::groove:horizontal {{
            border: 1px solid {PydeoStyles.COLORS['button_border']};
            height: 8px;
            background: {PydeoStyles.COLORS['button_blue']};
            border-radius: 4px;
        }}
        
        QSlider::handle:horizontal {{
            background: {PydeoStyles.COLORS['button_hover']};
            border: 1px solid {PydeoStyles.COLORS['button_hover']};
            width: 18px;
            margin: -5px 0;
            border-radius: 9px;
        }}
        
        QSlider::handle:horizontal:hover {{
            background: #92B2D9;
            border-color: #92B2D9;
        }}
        
        /* Video Preview */
        QWidget#video_preview {{
            background-color: #000000;
            border: 3px solid {PydeoStyles.COLORS['button_border']};
            border-radius: 10px;
        }}
        
        /* Timeline */
        QWidget#timeline {{
            background-color: {PydeoStyles.COLORS['timeline_bg']};
            border: 1px solid {PydeoStyles.COLORS['button_border']};
            border-radius: 8px;
        }}
        
        /* Scroll Areas */
        QScrollArea {{
            background-color: {PydeoStyles.COLORS['secondary']};
            border: 1px solid {PydeoStyles.COLORS['button_border']};
            border-radius: 6px;
        }}
        
        QScrollBar:vertical {{
            background-color: {PydeoStyles.COLORS['secondary']};
            width: 12px;
            border-radius: 6px;
        }}
        
        QScrollBar::handle:vertical {{
            background-color: {PydeoStyles.COLORS['button_border']};
            border-radius: 6px;
            min-height: 20px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background-color: {PydeoStyles.COLORS['button_hover']};
        }}
        
        /* Menu Bar */
        QMenuBar {{
            background-color: {PydeoStyles.COLORS['secondary']};
            border-bottom: 1px solid {PydeoStyles.COLORS['button_border']};
            color: {PydeoStyles.COLORS['text']};
        }}
        
        QMenuBar::item {{
            background-color: transparent;
            padding: 8px 12px;
            border-radius: 4px;
        }}
        
        QMenuBar::item:selected {{
            background-color: {PydeoStyles.COLORS['hover']};
        }}
        
        QMenu {{
            background-color: {PydeoStyles.COLORS['secondary']};
            border: 1px solid {PydeoStyles.COLORS['button_border']};
            border-radius: 6px;
        }}
        
        QMenu::item {{
            padding: 8px 20px;
            border-radius: 4px;
        }}
        
        QMenu::item:selected {{
            background-color: {PydeoStyles.COLORS['button_hover']};
        }}
        
        /* Dialogs */
        QDialog {{
            background-color: {PydeoStyles.COLORS['primary']};
            border: 2px solid {PydeoStyles.COLORS['button_border']};
            border-radius: 10px;
        }}
        
        /* SpinBoxes */
        QSpinBox, QDoubleSpinBox {{
            background-color: {PydeoStyles.COLORS['secondary']};
            border: 2px solid {PydeoStyles.COLORS['button_border']};
            border-radius: 6px;
            padding: 6px;
            color: {PydeoStyles.COLORS['text']};
        }}
        
        QSpinBox:focus, QDoubleSpinBox:focus {{
            border-color: {PydeoStyles.COLORS['button_hover']};
        }}
        
        /* Tab Widget */
        QTabWidget::pane {{
            border: 1px solid {PydeoStyles.COLORS['button_border']};
            background: {PydeoStyles.COLORS['secondary']};
            border-radius: 6px;
        }}
        
        QTabBar {{
            background: {PydeoStyles.COLORS['button_blue']};
        }}
        
        QTabBar::tab {{
            background: {PydeoStyles.COLORS['button_blue']};
            border: 1px solid {PydeoStyles.COLORS['button_border']};
            padding: 8px 12px;
            margin-right: 2px;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
            color: {PydeoStyles.COLORS['text']};
        }}
        
        QTabBar::tab:selected {{
            background: {PydeoStyles.COLORS['button_border']};
            border-bottom-color: {PydeoStyles.COLORS['secondary']};
        }}
        
        QTabBar::tab:hover {{
            background: {PydeoStyles.COLORS['button_hover']};
        }}
        """
    
    @staticmethod
    def get_timeline_stylesheet():
        """Returns timeline-specific styles"""
        return f"""
        QFrame#timeline_frame {{
            background-color: {PydeoStyles.COLORS['timeline_bg']};
            border: 2px solid {PydeoStyles.COLORS['button_border']};
            border-radius: 8px;
        }}
        
        QFrame#track_frame {{
            background-color: {PydeoStyles.COLORS['primary']};
            border: 1px solid {PydeoStyles.COLORS['border']};
            border-radius: 4px;
            margin: 2px;
        }}
        
        QFrame#clip_frame {{
            background-color: {PydeoStyles.COLORS['timeline_clip']};
            border: 1px solid {PydeoStyles.COLORS['text']};
            border-radius: 3px;
        }}
        """
    
    @staticmethod
    def get_animation_stylesheet():
        """Returns styles with animations"""
        return """
        QPushButton {
            transition: all 0.2s ease;
        }
        
        QPushButton:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(129, 182, 230, 0.3);
        }
        
        QSlider::handle:horizontal {
            transition: all 0.1s ease;
        }
        
        QSlider::handle:horizontal:hover {
            transform: scale(1.1);
        }
        """
    
    @staticmethod
    def get_all_styles():
        """Returns all styles combined"""
        return (PydeoStyles.get_main_stylesheet() + 
                PydeoStyles.get_timeline_stylesheet() + 
                PydeoStyles.get_animation_stylesheet())
