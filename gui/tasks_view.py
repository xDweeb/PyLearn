# tasks_view.py
# Tasks screen view for PyLearn Desktop

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class TasksView(QWidget):
    """
    Tasks screen view (placeholder).
    """
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel("Tasks Screen")
        layout.addWidget(label)
        self.setLayout(layout)
