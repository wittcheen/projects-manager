from utils.core import Core, JSON_KEYS
from utils.session import FTPSession
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QMessageBox
)
from widgets.login_panel import LoginPanel
from widgets.project_list import ProjectList
from widgets.action_row import ActionRow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.session = None
        self.setWindowTitle("Projects Manager")
        self.setMinimumSize(650, 350)
        self.resize(1000, 550)

        self.setCentralWidget(QWidget())
        layout = QVBoxLayout(self.centralWidget())
        layout.setSpacing(11)

        self.login_panel = LoginPanel()
        layout.addWidget(self.login_panel)
        self.login_panel.login_clicked.connect(self._on_login)
        self.login_panel.logout_clicked.connect(self._on_logout)
        QApplication.instance().aboutToQuit.connect(self._on_logout)

        self.project_list = ProjectList(JSON_KEYS)
        layout.addWidget(self.project_list)

        self.action_row = ActionRow(self.project_list)
        layout.addWidget(self.action_row)
        self.action_row.save_clicked.connect(self._save_changes_to_ftp)

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

    def _save_changes_to_ftp(self):
        """ Save current projects to the FTP server. """
        try:
            self.session.save_json(self.project_list.get_json())
            QMessageBox.information(self, "Success", "File saved successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Save Failed", str(e))

    def _update_ui_state(self):
        """ Enable or disable UI based on login state. """
        logged_in = self.session is not None
        self.login_panel.set_enabled(not logged_in)
        self.action_row.set_enabled(logged_in)


if __name__ == "__main__":
    Core(MainWindow).run()
