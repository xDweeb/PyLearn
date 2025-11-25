# statistics_view.py
# Statistics screen view for PyLearn Desktop
# Displays global progress statistics and achievements.

from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QProgressBar,
    QGridLayout,
)
from controllers.progression_manager import ProgressionManager


class StatisticsView(QWidget):
    """Statistics screen view with global progress information.

    Signals:
        navigate_back(): emitted when the user clicks the back button.
    """

    # Navigation signals
    navigate_back = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.progression_manager = ProgressionManager()
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Configure the layout and widgets for the statistics page."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(30)

        # Header with back button
        header = QHBoxLayout()
        
        back_btn = QPushButton("← Retour")
        back_btn.setObjectName("secondaryButton")
        back_btn.setFixedWidth(120)
        back_btn.clicked.connect(self.navigate_back.emit)
        header.addWidget(back_btn)
        
        header.addStretch()
        layout.addLayout(header)

        # Title
        title = QLabel("📊 Statistiques")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        subtitle = QLabel("Suivez votre progression d'apprentissage")
        subtitle.setObjectName("subtitleLabel")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)

        # Global progress card
        global_card = self._create_global_progress_card()
        layout.addWidget(global_card)

        # Stats grid
        stats_grid = self._create_stats_grid()
        layout.addLayout(stats_grid)

        layout.addStretch()

    def _create_global_progress_card(self) -> QFrame:
        """Create the main global progress card."""
        card = QFrame()
        card.setObjectName("moduleCard")
        card.setStyleSheet("""
            QFrame#moduleCard {
                background-color: #ffffff;
                border: 1px solid #ddd;
                border-radius: 12px;
                padding: 20px;
            }
        """)

        layout = QVBoxLayout(card)
        layout.setSpacing(15)

        # Title
        title = QLabel("🎯 Progression globale")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(title)

        # Global progress bar
        self.global_progress_bar = QProgressBar()
        self.global_progress_bar.setMinimum(0)
        self.global_progress_bar.setMaximum(100)
        self.global_progress_bar.setValue(0)
        self.global_progress_bar.setTextVisible(True)
        self.global_progress_bar.setFixedHeight(30)
        self.global_progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #3c78d8;
                border-radius: 8px;
                background-color: #f0f0f0;
                text-align: center;
                font-size: 14px;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3c78d8, stop:1 #27ae60);
                border-radius: 6px;
            }
        """)
        layout.addWidget(self.global_progress_bar)

        # Progress details
        self.progress_details = QLabel("Chargement...")
        self.progress_details.setStyleSheet("font-size: 13px; color: #666;")
        self.progress_details.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.progress_details)

        return card

    def _create_stats_grid(self) -> QGridLayout:
        """Create grid of individual stat cards."""
        grid = QGridLayout()
        grid.setSpacing(20)

        # Modules card
        self.modules_card = self._create_stat_card(
            "📚", "Modules", "0/0", "#3c78d8"
        )
        grid.addWidget(self.modules_card, 0, 0)

        # Lessons card
        self.lessons_card = self._create_stat_card(
            "📖", "Leçons", "0/0", "#9b59b6"
        )
        grid.addWidget(self.lessons_card, 0, 1)

        # Tasks card
        self.tasks_card = self._create_stat_card(
            "✅", "Tâches", "0/0", "#27ae60"
        )
        grid.addWidget(self.tasks_card, 0, 2)

        return grid

    def _create_stat_card(self, icon: str, title: str, value: str, color: str) -> QFrame:
        """Create an individual stat card."""
        card = QFrame()
        card.setObjectName("statCard")
        card.setFixedSize(200, 140)
        card.setStyleSheet(f"""
            QFrame#statCard {{
                background-color: #ffffff;
                border: 2px solid {color};
                border-radius: 12px;
            }}
        """)

        layout = QVBoxLayout(card)
        layout.setSpacing(8)
        layout.setContentsMargins(15, 15, 15, 15)

        # Icon
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 32px;")
        icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon_label)

        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet(f"font-size: 14px; font-weight: bold; color: {color};")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Value
        value_label = QLabel(value)
        value_label.setObjectName(f"{title.lower()}_value")
        value_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50;")
        value_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(value_label)

        return card

    def load_statistics(self) -> None:
        """Load and display statistics from the database."""
        stats = self.progression_manager.get_global_progress()

        # Update global progress
        self.global_progress_bar.setValue(stats["global_percent"])
        self.global_progress_bar.setFormat(f"{stats['global_percent']}%")

        # Update details text
        self.progress_details.setText(
            f"Vous avez complété {stats['completed_tasks']} tâches sur {stats['total_tasks']}"
        )

        # Update stat cards
        self._update_stat_card(
            self.modules_card, 
            f"{stats['completed_modules']}/{stats['total_modules']}"
        )
        self._update_stat_card(
            self.lessons_card,
            f"{stats['completed_lessons']}/{stats['total_lessons']}"
        )
        self._update_stat_card(
            self.tasks_card,
            f"{stats['completed_tasks']}/{stats['total_tasks']}"
        )

    def _update_stat_card(self, card: QFrame, value: str) -> None:
        """Update the value label in a stat card."""
        # Find the value label (last QLabel in the card)
        layout = card.layout()
        for i in range(layout.count()):
            widget = layout.itemAt(i).widget()
            if isinstance(widget, QLabel):
                # Check if this is the value label (the last one)
                if i == layout.count() - 1:
                    widget.setText(value)
                    break
