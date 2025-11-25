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
    QScrollArea,
    QFrame,
)
from controllers.lesson_controller import LessonController


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
        self.controller = LessonController()
        self.lessons = []
        self.current_module_id = None
        # Placeholder module name; can be updated later by controllers
        self._module_name = "Module 1 : Python Start"
        self._setup_ui()

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------
    def _setup_ui(self) -> None:
        """Configure the layout and widgets for the lessons page."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Header with back button
        header = QHBoxLayout()

        back_btn = QPushButton("← Retour")
        back_btn.setObjectName("secondaryButton")
        back_btn.setFixedWidth(120)
        back_btn.clicked.connect(self.navigate_back.emit)
        header.addWidget(back_btn)

        header.addStretch()
        layout.addLayout(header)

        # Title (will be updated with module name)
        self.title = QLabel("Leçons du module")
        self.title.setObjectName("viewTitle")
        self.title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title)

        self.subtitle = QLabel(
            "Progressez à travers les leçons pour maîtriser ce module"
        )
        self.subtitle.setObjectName("viewSubtitle")
        self.subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.subtitle)

        # Scrollable area for lessons
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        scroll_content = QWidget()
        self.lessons_layout = QVBoxLayout(scroll_content)
        self.lessons_layout.setSpacing(15)
        self.lessons_layout.setContentsMargins(50, 10, 50, 10)

        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

        self.setLayout(layout)

    def load_lessons(self, module_id: int, module_name: str = ""):
        """Load lessons for a specific module."""
        self.current_module_id = module_id

        # Update title
        if module_name:
            self.title.setText(f"Leçons - {module_name}")
        else:
            self.title.setText(f"Leçons du module {module_id}")

        # Clear existing lesson cards
        while self.lessons_layout.count():
            item = self.lessons_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Load lessons from controller
        self.lessons = self.controller.load_lessons(module_id)

        # Create lesson cards
        for idx, lesson in enumerate(self.lessons):
            card = self._create_lesson_card(lesson, idx + 1)
            self.lessons_layout.addWidget(card)

        # Add stretch at the end
        self.lessons_layout.addStretch()

    def _create_lesson_card(self, lesson: dict, number: int) -> QFrame:
        """Create a card widget for a lesson."""
        card = QFrame()
        card.setObjectName("lessonCard")
        card.setFixedHeight(80)

        card_layout = QHBoxLayout(card)
        card_layout.setContentsMargins(20, 15, 20, 15)
        card_layout.setSpacing(15)

        # Status icon
        status = lesson["status"]
        if status == "completed":
            status_icon = "✔"
            status_color = "#27ae60"
        elif status == "in_progress":
            status_icon = "●"
            status_color = "#3c78d8"
        else:  # locked
            status_icon = "🔒"
            status_color = "#7f8c8d"

        icon_label = QLabel(status_icon)
        icon_label.setStyleSheet(f"font-size: 20px; color: {status_color};")
        icon_label.setFixedWidth(30)
        card_layout.addWidget(icon_label)

        # Lesson number
        num_label = QLabel(f"{number}.")
        num_label.setStyleSheet(
            "font-size: 16px; font-weight: bold; color: #2c3e50;"
        )
        num_label.setFixedWidth(30)
        card_layout.addWidget(num_label)

        # Lesson info
        info_layout = QVBoxLayout()
        info_layout.setSpacing(2)

        name_label = QLabel(lesson["name"])
        name_label.setObjectName("lessonTitle")
        info_layout.addWidget(name_label)

        desc_label = QLabel(lesson["description"])
        desc_label.setObjectName("lessonDescription")
        info_layout.addWidget(desc_label)

        card_layout.addLayout(info_layout, 1)

        # Action button
        if status == "locked":
            btn = QPushButton("Verrouillé")
            btn.setObjectName("secondaryButton")
            btn.setEnabled(False)
        elif status == "completed":
            btn = QPushButton("Réviser")
            btn.setObjectName("secondaryButton")
            btn.clicked.connect(
                lambda checked, l_id=lesson["id"]: self.navigate_to_tasks.emit(l_id)
            )
        else:
            btn = QPushButton("Continuer")
            btn.setObjectName("primaryButton")
            btn.clicked.connect(
                lambda checked, l_id=lesson["id"]: self.navigate_to_tasks.emit(l_id)
            )

        btn.setFixedWidth(120)
        card_layout.addWidget(btn)

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