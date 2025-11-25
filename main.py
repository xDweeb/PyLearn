# main.py
# Entry point for PyLearn Desktop application

import os
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QMessageBox

from utils.resource_path import resource_path
from database.db import Database
from controllers.module_controller import ModuleController
from controllers.lesson_controller import LessonController
from controllers.task_controller import TaskController
from controllers.progression_manager import ProgressionManager
from navigation_manager import NavigationManager
from gui.home_view import HomeView
from gui.modules_view import ModulesView
from gui.lessons_view import LessonsView
from gui.tasks_view import TasksView
from gui.quiz_view import QuizView
from gui.exercise_view import ExerciseView
from gui.typing_view import TypingView
from gui.statistics_view import StatisticsView


class MainWindow(QMainWindow):
    """Main application window with stacked widget for navigation."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("PyLearn Desktop")
        self.setGeometry(100, 100, 1024, 768)

        # Controllers for fetching data
        self.module_controller = ModuleController()
        self.lesson_controller = LessonController()
        self.task_controller = TaskController()
        self.progression_manager = ProgressionManager()

        # Store current context for navigation
        self.current_module_id = None
        self.current_module_name = ""
        self.current_lesson_id = None
        self.current_lesson_name = ""
        self.current_task_id = None

        # Stacked widget for navigation between views
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Navigation manager to keep track of named views
        self.navigation = NavigationManager()
        self.navigation.set_navigation_callback(self.navigate_to)

        # Create, register, and wire all views
        self._create_views()
        self._register_views()
        self._connect_navigation_signals()

        # Start on the home view
        self.navigate_to("home")

    def _create_views(self) -> None:
        """Instantiate all views used in the application."""
        self.home_view = HomeView()
        self.modules_view = ModulesView()
        self.lessons_view = LessonsView()
        self.tasks_view = TasksView()
        self.quiz_view = QuizView()
        self.exercise_view = ExerciseView()
        self.typing_view = TypingView()
        self.statistics_view = StatisticsView()

    def _register_views(self) -> None:
        """Add views to stacked widget and register them in NavigationManager."""
        # Add widgets to the stacked widget
        self.stacked_widget.addWidget(self.home_view)
        self.stacked_widget.addWidget(self.modules_view)
        self.stacked_widget.addWidget(self.lessons_view)
        self.stacked_widget.addWidget(self.tasks_view)
        self.stacked_widget.addWidget(self.quiz_view)
        self.stacked_widget.addWidget(self.exercise_view)
        self.stacked_widget.addWidget(self.typing_view)
        self.stacked_widget.addWidget(self.statistics_view)

        # Register views by name
        self.navigation.register_view("home", self.home_view)
        self.navigation.register_view("modules", self.modules_view)
        self.navigation.register_view("lessons", self.lessons_view)
        self.navigation.register_view("tasks", self.tasks_view)
        self.navigation.register_view("quiz", self.quiz_view)
        self.navigation.register_view("exercise", self.exercise_view)
        self.navigation.register_view("typing", self.typing_view)
        self.navigation.register_view("statistics", self.statistics_view)

    def _connect_navigation_signals(self) -> None:
        """Connect navigation signals from views to navigation actions."""
        # Forward navigation signals
        self.home_view.navigate_to_modules.connect(
            self._on_navigate_to_modules
        )

        self.home_view.navigate_to_statistics.connect(
            self._on_navigate_to_statistics
        )

        self.modules_view.navigate_to_lessons.connect(
            self._on_navigate_to_lessons
        )

        self.lessons_view.navigate_to_tasks.connect(
            self._on_navigate_to_tasks
        )

        self.tasks_view.navigate_to_quiz.connect(
            self._on_navigate_to_quiz
        )

        self.tasks_view.navigate_to_typing.connect(
            self._on_navigate_to_typing
        )

        self.tasks_view.navigate_to_exercise.connect(
            self._on_navigate_to_exercise
        )

        # Task selection tracking
        self.tasks_view.task_selected.connect(
            self._on_task_selected
        )

        # Back navigation signals
        self.modules_view.navigate_back.connect(
            self._on_back_to_home
        )

        self.lessons_view.navigate_back.connect(
            self._on_back_to_modules
        )

        self.tasks_view.navigate_back.connect(
            self._on_back_to_lessons
        )

        self.quiz_view.navigate_back.connect(
            self._on_back_to_tasks
        )

        self.typing_view.navigate_back.connect(
            self._on_back_to_tasks
        )

        self.exercise_view.navigate_back.connect(
            self._on_back_to_tasks
        )

        # Statistics view back navigation
        self.statistics_view.navigate_back.connect(
            self._on_back_to_home
        )

    def _on_back_to_home(self) -> None:
        """Handle back navigation to home view (refresh data)."""
        self.home_view.refresh_data()
        self.navigation.navigate("home")

    def _on_navigate_to_statistics(self) -> None:
        """Handle navigation to statistics view."""
        self.statistics_view.load_statistics()
        self.navigation.navigate("statistics")

    def _on_navigate_to_modules(self) -> None:
        """Handle navigation to modules view."""
        self.modules_view.load_modules()
        self.navigation.navigate("modules")

    def _on_navigate_to_lessons(self, module_id: int) -> None:
        """Handle navigation to lessons, storing the module context."""
        self.current_module_id = module_id
        
        # Get module name for display
        module = self.module_controller.get_module_by_id(module_id)
        self.current_module_name = module["name"] if module else ""
        
        self.lessons_view.load_lessons(module_id, self.current_module_name)
        self.navigation.navigate("lessons")

    def _on_navigate_to_tasks(self, lesson_id: int) -> None:
        """Handle navigation to tasks, storing the lesson context."""
        self.current_lesson_id = lesson_id
        
        # Get lesson name for display
        lesson = self.lesson_controller.get_lesson_by_id(lesson_id)
        self.current_lesson_name = lesson["name"] if lesson else ""
        
        self.tasks_view.load_tasks(lesson_id, self.current_lesson_name)
        self.navigation.navigate("tasks")

    def _on_task_selected(self, task_id: int) -> None:
        """Handle task selection - store current task ID."""
        self.current_task_id = task_id

    def _on_navigate_to_quiz(self, task_id: int) -> None:
        """Handle navigation to quiz view."""
        # TODO: Load quiz content based on task_id
        self.navigation.navigate("quiz")

    def _on_navigate_to_typing(self, task_id: int) -> None:
        """Handle navigation to typing view."""
        # TODO: Load typing content based on task_id
        self.navigation.navigate("typing")

    def _on_navigate_to_exercise(self, task_id: int) -> None:
        """Handle navigation to exercise view."""
        # TODO: Load exercise content based on task_id
        self.navigation.navigate("exercise")

    def _on_back_to_modules(self) -> None:
        """Handle back navigation to modules view (reload data)."""
        self.modules_view.load_modules()
        self.navigation.navigate("modules")

    def _on_back_to_lessons(self) -> None:
        """Handle back navigation to lessons view (reload data)."""
        if self.current_module_id:
            self.lessons_view.load_lessons(self.current_module_id, self.current_module_name)
        self.navigation.navigate("lessons")

    def _on_back_to_tasks(self) -> None:
        """Handle back navigation to tasks view (reload data)."""
        if self.current_lesson_id:
            self.tasks_view.load_tasks(self.current_lesson_id, self.current_lesson_name)
        self.navigation.navigate("tasks")

    # ------------------------------------------------------------------
    # Task Validation Methods
    # ------------------------------------------------------------------

    def validate_current_task(self, task_id: int, user_input: str) -> dict:
        """
        Validate the current task with user input.

        Args:
            task_id: The ID of the task to validate
            user_input: The user's input/answer

        Returns:
            Dict with validation result:
                - success: bool
                - message: str
                - unlock_next: bool
        """
        result = self.task_controller.validate_task(task_id, user_input)

        # Show feedback to user
        if result["success"]:
            QMessageBox.information(
                self,
                "Succès ! 🎉",
                result["message"],
                QMessageBox.Ok
            )
            # Refresh tasks view to show updated status
            if self.current_lesson_id:
                self.tasks_view.load_tasks(self.current_lesson_id, self.current_lesson_name)
        else:
            QMessageBox.warning(
                self,
                "Réessayez",
                result["message"],
                QMessageBox.Ok
            )

        return result

    def navigate_to(self, view_name: str) -> None:
        """Switch the current widget in the stacked widget by view name."""
        widget = self.navigation.get_view(view_name)
        if widget is not None:
            self.stacked_widget.setCurrentWidget(widget)


if __name__ == "__main__":
    # Initialize database
    Database.initialize()

    # Start Qt application
    app = QApplication(sys.argv)

    # Load global stylesheet using resource_path for PyInstaller compatibility
    style_path = resource_path(os.path.join("assets", "styles", "style.qss"))
    if os.path.exists(style_path):
        with open(style_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
