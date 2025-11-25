# init_db.py
# SQLite database initialization for PyLearn Desktop

def initialize_tables(db_path):
    """
    Creates required tables if they do not exist.
    """
    import sqlite3
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
        user_id INTEGER,
        module_id INTEGER,
        lesson_id INTEGER,
        task_id INTEGER,
        quiz_id INTEGER,
        exercise_id INTEGER,
        typing_id INTEGER,
        status TEXT
    );
    """)
    conn.commit()
    conn.close()
