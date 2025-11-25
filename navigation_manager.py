# navigation_manager.py
# Central navigation manager for PyLearn Desktop.

from typing import Dict, Optional
from PySide6.QtWidgets import QWidget


class NavigationManager:
    """Simple registry-based navigation manager.

    Responsibilities:
    - Keep a mapping between view names and QWidget instances.
    - Provide access to views by name.
    - Provide a high-level navigate(name) API that the MainWindow can use.
    """

    def __init__(self) -> None:
        # Internal mapping of view name -> QWidget instance
        self._views: Dict[str, QWidget] = {}
        # Optional callback that is invoked when navigate() is called.
        # MainWindow should set this to a function that actually performs
        # the stacked widget switching.
        self._navigation_callback = None

    def register_view(self, name: str, widget: QWidget) -> None:
        """Register a view under a specific name."""
        self._views[name] = widget

    def get_view(self, name: str) -> Optional[QWidget]:
        """Retrieve a view by its registered name."""
        return self._views.get(name)

    def navigate(self, name: str) -> None:
        """High-level navigation entry point.

        Delegates to a callback set by MainWindow, keeping this class
        free of any direct dependency on QMainWindow/QStackedWidget.
        """
        if self._navigation_callback is not None:
            self._navigation_callback(name)

    def set_navigation_callback(self, callback) -> None:
        """Set the function that is called when navigate(name) is invoked."""
        self._navigation_callback = callback
