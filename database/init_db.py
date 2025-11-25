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
        content TEXT,
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
    # Insert Tasks with Content for each Lesson
    # ------------------------------------------------------------------
    # Lesson 1: Introduction à Python
    _insert_lesson_tasks(cursor, 1, {
        "theory": "Python est un langage de programmation interprété, facile à apprendre et très populaire. Il est utilisé pour le développement web, l'analyse de données, l'intelligence artificielle et bien plus encore.\n\nCaractéristiques principales:\n• Syntaxe claire et lisible\n• Typage dynamique\n• Grande bibliothèque standard\n• Communauté active",
        "quiz_question": "Quel type de langage est Python?\n\nA) Compilé\nB) Interprété\nC) Assembleur\nD) Machine",
        "quiz_answer": "B",
        "typing_text": "print('Bienvenue en Python!')",
        "exercise_prompt": "Écrivez un programme qui affiche 'Hello, World!' dans la console.",
        "exercise_solution": "print('Hello, World!')"
    })

    # Lesson 2: La fonction print()
    _insert_lesson_tasks(cursor, 2, {
        "theory": "La fonction print() permet d'afficher du texte ou des valeurs dans la console.\n\nSyntaxe:\nprint('votre texte')\nprint(variable)\n\nExemples:\nprint('Bonjour')\nprint(42)\nprint('Résultat:', 10 + 5)",
        "quiz_question": "Quelle syntaxe est correcte pour afficher 'Salut'?\n\nA) print Salut\nB) print('Salut')\nC) echo('Salut')\nD) display('Salut')",
        "quiz_answer": "B",
        "typing_text": "print('Hello, Python!')\nprint(2024)",
        "exercise_prompt": "Utilisez print() pour afficher votre prénom sur une ligne et votre âge sur la ligne suivante.",
        "exercise_solution": "print('Jean')\nprint(25)"
    })

    # Lesson 3: La fonction input()
    _insert_lesson_tasks(cursor, 3, {
        "theory": "La fonction input() permet de récupérer une entrée utilisateur depuis la console.\n\nSyntaxe:\nvariable = input('Message à afficher: ')\n\nExemple:\nnom = input('Entrez votre nom: ')\nprint('Bonjour', nom)\n\nNote: input() retourne toujours une chaîne de caractères (str).",
        "quiz_question": "Quel type de données retourne input()?\n\nA) int\nB) float\nC) str\nD) bool",
        "quiz_answer": "C",
        "typing_text": "nom = input('Votre nom: ')\nprint('Bonjour', nom)",
        "exercise_prompt": "Demandez à l'utilisateur son prénom avec input(), puis affichez 'Bienvenue, [prénom]!'",
        "exercise_solution": "prenom = input('Entrez votre prénom: ')\nprint('Bienvenue,', prenom + '!')"
    })

    # Lesson 4: Commentaires en Python
    _insert_lesson_tasks(cursor, 4, {
        "theory": "Les commentaires permettent de documenter votre code sans affecter son exécution.\n\nCommentaire sur une ligne:\n# Ceci est un commentaire\n\nCommentaire multi-lignes:\n'''\nCeci est un\ncommentaire sur\nplusieurs lignes\n'''\n\nBonne pratique: Commentez votre code pour le rendre compréhensible!",
        "quiz_question": "Comment écrire un commentaire sur une ligne en Python?\n\nA) // commentaire\nB) /* commentaire */\nC) # commentaire\nD) -- commentaire",
        "quiz_answer": "C",
        "typing_text": "# Mon premier programme\nprint('Hello')  # Affiche Hello",
        "exercise_prompt": "Écrivez un programme avec un commentaire expliquant ce que fait le code, suivi d'un print().",
        "exercise_solution": "# Ce programme affiche un message de bienvenue\nprint('Bienvenue dans PyLearn!')"
    })

    # ------------------------------------------------------------------
    # Insert initial progression for user 1 (first lesson unlocked)
    # ------------------------------------------------------------------
    cursor.execute(
        "INSERT INTO progression (user_id, module_id, lesson_id, status) VALUES (?, ?, ?, ?)",
        (1, 1, 1, "in_progress")
    )

    conn.commit()


def _insert_lesson_tasks(cursor, lesson_id: int, content: dict) -> None:
    """Insert tasks and their content for a specific lesson."""
    
    # Task 1: Theory
    cursor.execute(
        "INSERT INTO tasks (lesson_id, name, task_type, description, content) VALUES (?, ?, ?, ?, ?)",
        (lesson_id, "Théorie", "theory", "Lire la théorie de la leçon", content["theory"])
    )

    # Task 2: Quiz
    cursor.execute(
        "INSERT INTO tasks (lesson_id, name, task_type, description, content) VALUES (?, ?, ?, ?, ?)",
        (lesson_id, "Quiz", "quiz", "Répondre aux questions du quiz", None)
    )
    cursor.execute(
        "INSERT INTO quiz (lesson_id, question, answer) VALUES (?, ?, ?)",
        (lesson_id, content["quiz_question"], content["quiz_answer"])
    )

    # Task 3: Typing
    cursor.execute(
        "INSERT INTO tasks (lesson_id, name, task_type, description, content) VALUES (?, ?, ?, ?, ?)",
        (lesson_id, "Typing", "typing", "Pratiquer la frappe de code", None)
    )
    cursor.execute(
        "INSERT INTO typing (lesson_id, text) VALUES (?, ?)",
        (lesson_id, content["typing_text"])
    )

    # Task 4: Exercise
    cursor.execute(
        "INSERT INTO tasks (lesson_id, name, task_type, description, content) VALUES (?, ?, ?, ?, ?)",
        (lesson_id, "Exercice", "exercise", "Compléter l'exercice de code", None)
    )
    cursor.execute(
        "INSERT INTO exercise (lesson_id, prompt, solution) VALUES (?, ?, ?)",
        (lesson_id, content["exercise_prompt"], content["exercise_solution"])
    )
