# typing_view.py
# Typing screen view for PyLearn Desktop

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class TypingView(QWidget):
    """
    Typing screen view (placeholder).
    """
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel("Typing Screen")
        layout.addWidget(label)
        self.setLayout(layout)
