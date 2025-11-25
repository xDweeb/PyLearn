# modules_view.py
# View for displaying modules in PyLearn Desktop

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QFrame, QGridLayout
)
from PySide6.QtCore import Signal, Qt
from controllers.module_controller import ModuleController


class ModulesView(QWidget):
    """View for displaying all modules."""

    # Navigation signals
    navigate_back = Signal()
    navigate_to_lessons = Signal(int)  # Emits module_id

    def __init__(self, parent=None):
        super().__init__(parent)
        self.controller = ModuleController()
        self.modules = []
        self._setup_ui()

    def _setup_ui(self):
        """Set up the user interface."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

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
        title = QLabel("Modules de formation")
        title.setObjectName("viewTitle")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        subtitle = QLabel("Choisissez un module pour commencer votre apprentissage")
        subtitle.setObjectName("viewSubtitle")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)

        # Scrollable area for modules
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        scroll_content = QWidget()
        self.grid_layout = QGridLayout(scroll_content)
        self.grid_layout.setSpacing(20)
        self.grid_layout.setContentsMargins(10, 10, 10, 10)

        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

    def load_modules(self):
        """Load modules from database and refresh the view."""
        # Clear existing cards
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Load modules from controller
        self.modules = self.controller.load_modules()

        # Create module cards
        for idx, module in enumerate(self.modules):
            card = self._create_module_card(module)
            row = idx // 3
            col = idx % 3
            self.grid_layout.addWidget(card, row, col)

        # Add stretch at the end
        self.grid_layout.setRowStretch(len(self.modules) // 3 + 1, 1)

    def _create_module_card(self, module: dict) -> QFrame:
        """Create a card widget for a module."""
        card = QFrame()
        card.setObjectName("moduleCard")
        card.setFixedSize(280, 200)
        
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(10)

        # Lock icon or module number
        if module["is_unlocked"]:
            icon_text = f"📘"
        else:
            icon_text = "🔒"
        
        icon_label = QLabel(icon_text)
        icon_label.setStyleSheet("font-size: 32px;")
        icon_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(icon_label)

        # Module name
        name_label = QLabel(module["name"])
        name_label.setObjectName("cardTitle")
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setWordWrap(True)
        card_layout.addWidget(name_label)

        # Module description
        desc_label = QLabel(module["description"])
        desc_label.setObjectName("cardDescription")
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setWordWrap(True)
        card_layout.addWidget(desc_label)

        card_layout.addStretch()

        # Button
        if module["is_unlocked"]:
            btn = QPushButton("Commencer")
            btn.setObjectName("primaryButton")
            btn.clicked.connect(lambda checked, m_id=module["id"]: self.navigate_to_lessons.emit(m_id))
        else:
            btn = QPushButton("Verrouillé")
            btn.setObjectName("secondaryButton")
            btn.setEnabled(False)
        
        card_layout.addWidget(btn)

        return card
