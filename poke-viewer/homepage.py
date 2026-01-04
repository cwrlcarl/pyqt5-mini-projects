from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import (
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QWidget
)
import os

BASE_DIR = os.path.dirname(__file__)
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')


class HomePage(QWidget):
    def __init__(self, on_search_callback):
        super().__init__()
        self.on_search = on_search_callback

        self.pokemon_logo = QLabel()
        self.welcome_label = QLabel("Welcome to", objectName="welcome")
        self.title_label = QLabel("Pokémon Viewer!", objectName="title")
        self.subtitle = QLabel("Search your favorite Pokémon to get started",
                               objectName="desc")
        self.search_input = QLineEdit()

        self.initUI()
        self.styleUI()

    
    def initUI(self):
        main_layout = QVBoxLayout()

        image_width = int(self.width() * 0.20)
        image_height = int(self.height() * 0.20)
        pokemon_logo = QPixmap(os.path.join(ASSETS_DIR, 'pokemon-logo.png'))
        self.pokemon_logo.setPixmap(
            pokemon_logo.scaled(
                image_width, image_height,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation))
        self.pokemon_logo.setAlignment(Qt.AlignHCenter)

        self.subtitle.setWordWrap(True)
        self.subtitle.setAlignment(Qt.AlignCenter)

        search_icon = QIcon(os.path.join(ASSETS_DIR, 'search-icon.png'))
        self.search_input.addAction(search_icon, QLineEdit.LeadingPosition)
        self.search_input.setPlaceholderText("Search Pokémon...")
        self.search_input.returnPressed.connect(self.handle_search)

        main_layout.addSpacing(-120)
        main_layout.addWidget(self.pokemon_logo)
        main_layout.addSpacing(80)
        main_layout.addWidget(self.welcome_label, alignment=Qt.AlignHCenter)
        main_layout.addSpacing(-15)
        main_layout.addWidget(self.title_label, alignment=Qt.AlignHCenter)
        main_layout.addWidget(self.subtitle, alignment=Qt.AlignHCenter)
        main_layout.addSpacing(15)
        main_layout.addWidget(self.search_input, alignment=Qt.AlignHCenter)
        main_layout.setAlignment(Qt.AlignCenter)
        
        self.setLayout(main_layout)


    def styleUI(self):
        self.setStyleSheet("""
            QLabel {
                background-color: transparent;      
            }

            QLabel#welcome {
                font-size: 20px;
                font-weight: Bold;
                color: #737475;
            }
            
            QLabel#title {
                font-size: 30px;
                font-weight: Bold;
            }
                        
            QLabel#desc {
                font-size: 13px;
                color: #575859;
            }
            
            QLineEdit {
                padding: 7px;
                padding-left: 12px;
                min-width: 220px;
                border: 1px solid #1e1f21;
                border-radius: 20px;
                background: qlineargradient(
                    x1: 0, y1: 0, 
                    x2: 1, y2: 1, 
                    stop: 0 #202224,
                    stop: 0.3 #1e1f21,
                    stop: 1 #151617
                );
            }
        """)


    def handle_search(self):
        pokemon_name = self.search_input.text().strip()
        if pokemon_name:
            self.on_search(pokemon_name)
            self.search_input.clear()