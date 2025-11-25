# resource_path.py
# Utility for resolving resource paths in both development and PyInstaller builds

import os
import sys


def get_base_path() -> str:
    """
    Get the base path for resources.
    
    Returns the path to the folder containing the executable (PyInstaller)
    or the project root (development mode).
    """
    if getattr(sys, 'frozen', False):
        # Running as compiled executable (PyInstaller)
        return sys._MEIPASS
    else:
        # Running in development mode
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def resource_path(relative_path: str) -> str:
    """
    Get the absolute path to a resource.
    
    Works both in development mode and when packaged with PyInstaller.
    
    Args:
        relative_path: Path relative to the project root (e.g., "assets/styles/style.qss")
    
    Returns:
        Absolute path to the resource
    """
    base = get_base_path()
    return os.path.join(base, relative_path)


def get_user_data_path() -> str:
    """
    Get the path for user data files (writable location).
    
    For PyInstaller --onefile builds, _MEIPASS is read-only,
    so we need a writable location for the database.
    
    Returns:
        Path to user data directory
    """
    if getattr(sys, 'frozen', False):
        # Use AppData folder on Windows for writable data
        app_data = os.environ.get('APPDATA', os.path.expanduser('~'))
        user_data = os.path.join(app_data, 'PyLearnDesktop')
        os.makedirs(user_data, exist_ok=True)
        return user_data
    else:
        # Development mode - use project assets folder
        return os.path.join(get_base_path(), 'assets')


def get_database_path() -> str:
    """
    Get the path to the SQLite database.
    
    In production, copies the bundled database to user data folder
    if it doesn't exist yet.
    
    Returns:
        Path to the database file
    """
    import shutil
    
    if getattr(sys, 'frozen', False):
        # Production: database in user data folder (writable)
        user_db_path = os.path.join(get_user_data_path(), 'pylearn.db')
        
        # Copy bundled database if user database doesn't exist
        if not os.path.exists(user_db_path):
            bundled_db = resource_path(os.path.join('assets', 'pylearn.db'))
            if os.path.exists(bundled_db):
                shutil.copy2(bundled_db, user_db_path)
        
        return user_db_path
    else:
        # Development: database in assets folder
        return resource_path(os.path.join('assets', 'pylearn.db'))
