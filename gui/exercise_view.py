# exercise_view.py
# Exercise screen view for PyLearn Desktop

from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
)


class ExerciseView(QWidget):
    """Exercise screen view (placeholder).

    Signals:
        navigate_back(): emitted when the user clicks the back button.
    """

    # Navigation signal
    navigate_back = Signal()

    def __init__(self) -> None:
        super().__init__()
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Configure the layout and widgets for the exercise page."""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(24)

        # Top bar with back button
        top_layout = QHBoxLayout()
        back_button = QPushButton("← Retour")
        back_button.setObjectName("backButton")
        back_button.setCursor(Qt.PointingHandCursor)
        back_button.clicked.connect(self._on_back_clicked)
        top_layout.addWidget(back_button)
        top_layout.addStretch()

        main_layout.addLayout(top_layout)

        # Page title
        title_label = QLabel("Exercice")
        title_label.setObjectName("titleLabel")
        main_layout.addWidget(title_label)

        # Placeholder content
        content_label = QLabel("Exercice de code à venir...")
        content_label.setObjectName("subtitleLabel")
        main_layout.addWidget(content_label)

        main_layout.addStretch()

        self.setLayout(main_layout)

    def _on_back_clicked(self) -> None:
        """Emit signal to navigate back to tasks."""
        self.navigate_back.emit()
