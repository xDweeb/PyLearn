# home_view.py
# Home screen view for PyLearn Desktop
# Defines the main landing UI with title, subtitle, primary/secondary actions,
# and a small preview of available modules.

from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QSizePolicy,
    QProgressBar,
)
from controllers.progression_manager import ProgressionManager
from controllers.module_controller import ModuleController


class HomeView(QWidget):
    """Home screen view with main actions and module preview cards.

    Signals:
        navigate_to_modules: emitted when the user clicks "Commencer l'apprentissage".
        navigate_continue: emitted when the user clicks "Continuer".
        navigate_to_statistics: emitted when the user clicks "Statistiques".
    """

    navigate_to_modules = Signal()
    navigate_continue = Signal()
    navigate_to_statistics = Signal()

    def __init__(self) -> None:
        super().__init__()
        self.progression_manager = ProgressionManager()
        self.module_controller = ModuleController()
        self._setup_ui()

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------
    def _setup_ui(self) -> None:
        """Configure the full layout and widgets for the home screen."""
        # Global vertical layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(30)

        # Title section (centered)
        header_layout = QVBoxLayout()
        header_layout.setSpacing(10)
        header_layout.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

        title_label = QLabel("PyLearn Desktop")
        title_label.setObjectName("titleLabel")
        title_label.setAlignment(Qt.AlignHCenter)

        subtitle_label = QLabel("Bienvenue dans votre espace d'apprentissage")
        subtitle_label.setObjectName("subtitleLabel")
        subtitle_label.setAlignment(Qt.AlignHCenter)

        header_layout.addWidget(title_label)
        header_layout.addWidget(subtitle_label)

        # Global progress section
        progress_section = self._create_global_progress_section()

        # Call-to-action buttons (centered)
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(16)
        buttons_layout.setAlignment(Qt.AlignHCenter)

        start_button = QPushButton("Commencer l'apprentissage")
        start_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        start_button.clicked.connect(self._on_start_clicked)

        continue_button = QPushButton("Continuer")
        continue_button.setObjectName("secondaryButton")
        continue_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        continue_button.clicked.connect(self._on_continue_clicked)

        stats_button = QPushButton("📊 Statistiques")
        stats_button.setObjectName("secondaryButton")
        stats_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        stats_button.clicked.connect(self._on_stats_clicked)

        buttons_layout.addWidget(start_button)
        buttons_layout.addWidget(continue_button)
        buttons_layout.addWidget(stats_button)

        # Module preview section
        modules_section_layout = QVBoxLayout()
        modules_section_layout.setSpacing(12)

        section_title = QLabel("Aperçu des modules")
        section_title.setObjectName("sectionTitle")
        modules_section_layout.addWidget(section_title)

        # Container for dynamic module cards
        self.modules_list_layout = QVBoxLayout()
        self.modules_list_layout.setSpacing(10)
        modules_section_layout.addLayout(self.modules_list_layout)

        # Assemble main layout
        main_layout.addLayout(header_layout)
        main_layout.addWidget(progress_section)
        main_layout.addLayout(buttons_layout)
        main_layout.addLayout(modules_section_layout)
        main_layout.addStretch()  # Push content towards the top with breathing space

        self.setLayout(main_layout)

        # Load dynamic content
        self._load_modules_preview()

    def _create_global_progress_section(self) -> QFrame:
        """Create a global progress bar section."""
        frame = QFrame()
        frame.setObjectName("progressSection")
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(8)

        # Progress label
        self.progress_label = QLabel("Progression globale: 0%")
        self.progress_label.setAlignment(Qt.AlignCenter)

        # Progress bar
        self.global_progress_bar = QProgressBar()
        self.global_progress_bar.setMinimum(0)
        self.global_progress_bar.setMaximum(100)
        self.global_progress_bar.setValue(0)
        self.global_progress_bar.setTextVisible(False)
        self.global_progress_bar.setFixedHeight(12)
        self.global_progress_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                border-radius: 6px;
                background-color: #e0e0e0;
            }
            QProgressBar::chunk {
                border-radius: 6px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4CAF50, stop:1 #8BC34A);
            }
        """)

        layout.addWidget(self.progress_label)
        layout.addWidget(self.global_progress_bar)

        return frame

    def _load_modules_preview(self) -> None:
        """Load modules from database with dynamic progress."""
        # Clear existing cards
        while self.modules_list_layout.count():
            child = self.modules_list_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Get global progress
        global_stats = self.progression_manager.get_global_progress()
        global_percent = global_stats.get("global_percent", 0)
        self.global_progress_bar.setValue(global_percent)
        self.progress_label.setText(f"Progression globale: {global_percent}%")

        # Load modules from database
        modules = self.module_controller.get_all_modules()

        # Show first 3 modules as preview
        for module in modules[:3]:
            module_id = module.get("id")
            title = module.get("title", "Module")
            unlocked = module.get("unlocked", False)

            # Get progress for this module
            progress = self.progression_manager.get_module_progress(module_id)
            percent = progress.get("percent", 0)

            if unlocked:
                status_text = f"{percent}%"
            else:
                status_text = "Verrouillé"

            card = self._create_module_card(
                title=title,
                status_text=status_text,
                locked=not unlocked,
                progress_percent=percent if unlocked else 0,
            )
            self.modules_list_layout.addWidget(card)

    def _create_module_card(self, title: str, status_text: str, locked: bool, progress_percent: int = 0) -> QFrame:
        """Create a simple horizontal module card with progress."""
        card = QFrame()
        card.setObjectName("moduleCard")
        card.setFrameShape(QFrame.StyledPanel)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(6)

        # Top row with icon, title, status
        top_row = QHBoxLayout()
        top_row.setSpacing(12)

        # Optional lock icon
        if locked:
            lock_label = QLabel("🔒")
            lock_label.setAlignment(Qt.AlignCenter)
            top_row.addWidget(lock_label)
        else:
            check_label = QLabel("📚")
            top_row.addWidget(check_label)

        # Module title
        title_label = QLabel(title)
        top_row.addWidget(title_label, stretch=1)

        # Status text
        status_label = QLabel(status_text)
        status_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        top_row.addWidget(status_label)

        layout.addLayout(top_row)

        # Progress bar (only for unlocked modules)
        if not locked:
            progress_bar = QProgressBar()
            progress_bar.setMinimum(0)
            progress_bar.setMaximum(100)
            progress_bar.setValue(progress_percent)
            progress_bar.setTextVisible(False)
            progress_bar.setFixedHeight(6)
            progress_bar.setStyleSheet("""
                QProgressBar {
                    border: none;
                    border-radius: 3px;
                    background-color: #e0e0e0;
                }
                QProgressBar::chunk {
                    border-radius: 3px;
                    background-color: #4CAF50;
                }
            """)
            layout.addWidget(progress_bar)

        return card

    def refresh_data(self) -> None:
        """Refresh the home view with latest progress data."""
        self._load_modules_preview()

    # ------------------------------------------------------------------
    # Signal emitters
    # ------------------------------------------------------------------
    def _on_start_clicked(self) -> None:
        """Emit navigation signal when the user starts learning."""
        self.navigate_to_modules.emit()

    def _on_continue_clicked(self) -> None:
        """Emit navigation signal when the user wants to continue."""
        self.navigate_continue.emit()

    def _on_stats_clicked(self) -> None:
        """Emit navigation signal when the user wants to see statistics."""
        self.navigate_to_statistics.emit()
