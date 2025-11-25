# init_db.py
# SQLite database initialization for PyLearn Desktop
# Creates tables and inserts default data if tables are empty.

import sqlite3


def initialize_tables(db_path: str) -> None:
    """Creates required tables if they do not exist."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Table definitions
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS modules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS lessons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        module_id INTEGER,
        name TEXT NOT NULL,
        description TEXT,
        FOREIGN KEY(module_id) REFERENCES modules(id)
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lesson_id INTEGER,
        name TEXT NOT NULL,
        task_type TEXT,
        description TEXT,
        FOREIGN KEY(lesson_id) REFERENCES lessons(id)
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS quiz (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lesson_id INTEGER,
        question TEXT NOT NULL,
        answer TEXT,
        FOREIGN KEY(lesson_id) REFERENCES lessons(id)
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS exercise (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lesson_id INTEGER,
        prompt TEXT NOT NULL,
        solution TEXT,
        FOREIGN KEY(lesson_id) REFERENCES lessons(id)
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS typing (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lesson_id INTEGER,
        text TEXT NOT NULL,
        FOREIGN KEY(lesson_id) REFERENCES lessons(id)
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS progression (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER DEFAULT 1,
        module_id INTEGER,
        lesson_id INTEGER,
        task_id INTEGER,
        status TEXT DEFAULT 'not_started',
        FOREIGN KEY(module_id) REFERENCES modules(id),
        FOREIGN KEY(lesson_id) REFERENCES lessons(id),
        FOREIGN KEY(task_id) REFERENCES tasks(id)
    );
    """)

    conn.commit()

    # Insert default data if tables are empty
    _insert_default_data(conn)

    conn.close()


def _insert_default_data(conn: sqlite3.Connection) -> None:
    """Insert default modules, lessons, and tasks if tables are empty."""
    cursor = conn.cursor()

    # Check if modules table is empty
    cursor.execute("SELECT COUNT(*) FROM modules")
    if cursor.fetchone()[0] > 0:
        # Data already exists, skip insertion
        return

    # ------------------------------------------------------------------
    # Insert Modules
    # ------------------------------------------------------------------
    modules = [
        ("Python Start", "Introduction aux bases de Python"),
        ("Variables", "Découvrir les types et variables"),
        ("Strings", "Manipuler les chaînes de caractères"),
    ]
    cursor.executemany(
        "INSERT INTO modules (name, description) VALUES (?, ?)",
        modules
    )

    # ------------------------------------------------------------------
    # Insert Lessons for Module 1 (Python Start)
    # ------------------------------------------------------------------
    lessons_module_1 = [
        (1, "Introduction à Python", "Premiers pas avec Python"),
        (1, "La fonction print()", "Afficher du texte dans la console"),
        (1, "La fonction input()", "Récupérer des entrées utilisateur"),
        (1, "Commentaires en Python", "Documenter votre code"),
    ]
    cursor.executemany(
        "INSERT INTO lessons (module_id, name, description) VALUES (?, ?, ?)",
        lessons_module_1
    )

    # ------------------------------------------------------------------
    # Insert Tasks for each Lesson
    # Each lesson gets 4 tasks: Théorie, Quiz, Typing, Exercice
    # ------------------------------------------------------------------
    task_templates = [
        ("Théorie", "theory", "Lire la théorie de la leçon"),
        ("Quiz", "quiz", "Répondre aux questions du quiz"),
        ("Typing", "typing", "Pratiquer la frappe de code"),
        ("Exercice", "exercise", "Compléter l'exercice de code"),
    ]

    # Get all lesson IDs
    cursor.execute("SELECT id FROM lessons")
    lesson_ids = [row[0] for row in cursor.fetchall()]

    for lesson_id in lesson_ids:
        for task_name, task_type, task_desc in task_templates:
            cursor.execute(
                "INSERT INTO tasks (lesson_id, name, task_type, description) VALUES (?, ?, ?, ?)",
                (lesson_id, task_name, task_type, task_desc)
            )

    # ------------------------------------------------------------------
    # Insert initial progression for user 1 (first lesson unlocked)
    # ------------------------------------------------------------------
    # Mark first lesson of module 1 as "in_progress"
    cursor.execute(
        "INSERT INTO progression (user_id, module_id, lesson_id, status) VALUES (?, ?, ?, ?)",
        (1, 1, 1, "in_progress")
    )

    conn.commit()
