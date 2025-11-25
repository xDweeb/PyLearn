# task_controller.py
# Controller for managing tasks in PyLearn Desktop

from typing import List, Dict, Optional
from database.db import DatabaseConnection


class TaskController:
    """Controller for task-related operations."""

    def __init__(self):
        self.db = DatabaseConnection()

    def load_tasks(self, lesson_id: int) -> List[Dict]:
        """
        Load all tasks for a given lesson.

        Args:
            lesson_id: The ID of the lesson

        Returns:
            List of dicts with keys: id, lesson_id, name, task_type, description, is_completed
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, lesson_id, name, task_type, description 
            FROM tasks 
            WHERE lesson_id = ? 
            ORDER BY id
        """, (lesson_id,))
        rows = cursor.fetchall()

        tasks = []
        for row in rows:
            task_id, les_id, name, task_type, description = row
            is_completed = self._is_task_completed(cursor, task_id)
            tasks.append({
                "id": task_id,
                "lesson_id": les_id,
                "name": name,
                "task_type": task_type or "theory",
                "description": description or "",
                "is_completed": is_completed
            })

        conn.close()
        return tasks

    def _is_task_completed(self, cursor, task_id: int) -> bool:
        """Check if a task is completed for user 1."""
        cursor.execute("""
            SELECT status FROM progression 
            WHERE task_id = ? AND user_id = 1 AND status = 'completed'
        """, (task_id,))
        return cursor.fetchone() is not None

    def get_task_by_id(self, task_id: int) -> Optional[Dict]:
        """
        Get a specific task by ID.

        Returns:
            Dict with task info or None if not found
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, lesson_id, name, task_type, description, content FROM tasks WHERE id = ?",
            (task_id,)
        )
        row = cursor.fetchone()
        conn.close()

        if row:
            return {
                "id": row[0],
                "lesson_id": row[1],
                "name": row[2],
                "task_type": row[3] or "theory",
                "description": row[4] or "",
                "content": row[5] or ""
            }
        return None

    def add_task(self, lesson_id: int, name: str, task_type: str = "theory", description: str = "") -> int:
        """
        Add a new task to the database.

        Returns:
            The ID of the newly created task
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO tasks (lesson_id, name, task_type, description) VALUES (?, ?, ?, ?)",
            (lesson_id, name, task_type, description)
        )
        task_id = cursor.lastrowid

        conn.commit()
        conn.close()

        return task_id

    def mark_task_completed(self, task_id: int) -> None:
        """Mark a task as completed for user 1."""
        conn = self.db.get_connection()
        cursor = conn.cursor()

        # Get task info to also store lesson_id
        cursor.execute("SELECT lesson_id FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        lesson_id = row[0] if row else None

        # Update or insert progression
        cursor.execute("""
            INSERT OR REPLACE INTO progression (user_id, task_id, lesson_id, status)
            VALUES (1, ?, ?, 'completed')
        """, (task_id, lesson_id))

        conn.commit()
        conn.close()

    # ------------------------------------------------------------------
    # Content Loading Methods
    # ------------------------------------------------------------------

    def load_task_content(self, task_id: int) -> Dict:
        """
        Load full content for a specific task based on its type.

        Returns:
            Dict with structured content:
            {
                "type": "theory" | "quiz" | "typing" | "exercise",
                "task_id": int,
                "lesson_id": int,
                "name": str,
                "description": str,
                "content": str (for theory),
                "question": str (for quiz),
                "answer": str (for quiz),
                "text": str (for typing),
                "prompt": str (for exercise),
                "solution": str (for exercise)
            }
        """
        task = self.get_task_by_id(task_id)
        if not task:
            return {}

        task_type = task["task_type"]
        lesson_id = task["lesson_id"]

        result = {
            "type": task_type,
            "task_id": task["id"],
            "lesson_id": lesson_id,
            "name": task["name"],
            "description": task["description"]
        }

        if task_type == "theory":
            result["content"] = task.get("content", "")
        elif task_type == "quiz":
            quiz_data = self.load_quiz(lesson_id)
            result["question"] = quiz_data.get("question", "")
            result["answer"] = quiz_data.get("answer", "")
        elif task_type == "typing":
            typing_data = self.load_typing(lesson_id)
            result["text"] = typing_data.get("text", "")
        elif task_type == "exercise":
            exercise_data = self.load_exercise(lesson_id)
            result["prompt"] = exercise_data.get("prompt", "")
            result["solution"] = exercise_data.get("solution", "")

        return result

    def load_quiz(self, lesson_id: int) -> Dict:
        """
        Load quiz content for a lesson.

        Returns:
            Dict with keys: question, answer
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT question, answer FROM quiz WHERE lesson_id = ? LIMIT 1",
            (lesson_id,)
        )
        row = cursor.fetchone()
        conn.close()

        if row:
            return {
                "question": row[0] or "",
                "answer": row[1] or ""
            }
        return {"question": "", "answer": ""}

    def load_typing(self, lesson_id: int) -> Dict:
        """
        Load typing content for a lesson.

        Returns:
            Dict with key: text
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT text FROM typing WHERE lesson_id = ? LIMIT 1",
            (lesson_id,)
        )
        row = cursor.fetchone()
        conn.close()

        if row:
            return {"text": row[0] or ""}
        return {"text": ""}

    def load_exercise(self, lesson_id: int) -> Dict:
        """
        Load exercise content for a lesson.

        Returns:
            Dict with keys: prompt, solution
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT prompt, solution FROM exercise WHERE lesson_id = ? LIMIT 1",
            (lesson_id,)
        )
        row = cursor.fetchone()
        conn.close()

        if row:
            return {
                "prompt": row[0] or "",
                "solution": row[1] or ""
            }
        return {"prompt": "", "solution": ""}

    def get_task_content(self, task_id: int) -> Dict:
        """
        Legacy method - use load_task_content() instead.
        Get the content for a specific task based on its type.

        Returns:
            Dict with task content (varies by type)
        """
        return self.load_task_content(task_id)
