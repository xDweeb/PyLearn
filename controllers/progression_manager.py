# progression_manager.py
# Manager for user progression logic and progress calculation

from typing import Dict
from database.db import DatabaseConnection


class ProgressionManager:
    """
    Handles user progression tracking and progress calculations.
    Provides methods to get progress percentages for modules, lessons, and tasks.
    """

    def __init__(self):
        self.db = DatabaseConnection()

    # ------------------------------------------------------------------
    # Progress Calculation Methods
    # ------------------------------------------------------------------

    def get_module_progress(self, module_id: int, user_id: int = 1) -> Dict:
        """
        Calculate progress for a specific module.

        Args:
            module_id: The ID of the module
            user_id: The user ID (default 1 for single-user mode)

        Returns:
            Dict with keys: completed, total, percent
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()

        # Get all tasks for this module (via lessons)
        cursor.execute("""
            SELECT t.id FROM tasks t
            JOIN lessons l ON t.lesson_id = l.id
            WHERE l.module_id = ?
        """, (module_id,))
        all_tasks = cursor.fetchall()
        total = len(all_tasks)

        if total == 0:
            conn.close()
            return {"completed": 0, "total": 0, "percent": 0}

        # Get completed tasks for this module
        cursor.execute("""
            SELECT COUNT(*) FROM progression p
            JOIN tasks t ON p.task_id = t.id
            JOIN lessons l ON t.lesson_id = l.id
            WHERE l.module_id = ? AND p.user_id = ? AND p.status = 'completed'
        """, (module_id, user_id))
        completed = cursor.fetchone()[0]

        conn.close()

        percent = round((completed / total) * 100) if total > 0 else 0
        return {
            "completed": completed,
            "total": total,
            "percent": percent
        }

    def get_lesson_progress(self, lesson_id: int, user_id: int = 1) -> Dict:
        """
        Calculate progress for a specific lesson.

        Args:
            lesson_id: The ID of the lesson
            user_id: The user ID (default 1 for single-user mode)

        Returns:
            Dict with keys: completed, total, percent
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()

        # Get total tasks for this lesson
        cursor.execute(
            "SELECT COUNT(*) FROM tasks WHERE lesson_id = ?",
            (lesson_id,)
        )
        total = cursor.fetchone()[0]

        if total == 0:
            conn.close()
            return {"completed": 0, "total": 0, "percent": 0}

        # Get completed tasks for this lesson
        cursor.execute("""
            SELECT COUNT(*) FROM progression
            WHERE lesson_id = ? AND user_id = ? AND status = 'completed'
        """, (lesson_id, user_id))
        completed = cursor.fetchone()[0]

        conn.close()

        percent = round((completed / total) * 100) if total > 0 else 0
        return {
            "completed": completed,
            "total": total,
            "percent": percent
        }

    def get_task_status(self, task_id: int, user_id: int = 1) -> Dict:
        """
        Get status for a specific task.

        Args:
            task_id: The ID of the task
            user_id: The user ID (default 1 for single-user mode)

        Returns:
            Dict with keys: status, unlocked, is_completed
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT status, unlocked FROM progression
            WHERE task_id = ? AND user_id = ?
        """, (task_id, user_id))
        row = cursor.fetchone()

        conn.close()

        if row:
            return {
                "status": row[0] or "not_started",
                "unlocked": bool(row[1]),
                "is_completed": row[0] == "completed"
            }

        return {
            "status": "not_started",
            "unlocked": False,
            "is_completed": False
        }

    def get_global_progress(self, user_id: int = 1) -> Dict:
        """
        Calculate global progress across all modules.

        Args:
            user_id: The user ID (default 1 for single-user mode)

        Returns:
            Dict with keys:
                - total_modules, completed_modules
                - total_lessons, completed_lessons
                - total_tasks, completed_tasks
                - global_percent
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()

        # Total modules
        cursor.execute("SELECT COUNT(*) FROM modules")
        total_modules = cursor.fetchone()[0]

        # Total lessons
        cursor.execute("SELECT COUNT(*) FROM lessons")
        total_lessons = cursor.fetchone()[0]

        # Total tasks
        cursor.execute("SELECT COUNT(*) FROM tasks")
        total_tasks = cursor.fetchone()[0]

        # Completed tasks
        cursor.execute("""
            SELECT COUNT(*) FROM progression
            WHERE user_id = ? AND status = 'completed' AND task_id IS NOT NULL
        """, (user_id,))
        completed_tasks = cursor.fetchone()[0]

        # Completed lessons (all tasks in lesson completed)
        cursor.execute("SELECT id FROM lessons")
        lesson_ids = [row[0] for row in cursor.fetchall()]
        completed_lessons = 0
        for lesson_id in lesson_ids:
            cursor.execute(
                "SELECT COUNT(*) FROM tasks WHERE lesson_id = ?",
                (lesson_id,)
            )
            total_in_lesson = cursor.fetchone()[0]
            cursor.execute("""
                SELECT COUNT(*) FROM progression
                WHERE lesson_id = ? AND user_id = ? AND status = 'completed'
            """, (lesson_id, user_id))
            completed_in_lesson = cursor.fetchone()[0]
            if total_in_lesson > 0 and completed_in_lesson >= total_in_lesson:
                completed_lessons += 1

        # Completed modules (all lessons in module completed)
        cursor.execute("SELECT id FROM modules")
        module_ids = [row[0] for row in cursor.fetchall()]
        completed_modules = 0
        for module_id in module_ids:
            progress = self.get_module_progress(module_id, user_id)
            if progress["percent"] == 100:
                completed_modules += 1

        conn.close()

        global_percent = round((completed_tasks / total_tasks) * 100) if total_tasks > 0 else 0

        return {
            "total_modules": total_modules,
            "completed_modules": completed_modules,
            "total_lessons": total_lessons,
            "completed_lessons": completed_lessons,
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "global_percent": global_percent
        }

    # ------------------------------------------------------------------
    # Legacy Methods (kept for compatibility)
    # ------------------------------------------------------------------

    def track_progression(self, user_id, module_id, lesson_id, task_id=None,
                          quiz_id=None, exercise_id=None, typing_id=None, status=None):
        """
        Tracks progression for a user.
        """
        pass

    def get_progression(self, user_id):
        """
        Retrieves progression for a user.
        """
        return self.get_global_progress(user_id)
