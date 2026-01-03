from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import (
    QFrame, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton,
    QTextEdit, QVBoxLayout, QWidget
)
from helpers import *
import os
import requests

BASE_URL = "https://pokeapi.co/api/v2"
BASE_DIR = os.path.dirname(__file__)
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')


class PokemonInfo(QWidget):
    def __init__(self, on_back_callback):
        super().__init__()
        self.on_back = on_back_callback
        
        self.back_btn = QPushButton()
        self.header = QLabel()
        self.search_input = QLineEdit()
        self.pokemon_img = QLabel()
        self.pokemon_name = QLabel(objectName="name")
        self.pokemon_id = QLabel(objectName="id")
        self.pokemon_type = QLabel()
        self.pokemon_type2 = QLabel()
        self.pokemon_description = QTextEdit()
        self.pokemon_weight = QLabel()
        self.pokemon_height = QLabel()
        self.hp_stat = QLabel()
        self.attack_stat = QLabel()
        self.defense_stat = QLabel()

        self.initUI()
        self.styleUI()

    
    def initUI(self):
        main_layout = QVBoxLayout()

        back_button = QIcon(os.path.join(ASSETS_DIR, 'left-arrow-icon.png'))
        self.back_btn.setIcon(back_button)
        self.back_btn.setIconSize(QSize(15, 15))
        self.back_btn.setCursor(Qt.PointingHandCursor)
        self.back_btn.clicked.connect(self.on_back)

        search_icon = QIcon(os.path.join(ASSETS_DIR, 'search-icon.png'))
        self.search_input.addAction(search_icon, QLineEdit.LeadingPosition)
        self.search_input.setPlaceholderText("Search Pokémon...")
        self.search_input.returnPressed.connect(self.handle_search)

        search_field = QHBoxLayout()
        search_field.addWidget(self.back_btn)
        search_field.addWidget(self.search_input)
        
        self.pokemon_img.setAlignment(Qt.AlignHCenter)
        
        name_and_id = QHBoxLayout()
        name_and_id.setContentsMargins(0, 0, 0, 0)
        name_and_id.addWidget(self.pokemon_name)
        name_and_id.addWidget(self.pokemon_id)
        name_and_id.setAlignment(Qt.AlignHCenter)

        pokemon_type = QHBoxLayout()
        pokemon_type.setContentsMargins(0, 0, 0, 0)
        pokemon_type.addWidget(self.pokemon_type, alignment=Qt.AlignHCenter)
        pokemon_type.addWidget(self.pokemon_type2, alignment=Qt.AlignHCenter)
        pokemon_type.setAlignment(Qt.AlignHCenter)

        self.pokemon_description.setReadOnly(True)
        self.pokemon_description.setFrameStyle(QFrame.NoFrame)
        self.pokemon_description.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.pokemon_description.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.pokemon_description.setFixedHeight(100)
        self.pokemon_description.setContentsMargins(0, 0, 0, 0)
        self.pokemon_description.document().setDocumentMargin(0)

        weight_and_height = QGridLayout()
        weight_and_height.setContentsMargins(0, 0, 0, 0)
        weight_and_height.setSpacing(35)
        weight_and_height.addWidget(self.pokemon_weight, 0, 0)
        weight_and_height.addWidget(self.pokemon_height, 0, 1)
        weight_and_height.setAlignment(Qt.AlignHCenter)

        pokemon_stats = QGridLayout()
        pokemon_stats.setContentsMargins(0, 0, 0, 0)
        pokemon_stats.setSpacing(35)
        pokemon_stats.addWidget(self.hp_stat, 0, 0)
        pokemon_stats.addWidget(self.attack_stat, 0, 1)
        pokemon_stats.addWidget(self.defense_stat, 0, 2)
        pokemon_stats.setAlignment(Qt.AlignHCenter)

        container = QWidget(objectName="card")
        card = QVBoxLayout()

        card.addWidget(self.pokemon_img)
        card.addLayout(name_and_id)
        card.addSpacing(-10)
        card.addLayout(pokemon_type)
        card.addWidget(self.pokemon_description)
        card.addLayout(weight_and_height)
        card.addLayout(pokemon_stats)

        card.setContentsMargins(20, 20, 20, 10)
        card.setSpacing(10)
        container.setLayout(card)
        container.setFixedSize(340, 470)

        main_layout.addLayout(search_field)
        main_layout.addWidget(container, alignment=Qt.AlignHCenter)
        main_layout.setContentsMargins(30, 30, 30, 30)

        self.setLayout(main_layout)
        

    def styleUI(self):
        self.setStyleSheet("""
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
                           
            QPushButton {
                padding: 14px;
                border: None;
                border-radius: 12px;
                background-color: transparent;
            }
                           
            QPushButton::hover {
                background-color: #1e1f21;
            }

            QLabel {
                background-color: transparent;              
            } 

            QLabel#name {
                font-size:25px;
                font-weight: Bold;
            }

            QLabel#id {
                font-size: 15px;
                font-weight: Bold;
                color: #575859;
            }

            QTextEdit {
                padding-top: 7px;
                font-size: 13px;
                color: #575859;
                background-color: transparent;
            }

            QLineEdit {
                padding: 7px;
                padding-left: 12px;
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


    def handle_search(self):
        pokemon_name = self.search_input.text().lower().strip()
        if pokemon_name:
            success = self.display_pokemon(pokemon_name)
            if not success:
                print(f"Pokemon {pokemon_name} not found!")


    def display_pokemon(self, pokemon_name):
        pokemon_name = pokemon_name.lower().strip()
        if not pokemon_name:
            return False
        
        pokemon_data = self.load_pokemon(pokemon_name)
        if pokemon_data:
            types = pokemon_data['type']

            self.pokemon_type.setText(types[0])
            set_type_style(self.pokemon_type, types[0])

            if len(types) == 2:
                self.pokemon_type2.setText(pokemon_data['type'][1])
                set_type_style(self.pokemon_type2, types[1])
                self.pokemon_type2.show()
            else:
                self.pokemon_type2.hide()

            weight = convert_weight(pokemon_data['weight'])
            height = convert_height(pokemon_data['height'])

            self.pokemon_name.setText(pokemon_data['name'])
            self.pokemon_id.setText(f"#{pokemon_data['id']:04d}")
            self.pokemon_description.setText(pokemon_data['description'])
            self.pokemon_weight.setText(f"Weight: {weight}")
            self.pokemon_height.setText(f"Height: {height}")
            self.hp_stat.setText(f"HP: {pokemon_data['hp']}")
            self.attack_stat.setText(f"ATK: {pokemon_data['attack']}")
            self.defense_stat.setText(f"DEF: {pokemon_data['defense']}")
            self.load_pokemon_image(pokemon_data['image'])

            self.search_input.clear()
            return True
        else:
            return False


    def load_pokemon(self, pokemon_name):
        try:
            response = requests.get(f"{BASE_URL}/pokemon/{pokemon_name}")
            if response.status_code == 200:
                data = response.json()
                description = self.load_pokemon_description(pokemon_name)
                return {
                    'name': data['name'].capitalize(),
                    'id': data['id'],
                    'type': [t['type']['name'] for t in data['types']],
                    'description': description,
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
        

    def load_pokemon_description(self, pokemon_name):
        try:
            response = requests.get(f"{BASE_URL}/pokemon-species/{pokemon_name}")
            if response.status_code == 200:
                data = response.json()
                for entry in data['flavor_text_entries']:
                    if entry['language']['name'] == 'en':
                        description = entry['flavor_text']
                        description = description.replace('\n', ' ').replace('\f', ' ')
                        return description
            else:
                print(f"HTTP Error: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error fetching description: {e}")
            return None
        

    def load_pokemon_image(self, image):
        try:
            response = requests.get(image)
            image_data = response.content

            pixmap = QPixmap()
            pixmap.loadFromData(image_data)

            self.pokemon_img.setPixmap(
                pixmap.scaled(180, 180, Qt.KeepAspectRatio,
                              Qt.SmoothTransformation)
            )
        except Exception as e:
            print(f"Error fetching image: {e}")
            return None