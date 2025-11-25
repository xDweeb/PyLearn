# main.py
# Entry point for PyLearn Desktop application

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from database.db import Database
from gui.home_view import HomeView

class MainWindow(QMainWindow):
    """
    Main application window with stacked widget for navigation.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyLearn Desktop")
        self.setGeometry(100, 100, 1024, 768)

        # Stacked widget for navigation between views
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Initialize HomeView and add to stacked widget
        self.home_view = HomeView()
        self.stacked_widget.addWidget(self.home_view)
        self.stacked_widget.setCurrentWidget(self.home_view)

        # TODO: Add other views and navigation logic

if __name__ == "__main__":
    # Initialize database
    Database.initialize()

    # Start Qt application
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
