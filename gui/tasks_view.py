# tasks_view.py
# Tasks screen view for PyLearn Desktop

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

class TasksView(QWidget):
    """
    Tasks screen view (placeholder).
    """

    # Signals emitted when the user wants to open quiz or exercise
    navigate_to_quiz = Signal()
    navigate_to_exercise = Signal()

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout()

        label = QLabel("Tasks Screen")
        layout.addWidget(label)

        # Placeholder navigation button to Quiz
        quiz_button = QPushButton("Open Quiz")
        quiz_button.clicked.connect(self._on_open_quiz_clicked)
        layout.addWidget(quiz_button)

        # Placeholder navigation button to Exercise
        exercise_button = QPushButton("Open Exercise")
        exercise_button.clicked.connect(self._on_open_exercise_clicked)
        layout.addWidget(exercise_button)

        self.setLayout(layout)

    def _on_open_quiz_clicked(self) -> None:
        """Emit signal to navigate to the quiz view."""
        self.navigate_to_quiz.emit()

    def _on_open_exercise_clicked(self) -> None:
        """Emit signal to navigate to the exercise view."""
        self.navigate_to_exercise.emit()
