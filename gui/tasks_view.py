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
    QListWidget,
    QListWidgetItem,
    QStackedWidget,
    QTextEdit,
)
from controllers.task_controller import TaskController


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
    navigate_to_quiz = Signal(int)      # Emits task_id
    navigate_to_typing = Signal(int)    # Emits task_id
    navigate_to_exercise = Signal(int)  # Emits task_id
    navigate_back = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.controller = TaskController()
        self.tasks = []
        self.current_lesson_id = None
        self.current_task_index = 0
        self._setup_ui()

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------
    def _setup_ui(self) -> None:
        """Configure the main layout with sidebar and content area."""
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # LEFT: Sidebar with task list
        sidebar = self._create_sidebar()
        main_layout.addWidget(sidebar)

        # RIGHT: Content area
        content = self._create_content_area()
        main_layout.addWidget(content, 1)

    def _create_sidebar(self) -> QFrame:
        """Create the sidebar with task list."""
        sidebar = QFrame()
        sidebar.setObjectName("taskSidebar")
        sidebar.setFixedWidth(280)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(15, 20, 15, 20)
        layout.setSpacing(15)

        # Back button
        back_btn = QPushButton("← Retour")
        back_btn.setObjectName("secondaryButton")
        back_btn.clicked.connect(self.navigate_back.emit)
        layout.addWidget(back_btn)

        # Title
        self.sidebar_title = QLabel("Tâches de la leçon")
        self.sidebar_title.setObjectName("sidebarTitle")
        self.sidebar_title.setWordWrap(True)
        layout.addWidget(self.sidebar_title)

        # Task list
        self.task_list = QListWidget()
        self.task_list.setObjectName("taskList")
        self.task_list.currentRowChanged.connect(self._on_task_selected)
        layout.addWidget(self.task_list)

        # Progress info
        self.progress_label = QLabel("Progression: 0/0")
        self.progress_label.setObjectName("progressLabel")
        layout.addWidget(self.progress_label)

        return sidebar

    def _create_content_area(self) -> QFrame:
        """Create the main content area."""
        content = QFrame()
        content.setObjectName("taskContent")

        layout = QVBoxLayout(content)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Task title
        self.task_title = QLabel("Sélectionnez une tâche")
        self.task_title.setObjectName("taskMainTitle")
        layout.addWidget(self.task_title)

        # Task description
        self.task_description = QLabel("")
        self.task_description.setObjectName("taskDescription")
        self.task_description.setWordWrap(True)
        layout.addWidget(self.task_description)

        # Content stack for different task types
        self.content_stack = QStackedWidget()

        # Theory content
        self.theory_content = QTextEdit()
        self.theory_content.setObjectName("theoryContent")
        self.theory_content.setReadOnly(True)
        self.content_stack.addWidget(self.theory_content)

        # Placeholder for other task types
        placeholder = QLabel("Cliquez sur 'Commencer' pour accéder à cette tâche.")
        placeholder.setAlignment(Qt.AlignCenter)
        placeholder.setStyleSheet("color: #7f8c8d; font-size: 14px;")
        self.content_stack.addWidget(placeholder)

        layout.addWidget(self.content_stack, 1)

        # Action buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        self.validate_btn = QPushButton("Valider")
        self.validate_btn.setObjectName("primaryButton")
        self.validate_btn.setFixedWidth(120)
        self.validate_btn.clicked.connect(self._on_validate)
        btn_layout.addWidget(self.validate_btn)

        self.next_btn = QPushButton("Suivant →")
        self.next_btn.setObjectName("secondaryButton")
        self.next_btn.setFixedWidth(120)
        self.next_btn.clicked.connect(self._on_next)
        btn_layout.addWidget(self.next_btn)

        layout.addLayout(btn_layout)

        return content

    # ------------------------------------------------------------------
    # Task loading and selection
    # ------------------------------------------------------------------
    def load_tasks(self, lesson_id: int, lesson_name: str = ""):
        """Load tasks for a specific lesson."""
        self.current_lesson_id = lesson_id
        self.current_task_index = 0

        # Update sidebar title
        if lesson_name:
            self.sidebar_title.setText(lesson_name)
        else:
            self.sidebar_title.setText(f"Leçon {lesson_id}")

        # Clear and reload task list
        self.task_list.clear()
        self.tasks = self.controller.load_tasks(lesson_id)

        # Populate task list
        for task in self.tasks:
            icon = "✔" if task["is_completed"] else "○"
            item = QListWidgetItem(f"{icon}  {task['name']}")
            item.setData(Qt.UserRole, task["id"])
            self.task_list.addItem(item)

        # Update progress
        completed = sum(1 for t in self.tasks if t["is_completed"])
        self.progress_label.setText(f"Progression: {completed}/{len(self.tasks)}")

        # Select first task
        if self.tasks:
            self.task_list.setCurrentRow(0)

    def _on_task_selected(self, row: int):
        """Handle task selection from the list."""
        if row < 0 or row >= len(self.tasks):
            return

        self.current_task_index = row
        task = self.tasks[row]

        self.task_title.setText(task["name"])
        self.task_description.setText(task["description"])

        # Show appropriate content based on task type
        task_type = task["task_type"]

        if task_type == "theory":
            self.content_stack.setCurrentIndex(0)
            self.theory_content.setHtml(self._get_theory_content(task))
            self.validate_btn.setText("Marquer comme lu")
        else:
            self.content_stack.setCurrentIndex(1)
            self.validate_btn.setText("Commencer")

        # Update next button state
        self.next_btn.setEnabled(row < len(self.tasks) - 1)

    def _get_theory_content(self, task: dict) -> str:
        """Get HTML content for theory task."""
        # Placeholder theory content based on task name
        return f"""
        <h2>{task['name']}</h2>
        <p>{task['description']}</p>
        <br>
        <p>Contenu théorique à venir...</p>
        <br>
        <p style="color: #7f8c8d;">
            Ce contenu sera chargé depuis la base de données.
        </p>
        """

    # ------------------------------------------------------------------
    # Signal emitters and handlers
    # ------------------------------------------------------------------
    def _on_validate(self):
        """Handle validate button click."""
        if not self.tasks or self.current_task_index >= len(self.tasks):
            return

        task = self.tasks[self.current_task_index]
        task_type = task["task_type"]

        # For theory, mark as completed
        if task_type == "theory":
            self.controller.mark_task_completed(task["id"])
            self.load_tasks(self.current_lesson_id)  # Refresh
            return

        # For other types, navigate to specific view
        task_id = task["id"]
        if task_type == "quiz":
            self.navigate_to_quiz.emit(task_id)
        elif task_type == "typing":
            self.navigate_to_typing.emit(task_id)
        elif task_type == "exercise":
            self.navigate_to_exercise.emit(task_id)

    def _on_next(self):
        """Handle next button click."""
        if self.current_task_index < len(self.tasks) - 1:
            self.task_list.setCurrentRow(self.current_task_index + 1)
