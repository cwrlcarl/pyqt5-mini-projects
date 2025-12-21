import os
import sys
import requests

from pokemon_type import TYPE_COLORS
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
ASSET_DIR = os.path.join(BASE_DIR, 'asset')


class PokemonViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(500, 600)
        
        self.header = QLabel()
        self.input_pokemon = QLineEdit()
        self.pokemon_img = QLabel()
        self.pokemon_name = QLabel(objectName="name")
        self.pokemon_id = QLabel(objectName="id")
        self.pokemon_type = QLabel(objectName="type")
        self.pokemon_type2 = QLabel(objectName="type")
        self.pokemon_weight = QLabel()
        self.pokemon_height = QLabel()
        self.hp_stat = QLabel()
        self.attack_stat = QLabel()
        self.defense_stat = QLabel()

        self.initUI()
        self.styleUI()

    
    def initUI(self):
        image_width = int(self.width() * 0.25)
        image_height = int(self.height() * 0.25)
        pokedex_logo = QPixmap(os.path.join(ASSET_DIR, 'pokemon_logo.png'))
        self.header.setPixmap(
            pokedex_logo.scaled(
                image_width, image_height,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation))
        
        self.pokemon_id.setAlignment(Qt.AlignHCenter)
        self.pokemon_img.setAlignment(Qt.AlignHCenter)

        pokemon_info = QHBoxLayout()
        pokemon_info.addWidget(self.pokemon_name)
        pokemon_info.addWidget(self.pokemon_type)
        pokemon_info.addWidget(self.pokemon_type2)
        pokemon_info.setAlignment(Qt.AlignHCenter)

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

        search_field = QHBoxLayout()
        search_field.addWidget(self.header)
        search_field.addWidget(self.input_pokemon)

        widgets = [
            self.pokemon_id, self.pokemon_img, pokemon_info,
            weight_and_height, pokemon_stats
        ]

        horizontal_layouts = [
            pokemon_info, weight_and_height, pokemon_stats
        ]

        main_layout = QVBoxLayout()

        container = QWidget(objectName="card")
        card = QVBoxLayout()

        for widget in widgets: 
            if widget in horizontal_layouts:
                card.addLayout(widget)
            else:
                card.addWidget(widget)

        container.setLayout(card)
        container.setFixedSize(400, 440)

        main_layout.addLayout(search_field)
        main_layout.addSpacing(20)
        main_layout.addWidget(container, alignment=Qt.AlignHCenter)
        self.setLayout(main_layout)
        self.setContentsMargins(40, 15, 40, 15)


    def styleUI(self):
        self.setStyleSheet("""
            QWidget { 
                margin: 2px 3px;
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
                           
            QWidget#card {  
                border: 1px solid #2f3033;
                border-radius: 12px;
                background: qlineargradient(
                    x1: 0, y1: 0, 
                    x2: 1, y2: 1, 
                    stop: 0 #191b1c,
                    stop: 0.5 #1c1d1f,
                    stop: 1 #151617
                );
            }

            QLabel {
                background-color: transparent;              
            }     
                           
            QLabel#name { font-size:25px; font-weight: Bold; }
            QLabel#id { font-family: MADE Outer Sans; font-size: 70px; color: #9d9fa1; }
                           
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
                return {
                    'name': data['name'].capitalize(),
                    'id': data['id'],
                    'type': [t['type']['name'] for t in data['types']],
                    'weight': data['weight'],
                    'height': data['height'],
                    'hp': data['stats'][0]['base_stat'],
                    'attack': data['stats'][1]['base_stat'],
                    'defense': data['stats'][2]['base_stat'],
                    'image': data['sprites']['other']['official-artwork']['front_default']
                }
            else:
                print(f"HTTP Error: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None
        

    def load_pokemon_image(self, image):
        try:
            response = requests.get(image)
            image_data = response.content

            pixmap = QPixmap()
            pixmap.loadFromData(image_data)

            self.pokemon_img.setPixmap(
                pixmap.scaled(200, 200, Qt.KeepAspectRatio,
                              Qt.SmoothTransformation)
            )
        except Exception as e:
            print(f"Error fetching image: {e}")
            return None


    def display_pokemon(self):
        input_name = self.input_pokemon.text().lower().strip()
        if not input_name:
            self.input_pokemon.clear()
            return None
        
        pokemon_data = self.load_pokemon(input_name)
        if pokemon_data:
            self.pokemon_name.setText(pokemon_data['name'])
            self.pokemon_id.setText(f"#{pokemon_data['id']:04d}")
            if len(pokemon_data['type']) == 2:
                self.pokemon_type.setText(pokemon_data['type'][0])
                self.pokemon_type2.setText(pokemon_data['type'][1])
            else:
                self.pokemon_type.setText(pokemon_data['type'][0])
                self.pokemon_type2.clear()
            self.pokemon_weight.setText(f"Weight: {pokemon_data['weight']}")
            self.pokemon_height.setText(f"Height: {pokemon_data['height']}")
            self.hp_stat.setText(f"HP: {pokemon_data['hp']}")
            self.attack_stat.setText(f"Attack: {pokemon_data['attack']}")
            self.defense_stat.setText(f"Defense: {pokemon_data['defense']}")
            self.load_pokemon_image(pokemon_data['image'])


    def handle_errors(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    poke = PokemonViewer()
    poke.show()
    sys.exit(app.exec_())