# lessons_view.py
# Lessons screen view for PyLearn Desktop
# Displays a list of lessons for the selected module as styled cards.

from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
)


class LessonsView(QWidget):
    """Lessons screen view with lesson cards and navigation signals.

    Signals:
        navigate_to_tasks(int): emitted when the user opens a lesson,
                                passing the lesson_id.
        navigate_back(): emitted when the user clicks the back button.
    """

    # Navigation signals
    navigate_to_tasks = Signal(int)
    navigate_back = Signal()

    def __init__(self) -> None:
        super().__init__()
        # Placeholder module name; can be updated later by controllers
        self._module_name = "Module 1 : Python Start"
        self._setup_ui()

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------
    def _setup_ui(self) -> None:
        """Configure the layout and widgets for the lessons page."""
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

        # Header section: title + subtitle with module name placeholder
        header_layout = QVBoxLayout()
        header_layout.setSpacing(8)

        title_label = QLabel("Leçons du module")
        title_label.setObjectName("titleLabel")
        title_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        subtitle_label = QLabel(f"{self._module_name}")
        subtitle_label.setObjectName("subtitleLabel")
        subtitle_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        header_layout.addWidget(title_label)
        header_layout.addWidget(subtitle_label)

        # Vertical list of lesson cards
        lessons_list_layout = QVBoxLayout()
        lessons_list_layout.setSpacing(12)

        # Hard-coded placeholders for lessons of Module 1
        lesson1_card = self._create_lesson_card(
            lesson_id=1,
            title="Leçon 1 : Introduction à Python",
            status="completed",
        )
        lessons_list_layout.addWidget(lesson1_card)

        lesson2_card = self._create_lesson_card(
            lesson_id=2,
            title="Leçon 2 : La fonction print()",
            status="in_progress",
        )
        lessons_list_layout.addWidget(lesson2_card)

        lesson3_card = self._create_lesson_card(
            lesson_id=3,
            title="Leçon 3 : La fonction input()",
            status="locked",
        )
        lessons_list_layout.addWidget(lesson3_card)

        lesson4_card = self._create_lesson_card(
            lesson_id=4,
            title="Leçon 4 : Commentaires en Python",
            status="locked",
        )
        lessons_list_layout.addWidget(lesson4_card)

        main_layout.addLayout(header_layout)
        main_layout.addLayout(lessons_list_layout)
        main_layout.addStretch()

        self.setLayout(main_layout)

    def _create_lesson_card(
        self,
        lesson_id: int,
        title: str,
        status: str,
    ) -> QFrame:
        """Create a styled lesson card."""
        card = QFrame()
        card.setObjectName("lessonCard")
        card.setFrameShape(QFrame.StyledPanel)

        layout = QHBoxLayout(card)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(12)

        # Determine icon and status text based on status
        if status == "completed":
            icon = "✔"
            status_text = "Terminée"
            locked = False
        elif status == "in_progress":
            icon = "●"
            status_text = "En cours"
            locked = False
        else:  # status == "locked"
            icon = "🔒"
            status_text = "Verrouillée"
            locked = True

        # Left: status icon
        icon_label = QLabel(icon)
        icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon_label)

        # Middle: title and status text stacked vertically
        text_container = QWidget()
        text_layout = QVBoxLayout(text_container)
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(2)

        title_label = QLabel(title)
        status_label = QLabel(status_text)

        text_layout.addWidget(title_label)
        text_layout.addWidget(status_label)

        layout.addWidget(text_container, stretch=1)

        # Right: "Ouvrir" button for unlocked lessons only
        if not locked:
            open_button = QPushButton("Ouvrir")
            open_button.setObjectName("openButton")
            open_button.clicked.connect(
                lambda _checked=False, lid=lesson_id: self._on_open_lesson(lid)
            )
            layout.addWidget(open_button)

        return card

    # ------------------------------------------------------------------
    # Signal emitters
    # ------------------------------------------------------------------
    def _on_open_lesson(self, lesson_id: int) -> None:
        """Emit navigation signal with the selected lesson id."""
        self.navigate_to_tasks.emit(lesson_id)

    def _on_back_clicked(self) -> None:
        """Emit signal to navigate back to modules."""
        self.navigate_back.emit()