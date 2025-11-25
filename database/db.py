# db.py
# Database connection manager for PyLearn Desktop

import os
import sqlite3


class Database:
    """Handles SQLite database connection (static methods)."""

    # Resolve DB path relative to the project root (where main.py lives)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DB_PATH = os.path.join(BASE_DIR, "assets", "pylearn.db")

    @staticmethod
    def get_connection():
        """Returns a new database connection."""
        return sqlite3.connect(Database.DB_PATH)

    @staticmethod
    def initialize():
        """Initializes the database and tables."""
        from database.init_db import initialize_tables
        initialize_tables(Database.DB_PATH)


class DatabaseConnection:
    """Instance-based database connection manager for controllers."""

    def __init__(self):
        self.db_path = Database.DB_PATH

    def get_connection(self):
        """Returns a new database connection."""
        return sqlite3.connect(self.db_path)
