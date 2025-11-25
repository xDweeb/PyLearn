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
)

class HomeView(QWidget):
    """Home screen view with main actions and module preview cards.

    Signals:
        navigate_to_modules: emitted when the user clicks "Commencer l'apprentissage".
        navigate_continue: emitted when the user clicks "Continuer".
    """

    navigate_to_modules = Signal()
    navigate_continue = Signal()

    def __init__(self) -> None:
        super().__init__()
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
        title_label.setAlignment(Qt.AlignHCenter)
        title_label.setStyleSheet(
            "font-size: 32px; font-weight: 700;"
        )

        subtitle_label = QLabel("Bienvenue dans votre espace d'apprentissage")
        subtitle_label.setAlignment(Qt.AlignHCenter)
        subtitle_label.setStyleSheet(
            "font-size: 16px; color: #555555;"
        )

        header_layout.addWidget(title_label)
        header_layout.addWidget(subtitle_label)

        # Call-to-action buttons (centered)
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(16)
        buttons_layout.setAlignment(Qt.AlignHCenter)

        start_button = QPushButton("Commencer l'apprentissage")
        start_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        start_button.setStyleSheet(
            "padding: 10px 24px;"
            "font-size: 14px;"
            "font-weight: 600;"
        )
        start_button.clicked.connect(self._on_start_clicked)

        continue_button = QPushButton("Continuer")
        continue_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        continue_button.setStyleSheet(
            "padding: 8px 18px; font-size: 13px;"
        )
        continue_button.clicked.connect(self._on_continue_clicked)

        buttons_layout.addWidget(start_button)
        buttons_layout.addWidget(continue_button)

        # Module preview section
        modules_section_layout = QVBoxLayout()
        modules_section_layout.setSpacing(12)

        section_title = QLabel("Aperçu des modules")
        section_title.setStyleSheet("font-size: 18px; font-weight: 600;")
        modules_section_layout.addWidget(section_title)

        # Individual module cards (vertical list)
        modules_list_layout = QVBoxLayout()
        modules_list_layout.setSpacing(10)

        # Module 1: Python Start – 0%
        module1_card = self._create_module_card(
            title="Module 1: Python Start",
            status_text="0%",
            locked=False,
        )
        modules_list_layout.addWidget(module1_card)

        # Module 2: Variables – Verrouillé
        module2_card = self._create_module_card(
            title="Module 2: Variables",
            status_text="Verrouillé",
            locked=True,
        )
        modules_list_layout.addWidget(module2_card)

        # Module 3: Strings – Verrouillé
        module3_card = self._create_module_card(
            title="Module 3: Strings",
            status_text="Verrouillé",
            locked=True,
        )
        modules_list_layout.addWidget(module3_card)

        modules_section_layout.addLayout(modules_list_layout)

        # Assemble main layout
        main_layout.addLayout(header_layout)
        main_layout.addLayout(buttons_layout)
        main_layout.addLayout(modules_section_layout)
        main_layout.addStretch()  # Push content towards the top with breathing space

        self.setLayout(main_layout)

    def _create_module_card(self, title: str, status_text: str, locked: bool) -> QFrame:
        """Create a simple horizontal module card with minimal styling.

        The card uses a QHBoxLayout:
        - Left: optional lock icon for locked modules.
        - Middle: module title.
        - Right: status label (e.g., percentage or "Verrouillé").
        """
        card = QFrame()
        card.setFrameShape(QFrame.StyledPanel)
        card.setStyleSheet(
            "background-color: #f5f5f5;"
            "border-radius: 8px;"
            "padding: 10px;"
        )

        layout = QHBoxLayout(card)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(12)

        # Optional lock icon
        if locked:
            lock_label = QLabel("🔒")
            lock_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(lock_label)
        else:
            # To keep alignment consistent, add an empty placeholder
            lock_label = QLabel("")
            layout.addWidget(lock_label)

        # Module title
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 14px; font-weight: 500;")
        layout.addWidget(title_label, stretch=1)

        # Status text (e.g. "0%" or "Verrouillé")
        status_label = QLabel(status_text)
        status_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        status_label.setStyleSheet("font-size: 13px; color: #777777;")
        layout.addWidget(status_label)

        return card

    # ------------------------------------------------------------------
    # Signal emitters
    # ------------------------------------------------------------------
    def _on_start_clicked(self) -> None:
        """Emit navigation signal when the user starts learning."""
        self.navigate_to_modules.emit()

    def _on_continue_clicked(self) -> None:
        """Emit navigation signal when the user wants to continue."""
        self.navigate_continue.emit()
