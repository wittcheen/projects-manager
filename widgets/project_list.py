from utils.core import bold_font
from widgets.project_item import ProjectItem
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QListWidget, QListWidgetItem, QFrame
)
from PySide6.QtCore import Qt

class ProjectList(QWidget):
    """ Widget showing a draggable list of projects. """
    def __init__(self, keys: list, parent = None):
        super().__init__(parent)
        self.keys = keys
        layout = QHBoxLayout(self)
        self.current_editor = None

        self.list_widget = QListWidget()
        self.list_widget.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        self.list_widget.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self.list_widget.setFrameShadow(QFrame.Shadow.Plain)
        self.list_widget.setFont(bold_font())
        layout.addWidget(self.list_widget)
        self.list_widget.currentItemChanged.connect(self._on_project_changed)

        editor_frame = QFrame(
            frameShape = QFrame.Shape.StyledPanel,
            frameShadow = QFrame.Shadow.Plain
        )
        self.editor_layout = QVBoxLayout(editor_frame)
        layout.addWidget(editor_frame)

    def clear_editor(self):
        """ Remove current editor widget. """
        if self.current_editor:
            self.current_editor.setParent(None)
            self.current_editor = None

    def populate(self, projects: list):
        """ Fill list of projects. """
        for project in projects:
            self.add_project(project)

    def add_project(self, data: dict = None):
        """ Add a project; empty if no data provided. """
        item_data = data or { key: "Untitled \u00b7 Project" if key == "title" else "" for key in self.keys }
        item = QListWidgetItem(item_data.get("title", "Untitled"))
        item.setData(Qt.ItemDataRole.UserRole, item_data)

        if data is None:
            self.list_widget.insertItem(0, item)
            self.list_widget.setCurrentRow(0)
        else:
            self.list_widget.addItem(item)

    def remove_selected(self):
        """ Remove currently selected project if any. """
        # Walrus operator := assigns and tests in one expression.
        if (row := self.list_widget.currentRow()) >= 0:
            self.list_widget.takeItem(row)
            self.list_widget.clearSelection()
            self.clear_editor()

    def get_json(self) -> dict:
        """ Return dict of projects. """
        projects = []
        for i in range(self.list_widget.count()):
            stored = self.list_widget.item(i).data(Qt.ItemDataRole.UserRole)
            # Reorder according to self.keys
            projects.append({ key: stored.get(key, "") for key in self.keys })
        return { "projects": projects }

    def _on_project_changed(self, current_item, previous_item):
        """ Swap editor when selection changes, save old data. """
        self.clear_editor()
        if current_item:
            data = current_item.data(Qt.ItemDataRole.UserRole)
            editor = ProjectItem(data, self.keys)
            editor.title_changed.connect(current_item.setText)
            self.editor_layout.addWidget(editor)
            self.current_editor = editor
