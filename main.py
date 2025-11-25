# main.py
# Entry point for PyLearn Desktop application

import os
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget

from database.db import Database
from navigation_manager import NavigationManager
from gui.home_view import HomeView
from gui.modules_view import ModulesView
from gui.lessons_view import LessonsView
from gui.tasks_view import TasksView
from gui.quiz_view import QuizView
from gui.exercise_view import ExerciseView
from gui.typing_view import TypingView


class MainWindow(QMainWindow):
    """Main application window with stacked widget for navigation."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("PyLearn Desktop")
        self.setGeometry(100, 100, 1024, 768)

        # Placeholder IDs for back navigation (will be updated by controllers later)
        self.last_module_id = 1
        self.last_lesson_id = 1

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

        # Register views by name
        self.navigation.register_view("home", self.home_view)
        self.navigation.register_view("modules", self.modules_view)
        self.navigation.register_view("lessons", self.lessons_view)
        self.navigation.register_view("tasks", self.tasks_view)
        self.navigation.register_view("quiz", self.quiz_view)
        self.navigation.register_view("exercise", self.exercise_view)
        self.navigation.register_view("typing", self.typing_view)

    def _connect_navigation_signals(self) -> None:
        """Connect navigation signals from views to navigation actions."""
        # Forward navigation signals
        self.home_view.navigate_to_modules.connect(
            lambda: self.navigation.navigate("modules")
        )

        self.modules_view.navigate_to_lessons.connect(
            self._on_navigate_to_lessons
        )

        self.lessons_view.navigate_to_tasks.connect(
            self._on_navigate_to_tasks
        )

        self.tasks_view.navigate_to_quiz.connect(
            lambda: self.navigation.navigate("quiz")
        )

        self.tasks_view.navigate_to_exercise.connect(
            lambda: self.navigation.navigate("exercise")
        )

        # Back navigation signals
        self.modules_view.navigate_back.connect(
            lambda: self.navigation.navigate("home")
        )

        self.lessons_view.navigate_back.connect(
            lambda: self.navigation.navigate("modules")
        )

        self.tasks_view.navigate_back.connect(
            lambda: self.navigation.navigate("lessons")
        )

        self.quiz_view.navigate_back.connect(
            lambda: self.navigation.navigate("tasks")
        )

        self.typing_view.navigate_back.connect(
            lambda: self.navigation.navigate("tasks")
        )

        self.exercise_view.navigate_back.connect(
            lambda: self.navigation.navigate("tasks")
        )

    def _on_navigate_to_lessons(self, module_id: int) -> None:
        """Handle navigation to lessons, storing the module_id."""
        self.last_module_id = module_id
        self.navigation.navigate("lessons")

    def _on_navigate_to_tasks(self, lesson_id: int) -> None:
        """Handle navigation to tasks, storing the lesson_id."""
        self.last_lesson_id = lesson_id
        self.navigation.navigate("tasks")

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

    # Load global stylesheet
    style_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "assets", "styles", "style.qss"
    )
    if os.path.exists(style_path):
        with open(style_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
