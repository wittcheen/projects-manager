from utils.core import bold_font
from utils.session import FTPSession
from utils.keyvault import KeyVault
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QLineEdit, QLabel, QPushButton, QMessageBox
)
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtCore import Qt, Signal, QRegularExpression

ALLOWED_CHARS = r"[A-Za-z0-9!?@#$%^&*\-_.]*"

class LoginPanel(QWidget):
    """ Login widget for FTP connections. """
    login_clicked = Signal(object)
    logout_clicked = Signal()

    def __init__(self, parent = None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        validator = QRegularExpressionValidator(QRegularExpression(ALLOWED_CHARS))

        self.host_field = QLineEdit(frame = False)
        self.username_field = QLineEdit(frame = False)
        self.password_field = QLineEdit(frame = False, echoMode = QLineEdit.EchoMode.Password)

        self.action_button = QPushButton("Connect", flat = True, fixedHeight = 24, minimumWidth = 110)
        self.action_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.action_button.setFont(bold_font())

        field_list = [
            ("Host:", self.host_field),
            ("Username:", self.username_field),
            ("Password:", self.password_field)
        ]

        self._fields = []
        for label, field in field_list:
            layout.addWidget(QLabel(label, font = bold_font()))
            field.setValidator(validator)
            layout.addWidget(field)
            self._fields.append(field)
        self._load_credentials()

        layout.addWidget(self.action_button)
        self.action_button.clicked.connect(self._on_connect_action)
        self.password_field.returnPressed.connect(self._on_connect_action)

    def _load_credentials(self):
        """ Load credentials from the keyvault and populate fields. """
        self.stored_creds = KeyVault.retrieve()
        if self.stored_creds:
            self.host_field.setText(self.stored_creds.get("host", ""))
            self.username_field.setText(self.stored_creds.get("username", ""))
            self.password_field.setText(self.stored_creds.get("password", ""))

    def _on_connect_action(self):
        """ Handle the connect or disconnect action. """
        if self.action_button.text() == "Connect":
            host, username, password = (field.text() for field in self._fields)
            session = FTPSession(host, username, password)
            try:
                session.connect()
                if self.stored_creds != session.to_dict():
                    KeyVault.store(session.to_dict())
                self.login_clicked.emit(session)
            except Exception as e:
                QMessageBox.warning(self, "Login Failed", str(e))
        else:
            self.logout_clicked.emit()

    def set_enabled(self, enabled: bool):
        """ Enable or disable all fields. """
        self.action_button.setText("Connect" if enabled else "Disconnect")
        for field in self._fields:
            field.setEnabled(enabled)
