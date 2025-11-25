# tasks_view.py
# Tasks screen view for PyLearn Desktop
# Displays a sidebar with task list and a content area on the right.

from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QTextEdit,
    QSizePolicy,
)


class TasksView(QWidget):
    """Tasks screen view with a sidebar task list and content area.

    Signals:
        task_selected(int): emitted when a task is clicked, passing the task_id.
        navigate_to_quiz(): emitted when the user navigates to the quiz view.
        navigate_to_exercise(): emitted when the user navigates to the exercise view.
        navigate_back(): emitted when the user clicks the back button.
    """

    # Signals
    task_selected = Signal(int)
    navigate_to_quiz = Signal()
    navigate_to_exercise = Signal()
    navigate_back = Signal()

    def __init__(self) -> None:
        super().__init__()
        # Placeholder lesson title; can be updated later by controllers
        self._lesson_title = "La fonction print()"
        # Track currently selected task for UI highlighting
        self._current_task_id = 1
        self._setup_ui()

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------
    def _setup_ui(self) -> None:
        """Configure the main layout with sidebar and content area."""
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # LEFT: Sidebar with task list
        sidebar = self._create_sidebar()
        main_layout.addWidget(sidebar)

        # RIGHT: Content area
        content_area = self._create_content_area()
        main_layout.addWidget(content_area, stretch=1)

        self.setLayout(main_layout)

    def _create_sidebar(self) -> QFrame:
        """Create the left sidebar containing the task list."""
        sidebar = QFrame()
        sidebar.setObjectName("tasksSidebar")
        sidebar.setFixedWidth(220)
        sidebar.setStyleSheet(
            "#tasksSidebar {"
            "  background-color: #f0f0f0;"
            "  border-right: 1px solid #dcdcdc;"
            "}"
        )

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(16, 16, 16, 24)
        layout.setSpacing(12)

        # Back button at the top of sidebar
        back_button = QPushButton("← Retour")
        back_button.setStyleSheet(
            "padding: 6px 12px; font-size: 12px; font-weight: 500;"
        )
        back_button.setCursor(Qt.PointingHandCursor)
        back_button.clicked.connect(self._on_back_clicked)
        layout.addWidget(back_button)

        # Sidebar header
        header_label = QLabel("Tâches de la leçon")
        header_label.setStyleSheet("font-size: 16px; font-weight: 700;")
        layout.addWidget(header_label)

        # Lesson title (placeholder)
        lesson_label = QLabel(self._lesson_title)
        lesson_label.setStyleSheet("font-size: 13px; color: #555555;")
        lesson_label.setWordWrap(True)
        layout.addWidget(lesson_label)

        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("color: #dcdcdc;")
        layout.addWidget(separator)

        # Task list (hard-coded placeholders with status icons)
        # Status: ○ not started, ● in progress, ✔ completed
        tasks = [
            {"id": 1, "title": "Théorie", "status": "in_progress"},
            {"id": 2, "title": "Quiz", "status": "not_started"},
            {"id": 3, "title": "Typing", "status": "not_started"},
            {"id": 4, "title": "Exercice", "status": "not_started"},
        ]

        for task in tasks:
            task_button = self._create_task_item(
                task_id=task["id"],
                title=task["title"],
                status=task["status"],
            )
            layout.addWidget(task_button)

        layout.addStretch()

        return sidebar

    def _create_task_item(self, task_id: int, title: str, status: str) -> QPushButton:
        """Create a clickable task item for the sidebar.

        Args:
            task_id: unique identifier for the task.
            title: task title to display.
            status: one of 'completed', 'in_progress', or 'not_started'.
        """
        # Determine icon based on status
        if status == "completed":
            icon = "✔"
        elif status == "in_progress":
            icon = "●"
        else:  # not_started
            icon = "○"

        button = QPushButton(f"{icon}  {title}")
        button.setObjectName("taskItem")
        button.setStyleSheet(
            "#taskItem {"
            "  text-align: left;"
            "  padding: 10px 12px;"
            "  font-size: 13px;"
            "  background-color: transparent;"
            "  border: none;"
            "  border-radius: 6px;"
            "}"
            "#taskItem:hover {"
            "  background-color: #e0e0e0;"
            "}"
        )
        button.setCursor(Qt.PointingHandCursor)
        button.clicked.connect(
            lambda _checked=False, tid=task_id: self._on_task_clicked(tid)
        )

        return button

    def _create_content_area(self) -> QFrame:
        """Create the right content area for displaying task content."""
        content = QFrame()
        content.setObjectName("tasksContent")
        content.setStyleSheet(
            "#tasksContent {"
            "  background-color: #ffffff;"
            "}"
        )

        layout = QVBoxLayout(content)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(20)

        # Content header
        content_header = QLabel("Théorie")
        content_header.setObjectName("contentHeader")
        content_header.setStyleSheet(
            "#contentHeader {"
            "  font-size: 20px;"
            "  font-weight: 700;"
            "}"
        )
        layout.addWidget(content_header)

        # Instructions / theory placeholder
        instructions_label = QLabel(
            "Bienvenue dans la leçon sur la fonction print().\n\n"
            "La fonction print() permet d'afficher du texte ou des valeurs "
            "dans la console Python.\n\n"
            "Exemple :\n"
            "    print(\"Bonjour, monde!\")\n\n"
            "Cliquez sur 'Suivant' pour continuer."
        )
        instructions_label.setWordWrap(True)
        instructions_label.setStyleSheet("font-size: 14px; color: #333333;")
        instructions_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        layout.addWidget(instructions_label)

        # Code editor placeholder (for coding tasks)
        code_editor_label = QLabel("Zone de code (pour les exercices)")
        code_editor_label.setStyleSheet("font-size: 13px; color: #777777;")
        layout.addWidget(code_editor_label)

        self.code_editor = QTextEdit()
        self.code_editor.setPlaceholderText("# Écrivez votre code ici...")
        self.code_editor.setStyleSheet(
            "font-family: 'Consolas', 'Courier New', monospace;"
            "font-size: 13px;"
            "background-color: #f9f9f9;"
            "border: 1px solid #dcdcdc;"
            "border-radius: 6px;"
            "padding: 8px;"
        )
        self.code_editor.setMinimumHeight(120)
        layout.addWidget(self.code_editor)

        layout.addStretch()

        # Bottom buttons: Valider and Suivant
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(12)
        buttons_layout.addStretch()

        validate_button = QPushButton("Valider")
        validate_button.setStyleSheet(
            "padding: 10px 20px;"
            "font-size: 14px;"
            "font-weight: 500;"
            "background-color: #4CAF50;"
            "color: #ffffff;"
            "border: none;"
            "border-radius: 6px;"
        )
        validate_button.setCursor(Qt.PointingHandCursor)
        buttons_layout.addWidget(validate_button)

        next_button = QPushButton("Suivant")
        next_button.setStyleSheet(
            "padding: 10px 20px;"
            "font-size: 14px;"
            "font-weight: 500;"
            "background-color: #2196F3;"
            "color: #ffffff;"
            "border: none;"
            "border-radius: 6px;"
        )
        next_button.setCursor(Qt.PointingHandCursor)
        buttons_layout.addWidget(next_button)

        layout.addLayout(buttons_layout)

        return content

    # ------------------------------------------------------------------
    # Signal emitters
    # ------------------------------------------------------------------
    def _on_task_clicked(self, task_id: int) -> None:
        """Emit signal with the selected task id.

        This is UI-only: no database or business logic is involved.
        """
        self._current_task_id = task_id
        self.task_selected.emit(task_id)

        # Also emit specific navigation signals for quiz/exercise
        if task_id == 2:
            self.navigate_to_quiz.emit()
        elif task_id == 4:
            self.navigate_to_exercise.emit()

    def _on_back_clicked(self) -> None:
        """Emit signal to navigate back to lessons."""
        self.navigate_back.emit()
