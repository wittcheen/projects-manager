import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QFont

def bold_font() -> QFont:
    """ Return bold version of default font. """
    font = QApplication.instance().font()
    font.setBold(True)
    return font

class Core:
    """ Core application handler. """
    def __init__(self, main_window: QMainWindow):
        self.app = QApplication(sys.argv)
        self.window = main_window()

    def run(self):
        """ Start application event loop. """
        self.__center_window()
        self.window.show()
        sys.exit(self.app.exec())

    def __center_window(self):
        """ Center window on user's screen. """
        geometry = self.window.frameGeometry()
        center = self.app.primaryScreen().availableGeometry().center()
        geometry.moveCenter(center)
        self.window.move(geometry.topLeft())
