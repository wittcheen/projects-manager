import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.session = None
        self.setWindowTitle("Projects Manager")
        self.setMinimumSize(650, 350)
        self.resize(1000, 600)

        self.setCentralWidget(QWidget())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
