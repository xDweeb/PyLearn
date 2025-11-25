# db.py
# Database connection manager for PyLearn Desktop

import sqlite3

class Database:
    """
    Handles SQLite database connection.
    """
    DB_PATH = "pylearn_desktop/assets/pylearn.db"

    @staticmethod
    def get_connection():
        """
        Returns a new database connection.
        """
        return sqlite3.connect(Database.DB_PATH)

    @staticmethod
    def initialize():
        """
        Initializes the database and tables.
        """
        from database.init_db import initialize_tables
        initialize_tables(Database.DB_PATH)
