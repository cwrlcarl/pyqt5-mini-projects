import os
import sys
import requests

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

BASE_URL = "https://pokeapi.co/api/v2"
BASE_DIR = os.path.dirname(__file__)
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')


class PokemonViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(550, 500)
        
        self.header = QLabel()
        self.input_pokemon = QLineEdit()
        self.search_btn = QPushButton("Search")
        self.pokemon_img = QLabel()
        self.pokemon_name = QLabel("Name")

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

        widgets = [
            self.header, search_field,
            self.pokemon_img, self.pokemon_name
        ]

        main_layout = QVBoxLayout()
        for widget in widgets:
            if widget is search_field:
                main_layout.addLayout(widget)
            else:
                main_layout.addWidget(widget)
        self.setLayout(main_layout)
        self.setContentsMargins(15, 15, 15, 15)


    def styleUI(self):
        self.setStyleSheet("""
            QWidget {
                font-family: Poppins;
                font-size: 15px;z
                background-color: white;
            }
                           
            QLabel {
                
            }
                           
            QLineEdit {
                padding: 10px;
                border: 1px solid #f2f2f2;
                border-radius: 10px;
                background-color: #f5f6f7;
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


    def get_pokemon(self, pokemon_name):
        try:
            response = requests.get(f"{BASE_URL}/pokemon/{pokemon_name}")

            if response.status_code == 200:
                data = response.json()
                return data
            else:
                print(f"HTTP Error: {response.status_code}")
                return
        except requests.exception.RequestException as e:
            print(f"Error fetching data: {e}")
            return


    def show_pokemon(self):
        data = self.get_pokemon(pokemon_name)

        pokemon_name = self.input_pokemon.text().lower().strip()
        if not pokemon_name:
            self.input_pokemon.clear()
            return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    poke = PokemonViewer()
    poke.show()
    sys.exit(app.exec_())