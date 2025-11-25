# modules_view.py
# Modules screen view for PyLearn Desktop

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class ModulesView(QWidget):
    """
    Modules screen view (placeholder).
    """
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel("Modules Screen")
        layout.addWidget(label)
        self.setLayout(layout)
