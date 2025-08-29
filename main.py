from utils.core import Core, JSON_KEYS
from utils.session import FTPSession
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QMessageBox
)
from widgets.login_panel import LoginPanel
from widgets.project_list import ProjectList

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.session = None
        self.setWindowTitle("Projects Manager")
        self.setMinimumSize(650, 350)
        self.resize(1000, 600)

        self.setCentralWidget(QWidget())
        layout = QVBoxLayout(self.centralWidget())

        self.login_panel = LoginPanel()
        layout.addWidget(self.login_panel)
        self.login_panel.login_clicked.connect(self._on_login)
        self.login_panel.logout_clicked.connect(self._on_logout)
        QApplication.instance().aboutToQuit.connect(self._on_logout)

        self.project_list = ProjectList(JSON_KEYS)
        layout.addWidget(self.project_list)

        self._update_ui_state()

    def _on_login(self, session: FTPSession):
        """ Handle successful login and load data. """
        self.session = session
        self._update_ui_state()
        try:
            data = self.session.load_json()
            self.project_list.populate(data.get("projects", []))
            self._update_ui_state()
        except Exception as e:
            QMessageBox.critical(self, "Load Error", f"Failed to load projects: {e}")
            self._on_logout()

    def _on_logout(self):
        """ Handle logout and reset UI. """
        if self.session:
            self.session.disconnect()
        self.session = None
        self.project_list.list_widget.clear()
        self._update_ui_state()

    def _update_ui_state(self):
        """ Enable or disable UI based on login state. """
        logged_in = self.session is not None
        self.login_panel.set_enabled(not logged_in)


if __name__ == "__main__":
    Core(MainWindow).run()
