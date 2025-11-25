# quiz_view.py
# Quiz screen view for PyLearn Desktop

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class QuizView(QWidget):
    """Quiz screen view (placeholder)."""

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel("Quiz Screen")
        layout.addWidget(label)
        self.setLayout(layout)
