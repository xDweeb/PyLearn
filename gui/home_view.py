# home_view.py
# Home screen view for PyLearn Desktop

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class HomeView(QWidget):
    """
    Home screen view (placeholder).
    """
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel("Home Screen")
        layout.addWidget(label)
        self.setLayout(layout)
