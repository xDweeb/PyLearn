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
    QScrollArea,
    QRadioButton,
    QButtonGroup,
    QMessageBox,
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
    validation_requested = Signal(int, str)  # Emits (task_id, user_input)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.controller = TaskController()
        self.tasks = []
        self.current_lesson_id = None
        self.current_lesson_name = ""
        self.current_task_index = 0
        self.current_task_data = {}
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

        # Index 0: Theory content
        self._create_theory_widget()
        
        # Index 1: Quiz content
        self._create_quiz_widget()
        
        # Index 2: Typing content
        self._create_typing_widget()
        
        # Index 3: Exercise content
        self._create_exercise_widget()

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

    def _create_theory_widget(self) -> None:
        """Create the theory content widget."""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        
        self.theory_content = QLabel()
        self.theory_content.setObjectName("theoryContent")
        self.theory_content.setWordWrap(True)
        self.theory_content.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.theory_content.setTextFormat(Qt.PlainText)
        self.theory_content.setStyleSheet("""
            QLabel {
                font-size: 14px;
                line-height: 1.6;
                padding: 20px;
                background-color: #ffffff;
                border-radius: 8px;
            }
        """)
        
        scroll.setWidget(self.theory_content)
        self.content_stack.addWidget(scroll)

    def _create_quiz_widget(self) -> None:
        """Create the quiz content widget."""
        quiz_frame = QFrame()
        quiz_layout = QVBoxLayout(quiz_frame)
        quiz_layout.setContentsMargins(20, 20, 20, 20)
        quiz_layout.setSpacing(20)

        # Question label
        self.quiz_question = QLabel()
        self.quiz_question.setObjectName("quizQuestion")
        self.quiz_question.setWordWrap(True)
        self.quiz_question.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #2c3e50;
                padding: 15px;
                background-color: #f8f9fa;
                border-radius: 8px;
            }
        """)
        quiz_layout.addWidget(self.quiz_question)

        # Answer options frame
        self.quiz_options_frame = QFrame()
        self.quiz_options_layout = QVBoxLayout(self.quiz_options_frame)
        self.quiz_options_layout.setSpacing(10)
        self.quiz_button_group = QButtonGroup(self)
        quiz_layout.addWidget(self.quiz_options_frame)

        # User answer input (alternative)
        self.quiz_answer_label = QLabel("Votre réponse:")
        self.quiz_answer_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        quiz_layout.addWidget(self.quiz_answer_label)

        self.quiz_answer_input = QTextEdit()
        self.quiz_answer_input.setObjectName("quizAnswerInput")
        self.quiz_answer_input.setFixedHeight(60)
        self.quiz_answer_input.setPlaceholderText("Entrez votre réponse ici...")
        quiz_layout.addWidget(self.quiz_answer_input)

        quiz_layout.addStretch()
        self.content_stack.addWidget(quiz_frame)

    def _create_typing_widget(self) -> None:
        """Create the typing practice widget."""
        typing_frame = QFrame()
        typing_layout = QVBoxLayout(typing_frame)
        typing_layout.setContentsMargins(20, 20, 20, 20)
        typing_layout.setSpacing(20)

        # Instructions
        typing_instructions = QLabel("Recopiez le code ci-dessous exactement comme affiché:")
        typing_instructions.setStyleSheet("font-size: 14px; color: #7f8c8d;")
        typing_layout.addWidget(typing_instructions)

        # Target text to type
        self.typing_target = QLabel()
        self.typing_target.setObjectName("typingTarget")
        self.typing_target.setWordWrap(True)
        self.typing_target.setStyleSheet("""
            QLabel {
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 16px;
                padding: 20px;
                background-color: #2c3e50;
                color: #ecf0f1;
                border-radius: 8px;
            }
        """)
        typing_layout.addWidget(self.typing_target)

        # User typing area
        typing_label = QLabel("Votre saisie:")
        typing_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        typing_layout.addWidget(typing_label)

        self.typing_input = QTextEdit()
        self.typing_input.setObjectName("typingInput")
        self.typing_input.setPlaceholderText("Commencez à taper ici...")
        self.typing_input.setStyleSheet("""
            QTextEdit {
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 14px;
                padding: 15px;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
            }
            QTextEdit:focus {
                border-color: #3c78d8;
            }
        """)
        typing_layout.addWidget(self.typing_input)

        typing_layout.addStretch()
        self.content_stack.addWidget(typing_frame)

    def _create_exercise_widget(self) -> None:
        """Create the exercise widget."""
        exercise_frame = QFrame()
        exercise_layout = QVBoxLayout(exercise_frame)
        exercise_layout.setContentsMargins(20, 20, 20, 20)
        exercise_layout.setSpacing(20)

        # Exercise prompt
        self.exercise_prompt = QLabel()
        self.exercise_prompt.setObjectName("exercisePrompt")
        self.exercise_prompt.setWordWrap(True)
        self.exercise_prompt.setStyleSheet("""
            QLabel {
                font-size: 15px;
                padding: 20px;
                background-color: #e8f4f8;
                border-left: 4px solid #3c78d8;
                border-radius: 4px;
            }
        """)
        exercise_layout.addWidget(self.exercise_prompt)

        # Code editor area
        code_label = QLabel("Votre code:")
        code_label.setStyleSheet("font-weight: bold;")
        exercise_layout.addWidget(code_label)

        self.exercise_input = QTextEdit()
        self.exercise_input.setObjectName("exerciseInput")
        self.exercise_input.setPlaceholderText("# Écrivez votre code Python ici...")
        self.exercise_input.setStyleSheet("""
            QTextEdit {
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 14px;
                padding: 15px;
                background-color: #1e1e1e;
                color: #d4d4d4;
                border-radius: 8px;
            }
        """)
        exercise_layout.addWidget(self.exercise_input)

        # Hint area (hidden solution)
        self.exercise_hint_btn = QPushButton("💡 Voir un indice")
        self.exercise_hint_btn.setObjectName("secondaryButton")
        self.exercise_hint_btn.clicked.connect(self._toggle_hint)
        exercise_layout.addWidget(self.exercise_hint_btn)

        self.exercise_solution = QLabel()
        self.exercise_solution.setObjectName("exerciseSolution")
        self.exercise_solution.setWordWrap(True)
        self.exercise_solution.setVisible(False)
        self.exercise_solution.setStyleSheet("""
            QLabel {
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 13px;
                padding: 15px;
                background-color: #fff3cd;
                border: 1px solid #ffc107;
                border-radius: 8px;
            }
        """)
        exercise_layout.addWidget(self.exercise_solution)

        exercise_layout.addStretch()
        self.content_stack.addWidget(exercise_frame)

    def _toggle_hint(self) -> None:
        """Toggle the visibility of the solution hint."""
        is_visible = self.exercise_solution.isVisible()
        self.exercise_solution.setVisible(not is_visible)
        if is_visible:
            self.exercise_hint_btn.setText("💡 Voir un indice")
        else:
            self.exercise_hint_btn.setText("🙈 Masquer l'indice")

    # ------------------------------------------------------------------
    # Task loading and selection
    # ------------------------------------------------------------------
    def load_tasks(self, lesson_id: int, lesson_name: str = ""):
        """Load tasks for a specific lesson."""
        self.current_lesson_id = lesson_id
        self.current_lesson_name = lesson_name
        self.current_task_index = 0

        # Update sidebar title
        if lesson_name:
            self.sidebar_title.setText(lesson_name)
        else:
            self.sidebar_title.setText(f"Leçon {lesson_id}")

        # Clear and reload task list
        self.task_list.clear()
        self.tasks = self.controller.load_tasks(lesson_id)

        # Populate task list with status icons
        for task in self.tasks:
            if task["is_completed"]:
                icon = "✔"
            elif task["is_unlocked"]:
                icon = "○"
            else:
                icon = "🔒"
            
            item = QListWidgetItem(f"{icon}  {task['name']}")
            item.setData(Qt.UserRole, task["id"])
            
            # Disable locked tasks visually
            if not task["is_unlocked"] and not task["is_completed"]:
                item.setFlags(item.flags() & ~Qt.ItemIsEnabled)
            
            self.task_list.addItem(item)

        # Update progress
        completed = sum(1 for t in self.tasks if t["is_completed"])
        self.progress_label.setText(f"Progression: {completed}/{len(self.tasks)}")

        # Select first unlocked task
        first_unlocked = next(
            (i for i, t in enumerate(self.tasks) if t["is_unlocked"] and not t["is_completed"]),
            0
        )
        if self.tasks:
            self.task_list.setCurrentRow(first_unlocked)

    def _on_task_selected(self, row: int):
        """Handle task selection from the list."""
        if row < 0 or row >= len(self.tasks):
            return

        self.current_task_index = row
        task = self.tasks[row]

        # Check if task is locked
        if not task["is_unlocked"] and not task["is_completed"]:
            self.task_title.setText("🔒 Tâche verrouillée")
            self.task_description.setText("Complétez les tâches précédentes pour débloquer celle-ci.")
            self.content_stack.setCurrentIndex(0)
            self.theory_content.setText("Cette tâche est verrouillée.\n\nVeuillez compléter les tâches précédentes.")
            self.validate_btn.setEnabled(False)
            return

        # Enable validate button
        self.validate_btn.setEnabled(True)

        # Load full task content from controller
        task_id = task["id"]
        self.current_task_data = self.controller.load_task_content(task_id)
        
        # Display the task content
        self.display_task_content(self.current_task_data)

        # Update next button state
        self.next_btn.setEnabled(row < len(self.tasks) - 1)

        # Emit task_selected signal
        self.task_selected.emit(task_id)

    def display_task_content(self, task_data: dict) -> None:
        """Display task content in the appropriate widget based on task type."""
        if not task_data:
            return

        task_type = task_data.get("type", "theory")
        name = task_data.get("name", "")
        description = task_data.get("description", "")

        # Update header
        self.task_title.setText(name)
        self.task_description.setText(description)

        # Display content based on type
        if task_type == "theory":
            self._display_theory(task_data)
        elif task_type == "quiz":
            self._display_quiz(task_data)
        elif task_type == "typing":
            self._display_typing(task_data)
        elif task_type == "exercise":
            self._display_exercise(task_data)

    def _display_theory(self, task_data: dict) -> None:
        """Display theory content."""
        content = task_data.get("content", "Contenu non disponible.")
        self.theory_content.setText(content)
        self.content_stack.setCurrentIndex(0)
        self.validate_btn.setText("Marquer comme lu")

    def _display_quiz(self, task_data: dict) -> None:
        """Display quiz content."""
        question = task_data.get("question", "Question non disponible.")
        self.quiz_question.setText(question)
        self.quiz_answer_input.clear()
        self.content_stack.setCurrentIndex(1)
        self.validate_btn.setText("Vérifier")

    def _display_typing(self, task_data: dict) -> None:
        """Display typing content."""
        text = task_data.get("text", "Texte non disponible.")
        self.typing_target.setText(text)
        self.typing_input.clear()
        self.content_stack.setCurrentIndex(2)
        self.validate_btn.setText("Vérifier")

    def _display_exercise(self, task_data: dict) -> None:
        """Display exercise content."""
        prompt = task_data.get("prompt", "Exercice non disponible.")
        solution = task_data.get("solution", "")
        
        self.exercise_prompt.setText(prompt)
        self.exercise_solution.setText(f"Solution:\n{solution}")
        self.exercise_solution.setVisible(False)
        self.exercise_hint_btn.setText("💡 Voir un indice")
        self.exercise_input.clear()
        self.content_stack.setCurrentIndex(3)
        self.validate_btn.setText("Soumettre")

    # ------------------------------------------------------------------
    # Validation and Signal Handlers
    # ------------------------------------------------------------------
    def _on_validate(self):
        """Handle validate button click - collect input and validate."""
        if not self.tasks or self.current_task_index >= len(self.tasks):
            return

        task = self.tasks[self.current_task_index]
        task_id = task["id"]
        task_type = task["task_type"]

        # Collect user input based on task type
        user_input = self._collect_user_input(task_type)

        # Call validation through controller
        result = self.controller.validate_task(task_id, user_input)

        # Show result message
        self._show_validation_result(result)

        # Refresh task list to update status icons
        if result["success"]:
            self._refresh_after_validation()

    def _collect_user_input(self, task_type: str) -> str:
        """Collect user input based on task type."""
        if task_type == "theory":
            return ""  # No input needed for theory
        elif task_type == "quiz":
            return self.quiz_answer_input.toPlainText()
        elif task_type == "typing":
            return self.typing_input.toPlainText()
        elif task_type == "exercise":
            return self.exercise_input.toPlainText()
        return ""

    def _show_validation_result(self, result: dict) -> None:
        """Show validation result in a message box."""
        success = result.get("success", False)
        message = result.get("message", "")

        if success:
            QMessageBox.information(
                self,
                "Succès ! 🎉",
                message,
                QMessageBox.Ok
            )
        else:
            QMessageBox.warning(
                self,
                "Réessayez",
                message,
                QMessageBox.Ok
            )

    def _refresh_after_validation(self) -> None:
        """Refresh the view after successful validation."""
        # Store current position
        current_row = self.current_task_index

        # Reload tasks to get updated status
        self.load_tasks(self.current_lesson_id, self.current_lesson_name)

        # Move to next task if available and unlocked
        if current_row < len(self.tasks) - 1:
            next_task = self.tasks[current_row + 1]
            if next_task["is_unlocked"]:
                self.task_list.setCurrentRow(current_row + 1)
            else:
                self.task_list.setCurrentRow(current_row)
        else:
            self.task_list.setCurrentRow(current_row)

    def validate_from_external(self, task_id: int, user_input: str) -> dict:
        """
        Validate task from external caller (MainWindow).
        Returns validation result dict.
        """
        return self.controller.validate_task(task_id, user_input)

    def _on_next(self):
        """Handle next button click."""
        if self.current_task_index < len(self.tasks) - 1:
            self.task_list.setCurrentRow(self.current_task_index + 1)
