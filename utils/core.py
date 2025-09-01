import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QFont, QIcon
from pathlib import Path

JSON_KEYS = [ "title", "link", "tags", "description" ]

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
        self.app.setWindowIcon(QIcon(self.__get_icon_path()))
        self.window.show()
        sys.exit(self.app.exec())

    def __center_window(self):
        """ Center window on user's screen. """
        geometry = self.window.frameGeometry()
        center = self.app.primaryScreen().availableGeometry().center()
        geometry.moveCenter(center)
        self.window.move(geometry.topLeft())

    def __get_icon_path(self) -> str:
        """ Return absolute path to the app icon. """
        if getattr(sys, "frozen", False):
            # Running as a bundled executable (PyInstaller)
            base_path = Path(sys._MEIPASS)  # type: ignore[attr-defined]
        else:
            # Running as a script
            base_path = Path(sys.modules["__main__"].__file__).resolve().parent
        return str(base_path / "icon.ico")
