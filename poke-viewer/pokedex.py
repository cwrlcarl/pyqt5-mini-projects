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
    QStackedLayout,
    QVBoxLayout,
    QWidget
)

BASE_URL = "https://pokeapi.co/api/v2"
BASE_DIR = os.path.dirname(__file__)
ASSET_DIR = os.path.join(BASE_DIR, 'asset')


class PokemonViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pokemon Viewer")
        self.setFixedSize(500, 600)
        
        self.header = QLabel()
        self.input_pokemon = QLineEdit()
        self.pokemon_img = QLabel()
        self.pokemon_name = QLabel(objectName="name")
        self.pokemon_id = QLabel(objectName="id")
        self.pokemon_type = QLabel()
        self.pokemon_type2 = QLabel()
        self.pokemon_description = QLabel(objectName="desc")
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

        search_field = QHBoxLayout()
        search_field.addWidget(self.header)
        search_field.addWidget(self.input_pokemon)

        self.input_pokemon.setPlaceholderText("Search pokemon..")
        self.input_pokemon.returnPressed.connect(self.display_pokemon)
        
        overlay_widget = QWidget(objectName="stack")
        overlay_layout = QStackedLayout(overlay_widget)
        overlay_layout.setStackingMode(QStackedLayout.StackAll)
        self.pokemon_id.setAlignment(Qt.AlignHCenter)
        self.pokemon_img.setAlignment(Qt.AlignHCenter)
        overlay_layout.addWidget(self.pokemon_img)
        overlay_layout.addWidget(self.pokemon_id)
        overlay_widget.setFixedHeight(200)

        pokemon_info = QHBoxLayout()
        pokemon_info.addWidget(self.pokemon_name)
        pokemon_info.addWidget(self.pokemon_type, alignment=Qt.AlignHCenter)
        pokemon_info.addWidget(self.pokemon_type2, alignment=Qt.AlignHCenter)

        self.pokemon_description.setWordWrap(True)

        weight_and_height = QHBoxLayout()
        weight_and_height.addWidget(self.pokemon_weight)
        weight_and_height.addWidget(self.pokemon_height)

        pokemon_stats = QHBoxLayout()
        pokemon_stats.addWidget(self.hp_stat)
        pokemon_stats.addWidget(self.attack_stat)
        pokemon_stats.addWidget(self.defense_stat)

        layouts = [
            overlay_widget, pokemon_info,
            self.pokemon_description,
            weight_and_height, pokemon_stats
        ]

        horizontal_layouts = [
            pokemon_info, weight_and_height, pokemon_stats
        ]

        main_layout = QVBoxLayout()

        container = QWidget(objectName="card")
        card = QVBoxLayout()

        for layout in layouts: 
            if layout in horizontal_layouts:
                card.addLayout(layout)
            else:
                card.addWidget(layout)

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
                           
            QWidget#stack {
                background-color: transparent;
            }

            QLabel {
                background-color: transparent;              
            } 
                               
            QLabel#id {
                font-family: MADE Outer Sans;
                font-size: 85px;
                color: #575859;
            }  
                                     
            QLabel#name {
                font-size:25px;
                font-weight: Bold;
            }
                           
            QLabel#desc {
                font-size: 13px;
                color: #575859;
            }
                           
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


    def set_type_style(self, label, type_name):
        color = TYPE_COLORS.get(type_name, '#9d9fa1')
        bg_color = self.hex_to_rgba(color, 0.20)
        label.setStyleSheet(f"""
            QLabel {{
                max-height: 20px;
                padding: 1px 8px;
                font-size: 13px;
                border-radius: 10px;
                border: 1px solid {color};
                background-color: {bg_color};
                color: {color};
            }}
        """)


    def hex_to_rgba(self, hex_color, alpha):
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return f'rgba({r}, {g}, {b}, {alpha})'


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
            weight = self.convert_weight(pokemon_data['weight'])
            height = self.convert_height(pokemon_data['height'])

            types = pokemon_data['type']
            self.pokemon_type.setText(types[0])
            self.set_type_style(self.pokemon_type, types[0])

            if len(types) == 2:
                self.pokemon_type2.setText(pokemon_data['type'][1])
                self.set_type_style(self.pokemon_type2, types[1])
                self.pokemon_type2.show()
            else:
                self.pokemon_type2.hide()

            self.pokemon_name.setText(pokemon_data['name'])
            self.pokemon_id.setText(f"#{pokemon_data['id']:04d}")
            self.pokemon_description.setText(pokemon_data['description'])
            self.pokemon_weight.setText(f"Weight: {weight}")
            self.pokemon_height.setText(f"Height: {height}")
            self.hp_stat.setText(f"HP: {pokemon_data['hp']}")
            self.attack_stat.setText(f"Attack: {pokemon_data['attack']}")
            self.defense_stat.setText(f"Defense: {pokemon_data['defense']}")
            self.load_pokemon_image(pokemon_data['image'])


    def convert_weight(self, hectogram):
        kilogram = hectogram / 10
        pound = kilogram * 2.20462
        return f"{pound:.1f} lbs"


    def convert_height(self, decimeter):
        meter = decimeter / 10
        feet = meter * 3.28084
        inch = (feet - int(feet)) * 12
        return f"{feet:.0f}'{inch:.0f}\""


    def handle_errors(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    poke = PokemonViewer()
    poke.show()
    sys.exit(app.exec_())