# lesson_controller.py
# Controller for managing lessons in PyLearn Desktop

from typing import List, Dict, Optional
from database.db import DatabaseConnection


class LessonController:
    """Controller for lesson-related operations."""

    def __init__(self):
        self.db = DatabaseConnection()

    def load_lessons(self, module_id: int) -> List[Dict]:
        """
        Load all lessons for a given module.

        Args:
            module_id: The ID of the module

        Returns:
            List of dicts with keys: id, module_id, name, description, status
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, module_id, name, description 
            FROM lessons 
            WHERE module_id = ? 
            ORDER BY id
        """, (module_id,))
        rows = cursor.fetchall()

        lessons = []
        for idx, row in enumerate(rows):
            lesson_id, mod_id, name, description = row
            status = self._get_lesson_status(cursor, lesson_id, idx)
            lessons.append({
                "id": lesson_id,
                "module_id": mod_id,
                "name": name,
                "description": description or "",
                "status": status
            })

        conn.close()
        return lessons

    def _get_lesson_status(self, cursor, lesson_id: int, index: int) -> str:
        """
        Get the status of a lesson: 'completed', 'in_progress', or 'locked'.
        """
        # Check progression table
        cursor.execute("""
            SELECT status FROM progression 
            WHERE lesson_id = ? AND user_id = 1
        """, (lesson_id,))
        row = cursor.fetchone()

        if row:
            return row[0]

        # First lesson is always unlocked (in_progress)
        if index == 0:
            return "in_progress"

        # Check if previous lesson is completed
        cursor.execute("""
            SELECT status FROM progression 
            WHERE lesson_id = ? AND status = 'completed'
        """, (lesson_id - 1,))

        if cursor.fetchone():
            return "in_progress"

        return "locked"

    def get_lesson_by_id(self, lesson_id: int) -> Optional[Dict]:
        """
        Get a specific lesson by ID.

        Returns:
            Dict with lesson info or None if not found
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, module_id, name, description FROM lessons WHERE id = ?",
            (lesson_id,)
        )
        row = cursor.fetchone()
        conn.close()

        if row:
            return {
                "id": row[0],
                "module_id": row[1],
                "name": row[2],
                "description": row[3] or ""
            }
        return None

    def add_lesson(self, module_id: int, name: str, description: str = "") -> int:
        """
        Add a new lesson to the database.

        Returns:
            The ID of the newly created lesson
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO lessons (module_id, name, description) VALUES (?, ?, ?)",
            (module_id, name, description)
        )
        lesson_id = cursor.lastrowid

        conn.commit()
        conn.close()

        return lesson_id

    def mark_lesson_completed(self, lesson_id: int) -> None:
        """Mark a lesson as completed for user 1."""
        conn = self.db.get_connection()
        cursor = conn.cursor()

        # Update or insert progression
        cursor.execute("""
            INSERT OR REPLACE INTO progression (user_id, lesson_id, status)
            VALUES (1, ?, 'completed')
        """, (lesson_id,))

        conn.commit()
        conn.close()
