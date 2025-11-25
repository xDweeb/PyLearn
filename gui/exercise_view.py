# exercise_view.py
# Exercise screen view for PyLearn Desktop

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class ExerciseView(QWidget):
    """Exercise screen view (placeholder)."""

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel("Exercise Screen")
        layout.addWidget(label)
        self.setLayout(layout)
