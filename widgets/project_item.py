from utils.core import bold_font
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QLabel, QTextEdit
)
from PySide6.QtGui import QTextOption, QKeyEvent
from PySide6.QtCore import Qt, Signal

class SingleLineTextEdit(QTextEdit):
    """ Custom `QTextEdit` that blocks Enter/Return keys. """
    def __init__(self, row: int = 3, parent = None):
        super().__init__(parent)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWordWrapMode(QTextOption.WrapMode.WrapAtWordBoundaryOrAnywhere)
        self.setFixedHeight(self.fontMetrics().height() * row + 12)

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() not in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            super().keyPressEvent(event)


class ProjectItem(QWidget):
    """ Widget for editing project data. """
    title_changed = Signal(str)

    def __init__(self, data: dict, keys: list, parent = None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        placeholder_map = {
            "title": "enter the project title",
            "link": "paste a valid url (https://...)",
            "tags": "separate tags with commas",
            "description": "describe the project briefly..."
        }

        self._fields = {}
        for key in keys:
            value = data.get(key, "")
            if key == "description":
                field = SingleLineTextEdit()
                field.setPlainText(value)
            else:
                field = QLineEdit(value)
            layout.addWidget(QLabel(f"{key.capitalize()}:", font = bold_font()))
            field.setPlaceholderText(placeholder_map.get(key, ""))
            layout.addWidget(field)
            layout.addSpacing(12)
            self._fields[key] = field

        layout.addStretch()

    def get_data(self) -> dict:
        """ Return current values from all fields. """
        return {
            key: (widget.toPlainText() if isinstance(widget, QTextEdit) else widget.text())
            for key, widget in self._fields.items()
        }
