# module_controller.py
# Controller for managing modules in PyLearn Desktop

from typing import List, Dict, Optional
from database.db import DatabaseConnection


class ModuleController:
    """Controller for module-related operations."""

    def __init__(self):
        self.db = DatabaseConnection()

    def load_modules(self) -> List[Dict]:
        """
        Load all modules from the database.

        Returns:
            List of dicts with keys: id, name, description, is_unlocked
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id, name, description FROM modules ORDER BY id")
        rows = cursor.fetchall()

        modules = []
        for row in rows:
            module_id, name, description = row
            # Check if module is unlocked (has progression entry or is first module)
            is_unlocked = self._is_module_unlocked(cursor, module_id)
            modules.append({
                "id": module_id,
                "name": name,
                "description": description or "",
                "is_unlocked": is_unlocked
            })

        conn.close()
        return modules

    def _is_module_unlocked(self, cursor, module_id: int) -> bool:
        """Check if a module is unlocked for the user."""
        # First module is always unlocked
        if module_id == 1:
            return True

        # Check if previous module is completed
        cursor.execute("""
            SELECT COUNT(*) FROM progression 
            WHERE module_id = ? AND status = 'completed'
        """, (module_id - 1,))

        return cursor.fetchone()[0] > 0

    def get_module_by_id(self, module_id: int) -> Optional[Dict]:
        """
        Get a specific module by ID.

        Returns:
            Dict with module info or None if not found
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, name, description FROM modules WHERE id = ?",
            (module_id,)
        )
        row = cursor.fetchone()
        conn.close()

        if row:
            return {
                "id": row[0],
                "name": row[1],
                "description": row[2] or ""
            }
        return None

    def add_module(self, name: str, description: str = "") -> int:
        """
        Add a new module to the database.

        Returns:
            The ID of the newly created module
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO modules (name, description) VALUES (?, ?)",
            (name, description)
        )
        module_id = cursor.lastrowid

        conn.commit()
        conn.close()

        return module_id
