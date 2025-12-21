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
        self.setFixedSize(700, 550)
        
        self.header = QLabel()
        self.input_pokemon = QLineEdit()
        self.pokemon_img = QLabel()
        self.pokemon_name = QLabel(objectName="name")
        self.pokemon_id = QLabel(objectName="id")
        self.pokemon_type = QLabel()
        self.pokemon_weight = QLabel()
        self.pokemon_height = QLabel()
        self.hp_stat = QLabel()
        self.attack_stat = QLabel()
        self.defense_stat = QLabel()

        self.initUI()
        self.styleUI()

    
    def initUI(self):
        image_width = int(self.width() * 0.2)
        image_height = int(self.height() * 0.2)
        pokedex_logo = QPixmap(os.path.join(ASSETS_DIR, 'pokemon_logo.png'))
        self.header.setPixmap(pokedex_logo.scaled(image_width, image_height, Qt.KeepAspectRatio,
                                                  Qt.SmoothTransformation))
        
        self.header.setAlignment(Qt.AlignHCenter)
        self.pokemon_img.setAlignment(Qt.AlignHCenter)
        self.pokemon_type.setAlignment(Qt.AlignHCenter)

        name_and_id = QHBoxLayout()
        name_and_id.addWidget(self.pokemon_name)
        name_and_id.addWidget(self.pokemon_id)
        name_and_id.setAlignment(Qt.AlignHCenter)

        weight_and_height = QHBoxLayout()
        weight_and_height.addWidget(self.pokemon_weight)
        weight_and_height.addWidget(self.pokemon_height)
        weight_and_height.setAlignment(Qt.AlignHCenter)

        pokemon_stats = QHBoxLayout()
        pokemon_stats.addWidget(self.hp_stat)
        pokemon_stats.addWidget(self.attack_stat)
        pokemon_stats.addWidget(self.defense_stat)
        pokemon_stats.setAlignment(Qt.AlignHCenter)

        self.input_pokemon.setPlaceholderText("Search pokemon..")
        self.input_pokemon.returnPressed.connect(self.display_pokemon)
        self.search_btn.clicked.connect(self.display_pokemon)
        self.search_btn.setCursor(Qt.PointingHandCursor)

        search_field = QHBoxLayout()
        search_field.addWidget(self.header)
        search_field.addWidget(self.input_pokemon)

        widgets = [
            search_field, self.pokemon_img,
            name_and_id, self.pokemon_type,
            weight_and_height, pokemon_stats
        ]

        horizontal_layouts = [
            search_field, name_and_id, weight_and_height, pokemon_stats
        ]

        main_layout = QVBoxLayout()
        for widget in widgets: 
            if widget in horizontal_layouts:
                main_layout.addLayout(widget)
            else:
                main_layout.addWidget(widget)
        self.setLayout(main_layout)
        self.setContentsMargins(20, 15, 20, 15)


    def styleUI(self):
        self.setStyleSheet("""
            QWidget { 
                margin: 2px 10px;
                font-family: Poppins;
                font-size: 15px;
                color: white;
                background: qlineargradient(
                    x1: 0, y1: 0, 
                    x2: 1, y2: 1, 
                    stop: 0 #202224,
                    stop: 0.3 #101114,
                    stop: 1 #151617
                );
            }

            QLabel {
                background-color: transparent;              
            }     
                           
            QLabel#name { font-size:25px; font-weight: Bold; }
            QLabel#id { color: #bbbdbf; }
                           
            QLineEdit {
                padding: 7px;
                border: 1px solid #1e1f21;
                border-radius: 10px;
                background: qlineargradient(
                    x1: 0, y1: 0, 
                    x2: 1, y2: 1, 
                    stop: 0 #202224,
                    stop: 0.3 #1e1f21,
                    stop: 1 #151617
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
        except requests.exceptions.RequestException as e:
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

            pokemon_name = pokemon_data['name'].capitalize()
            pokemon_id = pokemon_data['id']
            pokemon_type = pokemon_data['types'][0]['type']['name']
            pokemon_weight = pokemon_data['weight']
            pokemon_height = pokemon_data['height']
            hp = pokemon_data['stats'][0]['base_stat']
            attack = pokemon_data['stats'][1]['base_stat']
            defense = pokemon_data['stats'][2]['base_stat']

            self.pokemon_name.setText(pokemon_name)
            self.pokemon_id.setText(f"#00{pokemon_id}")
            self.pokemon_type.setText(pokemon_type)
            self.pokemon_weight.setText(f"Weight: {pokemon_weight}")
            self.pokemon_height.setText(f"Height: {pokemon_height}")
            self.hp_stat.setText(f"HP: {hp}")
            self.attack_stat.setText(f"Attack: {attack}")
            self.defense_stat.setText(f"Defense: {defense}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    poke = PokemonViewer()
    poke.show()
    sys.exit(app.exec_())