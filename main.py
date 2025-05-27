from utils.core import Core
from PySide6.QtWidgets import QMainWindow, QStackedWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Projects Manager")
        self.stack = QStackedWidget(self)
        self.setCentralWidget(self.stack)

if __name__ == "__main__":
    core = Core(MainWindow)
    core.run_app()
