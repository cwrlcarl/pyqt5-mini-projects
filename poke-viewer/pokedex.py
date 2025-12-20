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
        self.setFixedSize(450, 530)
        
        self.header = QLabel()
        self.input_pokemon = QLineEdit()
        self.search_btn = QPushButton("Search")
        self.pokemon_img = QLabel()
        self.pokemon_name = QLabel(objectName="name")
        self.pokemon_type = QLabel()
        self.pokemon_weight = QLabel()
        self.pokemon_height = QLabel()
        self.hp_stat = QLabel()
        self.attack_stat = QLabel()
        self.defense_stat = QLabel()

        self.initUI()
        self.styleUI()

    
    def initUI(self):
        pokedex_logo = QPixmap(os.path.join(ASSETS_DIR, 'pokedex_logo.png'))
        self.header.setPixmap(pokedex_logo.scaled(193, 70, Qt.KeepAspectRatio,
                                                  Qt.SmoothTransformation))
        self.header.setAlignment(Qt.AlignHCenter)
        self.pokemon_img.setAlignment(Qt.AlignHCenter)

        weight_and_height = QHBoxLayout()
        weight_and_height.addWidget(self.pokemon_weight)
        weight_and_height.addWidget(self.pokemon_height)

        pokemon_stats = QHBoxLayout()
        pokemon_stats.addWidget(self.hp_stat)
        pokemon_stats.addWidget(self.attack_stat)
        pokemon_stats.addWidget(self.defense_stat)

        self.input_pokemon.setPlaceholderText("Search pokemon..")
        self.input_pokemon.returnPressed.connect(self.display_pokemon)
        self.search_btn.clicked.connect(self.display_pokemon)
        self.search_btn.setCursor(Qt.PointingHandCursor)

        search_field = QHBoxLayout()
        search_field.addWidget(self.input_pokemon)
        search_field.addWidget(self.search_btn)

        widgets = [
            self.header, search_field, self.pokemon_img,
            self.pokemon_name, self.pokemon_type,
            weight_and_height, pokemon_stats
        ]

        horizontal_layouts = [
            search_field, weight_and_height, pokemon_stats
        ]

        main_layout = QVBoxLayout()
        for widget in widgets:
            if widget in horizontal_layouts:
                main_layout.addLayout(widget)
            else:
                main_layout.addWidget(widget)
        self.setLayout(main_layout)
        self.setContentsMargins(15, 15, 15, 15)


    def styleUI(self):
        self.setStyleSheet("""
            QWidget { 
                font-family: Poppins;
                font-size: 15px;
                background-color: white;
            }
                           
            QLabel#name {

            }
                           
            QLineEdit {
                padding: 7px;
                border: 1px solid #f2f2f2;
                border-radius: 10px;
                background-color: #f5f6f7;
            }
                           
            QPushButton {
                border-radius: 10px;
                padding: 10px;
                min-width: 130px;
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


    def load_pokemon(self, pokemon_name):
        try:
            response = requests.get(f"{BASE_URL}/pokemon/{pokemon_name}")
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                print(f"HTTP Error: {response.status_code}")
                return None
        except requests.exception.RequestException as e:
            print(f"Error fetching data: {e}")
            return None
        

    def load_pokemon_image(self, pokemon_image):
        try:
            response = requests.get(pokemon_image)
            if response.status_code == 200:
                content = response.content
                return content
            else:
                print(f"Image HTTP Error: {response.status_code}")
                return None
        except requests.exception.RequestException as e:
            print(f"Error fetching image: {e}")
            return None


    def display_pokemon(self):
        pokemon_name = self.input_pokemon.text().lower().strip()
        if not pokemon_name or not pokemon_name.isalpha():
            self.input_pokemon.clear()
            return None
        
        pokemon_data = self.load_pokemon(pokemon_name)
        if pokemon_data:
            pokemon_image = pokemon_data['sprites']['other']['official-artwork']['front_default']
            pokemon_image_data = self.load_pokemon_image(pokemon_image)

            if pokemon_image_data:
                pixmap = QPixmap()
                pixmap.loadFromData(pokemon_image_data)
                self.pokemon_img.setPixmap(
                    pixmap.scaled(200, 200, Qt.KeepAspectRatio,
                                  Qt.SmoothTransformation)
                )

            name = pokemon_data['name'].capitalize()
            types = pokemon_data['types'][0]['type']['name']
            weight = pokemon_data['weight']
            height = pokemon_data['height']
            hp = pokemon_data['stats'][0]['base_stat']
            attack = pokemon_data['stats'][1]['base_stat']
            defense = pokemon_data['stats'][2]['base_stat']

            self.pokemon_name.setText(name)
            self.pokemon_type.setText(types)
            self.pokemon_weight.setText(f"Weight: {weight}")
            self.pokemon_height.setText(f"Height: {height}")
            self.hp_stat.setText(f"HP: {hp}")
            self.attack_stat.setText(f"Attack: {attack}")
            self.defense_stat.setText(f"Defense: {defense}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    poke = PokemonViewer()
    poke.show()
    sys.exit(app.exec_())