from PySide6.QtWidgets import QApplication
import sys
import VideoEditor

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