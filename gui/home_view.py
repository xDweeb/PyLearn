# home_view.py
# Home screen view for PyLearn Desktop

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

class HomeView(QWidget):
    """
    Home screen view (placeholder).
    """

    # Signal emitted when the user wants to navigate to modules
    navigate_to_modules = Signal()

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout()

        label = QLabel("Home Screen")
        layout.addWidget(label)

        # Placeholder navigation button
        modules_button = QPushButton("Go to Modules")
        modules_button.clicked.connect(self._on_go_to_modules_clicked)
        layout.addWidget(modules_button)

        self.setLayout(layout)

    def _on_go_to_modules_clicked(self) -> None:
        """Emit signal to navigate to the modules view."""
        self.navigate_to_modules.emit()
