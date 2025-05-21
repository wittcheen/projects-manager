import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Projects Manager")

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(600, 400)
    window.show()
    sys.exit(app.exec())
