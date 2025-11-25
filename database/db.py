# db.py
# Database connection manager for PyLearn Desktop

import os
import sqlite3
from utils.resource_path import get_database_path


class Database:
    """Handles SQLite database connection (static methods)."""

    # Use the resource path utility for PyInstaller compatibility
    DB_PATH = get_database_path()

    @staticmethod
    def get_connection():
        """Returns a new database connection."""
        return sqlite3.connect(Database.DB_PATH)

    @staticmethod
    def initialize():
        """Initializes the database and tables."""
        # Update DB_PATH in case it changed
        Database.DB_PATH = get_database_path()
        from database.init_db import initialize_tables
        initialize_tables(Database.DB_PATH)


class DatabaseConnection:
    """Instance-based database connection manager for controllers."""

    def __init__(self):
        self.db_path = get_database_path()

    def get_connection(self):
        """Returns a new database connection."""
        return sqlite3.connect(self.db_path)
