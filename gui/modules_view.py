# modules_view.py
# Modules screen view for PyLearn Desktop
# Presents a list of learning modules as styled cards.

from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
)


class ModulesView(QWidget):
    """Modules screen view with a list of module cards.

    Signals:
        navigate_to_lessons(int): emitted when the user opens a module,
                                  passing the module_id.
        navigate_back(): emitted when the user clicks the back button.
    """

    # Navigation signals
    navigate_to_lessons = Signal(int)
    navigate_back = Signal()

    def __init__(self) -> None:
        super().__init__()
        self._setup_ui()

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------
    def _setup_ui(self) -> None:
        """Configure the layout and widgets for the modules page."""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(24)

        # Top bar with back button
        top_layout = QHBoxLayout()
        back_button = QPushButton("← Retour")
        back_button.setObjectName("backButton")
        back_button.setCursor(Qt.PointingHandCursor)
        back_button.clicked.connect(self._on_back_clicked)
        top_layout.addWidget(back_button)
        top_layout.addStretch()

        main_layout.addLayout(top_layout)

        # Header section
        header_layout = QVBoxLayout()
        header_layout.setSpacing(8)

        title_label = QLabel("Modules d'apprentissage")
        title_label.setObjectName("titleLabel")
        title_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        subtitle_label = QLabel("Choisissez un module pour commencer")
        subtitle_label.setObjectName("subtitleLabel")
        subtitle_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        header_layout.addWidget(title_label)
        header_layout.addWidget(subtitle_label)

        # Vertical list of module cards
        modules_list_layout = QVBoxLayout()
        modules_list_layout.setSpacing(12)

        # Module 1: Python Start – 0% – Unlocked (with "Ouvrir" button)
        module1_card = self._create_module_card(
            module_id=1,
            title="Module 1: Python Start",
            status_text="0%",
            locked=False,
        )
        modules_list_layout.addWidget(module1_card)

        # Module 2: Variables – Verrouillé – Locked icon
        module2_card = self._create_module_card(
            module_id=2,
            title="Module 2: Variables",
            status_text="Verrouillé",
            locked=True,
        )
        modules_list_layout.addWidget(module2_card)

        # Module 3: Strings – Verrouillé – Locked icon
        module3_card = self._create_module_card(
            module_id=3,
            title="Module 3: Strings",
            status_text="Verrouillé",
            locked=True,
        )
        modules_list_layout.addWidget(module3_card)

        main_layout.addLayout(header_layout)
        main_layout.addLayout(modules_list_layout)
        main_layout.addStretch()

        self.setLayout(main_layout)

    def _create_module_card(
        self,
        module_id: int,
        title: str,
        status_text: str,
        locked: bool,
    ) -> QFrame:
        """Create a styled module card."""
        card = QFrame()
        card.setObjectName("moduleCard")
        card.setFrameShape(QFrame.StyledPanel)

        layout = QHBoxLayout(card)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(12)

        # Left: lock icon or empty placeholder
        if locked:
            lock_label = QLabel("🔒")
            lock_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(lock_label)
        else:
            lock_label = QLabel("")
            layout.addWidget(lock_label)

        # Middle: title and status stacked vertically
        text_container = QWidget()
        text_layout = QVBoxLayout(text_container)
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(2)

        title_label = QLabel(title)
        status_label = QLabel(status_text)

        text_layout.addWidget(title_label)
        text_layout.addWidget(status_label)

        layout.addWidget(text_container, stretch=1)

        # Right: "Ouvrir" button for unlocked modules only
        if not locked:
            open_button = QPushButton("Ouvrir")
            open_button.setObjectName("openButton")
            open_button.clicked.connect(
                lambda _checked=False, mid=module_id: self._on_open_module(mid)
            )
            layout.addWidget(open_button)

        return card

    # ------------------------------------------------------------------
    # Signal emitters
    # ------------------------------------------------------------------
    def _on_open_module(self, module_id: int) -> None:
        """Emit navigation signal with the selected module id."""
        self.navigate_to_lessons.emit(module_id)

    def _on_back_clicked(self) -> None:
        """Emit signal to navigate back to home."""
        self.navigate_back.emit()
