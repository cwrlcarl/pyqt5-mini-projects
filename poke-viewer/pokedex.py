import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget
)

BASE_DIR = os.path.dirname(__file__)
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')


class PokemonViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(550, 500)

        self.header = QLabel()
        self.input_pokemon = QLineEdit()
        self.search_btn = QPushButton("Search")

        self.initUI()
        self.styleUI()

    
    def initUI(self):
        pokedex_logo = QPixmap(os.path.join(ASSETS_DIR, 'pokedex_logo.png'))
        self.header.setPixmap(pokedex_logo.scaled(193, 70, Qt.KeepAspectRatio,
                                                  Qt.SmoothTransformation))
        self.header.setAlignment(Qt.AlignHCenter)

        self.input_pokemon.setPlaceholderText("Search pokemon..")
        self.input_pokemon.returnPressed.connect(self.show_pokemon)
        self.search_btn.clicked.connect(self.show_pokemon)
        self.search_btn.setCursor(Qt.PointingHandCursor)

        search_field = QHBoxLayout()
        search_field.addWidget(self.input_pokemon)
        search_field.addWidget(self.search_btn)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.header)
        main_layout.addLayout(search_field)
        self.setLayout(main_layout)


    def styleUI(self):
        self.setStyleSheet("""
            QWidget {
                font-family: Poppins;
            }
                           
            QLabel {
                
            }
                           
            QLineEdit {
                border-radius: 10px;
                padding: 10px;
            }
                           
            QPushButton {
                border-radius: 10px;
                padding: 10px;
                min-width: 150px;
                color: #f5f6f7;
                border: 1px solid #63aeff;
                background: qlineargradient(
                    x1: 0, y1: 0, 
                    x2: 1, y2: 1, 
                    stop: 0.2 #63aeff,
                    stop: 0.4 #8ac7ed,
                    stop: 0.9 #0e4cc9
                );
            }
        """)


    def show_pokemon(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    poke = PokemonViewer()
    poke.show()
    sys.exit(app.exec_())