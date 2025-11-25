# lessons_view.py
# Lessons screen view for PyLearn Desktop

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class LessonsView(QWidget):
    """
    Lessons screen view (placeholder).
    """
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel("Lessons Screen")
        layout.addWidget(label)
        self.setLayout(layout)
