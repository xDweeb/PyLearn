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
            List of dicts with keys: id, lesson_id, name, task_type, description, 
                                      is_completed, is_unlocked, status
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
            progression = self._get_task_progression(cursor, task_id)
            tasks.append({
                "id": task_id,
                "lesson_id": les_id,
                "name": name,
                "task_type": task_type or "theory",
                "description": description or "",
                "is_completed": progression["status"] == "completed",
                "is_unlocked": progression["unlocked"],
                "status": progression["status"]
            })

        conn.close()
        return tasks

    def _get_task_progression(self, cursor, task_id: int) -> Dict:
        """Get progression info for a task."""
        cursor.execute("""
            SELECT status, unlocked FROM progression 
            WHERE task_id = ? AND user_id = 1
        """, (task_id,))
        row = cursor.fetchone()
        
        if row:
            return {"status": row[0] or "not_started", "unlocked": bool(row[1])}
        # Default: first task should be unlocked
        return {"status": "not_started", "unlocked": True}

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

    # ------------------------------------------------------------------
    # Task Validation Methods
    # ------------------------------------------------------------------

    def validate_task(self, task_id: int, user_input: str = "") -> Dict:
        """
        Validate a task based on its type and user input.

        Args:
            task_id: The ID of the task to validate
            user_input: The user's input/answer (if applicable)

        Returns:
            Dict with keys:
                - success: bool - Whether validation passed
                - message: str - Feedback message
                - unlock_next: bool - Whether next task was unlocked
        """
        task = self.get_task_by_id(task_id)
        if not task:
            return {
                "success": False,
                "message": "Tâche non trouvée.",
                "unlock_next": False
            }

        task_type = task["task_type"]
        lesson_id = task["lesson_id"]

        # Validate based on task type
        if task_type == "theory":
            success, message = self._validate_theory(task_id)
        elif task_type == "quiz":
            success, message = self._validate_quiz(lesson_id, user_input)
        elif task_type == "typing":
            success, message = self._validate_typing(lesson_id, user_input)
        elif task_type == "exercise":
            success, message = self._validate_exercise(lesson_id, user_input)
        else:
            success, message = False, "Type de tâche inconnu."

        # Update progression and unlock next if successful
        unlock_next = False
        if success:
            self._update_task_status(task_id, "completed")
            unlock_next = self._unlock_next_task(task_id, lesson_id)
        else:
            self._update_task_status(task_id, "failed")

        return {
            "success": success,
            "message": message,
            "unlock_next": unlock_next
        }

    def _validate_theory(self, task_id: int) -> tuple:
        """Validate theory task - always passes."""
        return True, "Théorie marquée comme lue ! ✓"

    def _validate_quiz(self, lesson_id: int, user_input: str) -> tuple:
        """Validate quiz answer."""
        quiz_data = self.load_quiz(lesson_id)
        correct_answer = quiz_data.get("answer", "").strip().upper()
        user_answer = user_input.strip().upper()

        if not user_answer:
            return False, "Veuillez entrer une réponse."

        if user_answer == correct_answer:
            return True, "Bonne réponse ! ✓"
        else:
            return False, f"Incorrect. La bonne réponse était: {correct_answer}"

    def _validate_typing(self, lesson_id: int, user_input: str) -> tuple:
        """Validate typing task - exact match with whitespace stripped."""
        typing_data = self.load_typing(lesson_id)
        target_text = typing_data.get("text", "").strip()
        user_text = user_input.strip()

        if not user_text:
            return False, "Veuillez saisir le texte demandé."

        if user_text == target_text:
            return True, "Parfait ! Texte correct ! ✓"
        else:
            # Calculate similarity for feedback
            similarity = self._calculate_similarity(target_text, user_text)
            if similarity > 0.8:
                return False, "Presque ! Vérifiez les petites différences."
            else:
                return False, "Le texte ne correspond pas. Réessayez."

    def _validate_exercise(self, lesson_id: int, user_input: str) -> tuple:
        """Validate exercise - simple string match."""
        exercise_data = self.load_exercise(lesson_id)
        solution = exercise_data.get("solution", "").strip()
        user_code = user_input.strip()

        if not user_code:
            return False, "Veuillez écrire votre code."

        # Normalize both strings for comparison (remove extra whitespace)
        normalized_solution = self._normalize_code(solution)
        normalized_user = self._normalize_code(user_code)

        if normalized_user == normalized_solution:
            return True, "Excellent ! Code correct ! ✓"
        else:
            # Check if it's close
            if self._calculate_similarity(normalized_solution, normalized_user) > 0.7:
                return False, "Presque correct ! Vérifiez votre syntaxe."
            else:
                return False, "Le code ne correspond pas à la solution attendue."

    def _normalize_code(self, code: str) -> str:
        """Normalize code for comparison."""
        # Remove extra whitespace and normalize line endings
        lines = [line.strip() for line in code.strip().split('\n') if line.strip()]
        return '\n'.join(lines)

    def _calculate_similarity(self, str1: str, str2: str) -> float:
        """Calculate simple similarity ratio between two strings."""
        if not str1 or not str2:
            return 0.0
        
        # Simple character-based similarity
        matches = sum(1 for a, b in zip(str1, str2) if a == b)
        max_len = max(len(str1), len(str2))
        return matches / max_len if max_len > 0 else 0.0

    def _update_task_status(self, task_id: int, status: str) -> None:
        """Update task status in progression table."""
        conn = self.db.get_connection()
        cursor = conn.cursor()

        # Get lesson_id for the task
        cursor.execute("SELECT lesson_id FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        lesson_id = row[0] if row else None

        # Check if progression entry exists
        cursor.execute(
            "SELECT id FROM progression WHERE task_id = ? AND user_id = 1",
            (task_id,)
        )
        exists = cursor.fetchone()

        if exists:
            cursor.execute("""
                UPDATE progression 
                SET status = ?, unlocked = 1
                WHERE task_id = ? AND user_id = 1
            """, (status, task_id))
        else:
            cursor.execute("""
                INSERT INTO progression (user_id, task_id, lesson_id, status, unlocked)
                VALUES (1, ?, ?, ?, 1)
            """, (task_id, lesson_id, status))

        conn.commit()
        conn.close()

    def _unlock_next_task(self, current_task_id: int, lesson_id: int) -> bool:
        """Unlock the next task in the lesson. Returns True if a task was unlocked."""
        conn = self.db.get_connection()
        cursor = conn.cursor()

        # Get all tasks for this lesson ordered by id
        cursor.execute("""
            SELECT id FROM tasks 
            WHERE lesson_id = ? 
            ORDER BY id
        """, (lesson_id,))
        task_ids = [row[0] for row in cursor.fetchall()]

        # Find current task index and get next task
        try:
            current_index = task_ids.index(current_task_id)
            if current_index < len(task_ids) - 1:
                next_task_id = task_ids[current_index + 1]
                
                # Check if progression entry exists for next task
                cursor.execute(
                    "SELECT id FROM progression WHERE task_id = ? AND user_id = 1",
                    (next_task_id,)
                )
                exists = cursor.fetchone()

                if exists:
                    cursor.execute("""
                        UPDATE progression 
                        SET unlocked = 1
                        WHERE task_id = ? AND user_id = 1
                    """, (next_task_id,))
                else:
                    cursor.execute("""
                        INSERT INTO progression (user_id, task_id, lesson_id, status, unlocked)
                        VALUES (1, ?, ?, 'not_started', 1)
                    """, (next_task_id, lesson_id))

                conn.commit()
                conn.close()
                return True
        except ValueError:
            pass

        conn.close()
        return False

    def is_task_unlocked(self, task_id: int) -> bool:
        """Check if a task is unlocked for user 1."""
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT unlocked FROM progression 
            WHERE task_id = ? AND user_id = 1
        """, (task_id,))
        row = cursor.fetchone()
        conn.close()

        return bool(row[0]) if row else False
