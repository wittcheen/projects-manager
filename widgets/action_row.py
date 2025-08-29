from utils.core import bold_font
from widgets.project_list import ProjectList
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QPushButton
)
from PySide6.QtCore import Qt, Signal
from functools import partial

class ActionRow(QWidget):
    """ Widget containing action buttons. """
    save_clicked = Signal()

    def __init__(self, project_list: ProjectList, parent = None):
        super().__init__(parent)
        layout = QHBoxLayout(self)

        # (Button label, associated handler)
        button_list = [
            ("Add Project", project_list.add_project),
            ("Remove Selected", project_list.remove_selected),
            ("Save Changes", self.save_clicked)
        ]

        self._buttons = []
        for i, (label, handler) in enumerate(button_list):
            button = QPushButton(label, flat = True, minimumHeight = 30, minimumWidth = 130)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.setFont(bold_font())
            if hasattr(handler, "emit"):
                button.clicked.connect(handler.emit)
            else:
                button.clicked.connect(partial(handler))

            if i == len(button_list) - 1:
                layout.addStretch()
            layout.addWidget(button)
            self._buttons.append(button)

    def set_enabled(self, enabled: bool):
        """ Enable or disable all buttons. """
        for button in self._buttons:
            button.setEnabled(enabled)
