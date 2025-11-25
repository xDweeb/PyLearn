# lessons_view.py
# Lessons screen view for PyLearn Desktop

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

class LessonsView(QWidget):
    """
    Lessons screen view (placeholder).
    """

    # Signal emitted when the user wants to open tasks
    navigate_to_tasks = Signal()

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout()

        label = QLabel("Lessons Screen")
        layout.addWidget(label)

        # Placeholder navigation button
        tasks_button = QPushButton("Open Tasks")
        tasks_button.clicked.connect(self._on_open_tasks_clicked)
        layout.addWidget(tasks_button)

        self.setLayout(layout)

    def _on_open_tasks_clicked(self) -> None:
        """Emit signal to navigate to the tasks view."""
        self.navigate_to_tasks.emit()
