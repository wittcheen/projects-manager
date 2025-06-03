import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMainWindow

class Core:
    """ Core application handler. """
    def __init__(self, main_window: QMainWindow):
        self.app = QApplication(sys.argv)
        self.window = main_window()

    def run_app(self):
        """ Start application event loop. """
        self.window.resize(600, 400)
        self._center_window()
        self.window.show()
        sys.exit(self.app.exec())

    def _center_window(self):
        """ Center main window on user's primary screen. """
        _geometry = self.window.frameGeometry()
        _center = self.app.primaryScreen().availableGeometry().center()
        _geometry.moveCenter(_center)
        self.window.move(_geometry.topLeft())
