# modules_view.py
# Modules screen view for PyLearn Desktop

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

class ModulesView(QWidget):
    """
    Modules screen view (placeholder).
    """

    # Signal emitted when the user wants to open lessons
    navigate_to_lessons = Signal()

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout()

        label = QLabel("Modules Screen")
        layout.addWidget(label)

        # Placeholder navigation button
        lessons_button = QPushButton("Open Lessons")
        lessons_button.clicked.connect(self._on_open_lessons_clicked)
        layout.addWidget(lessons_button)

        self.setLayout(layout)

    def _on_open_lessons_clicked(self) -> None:
        """Emit signal to navigate to the lessons view."""
        self.navigate_to_lessons.emit()
