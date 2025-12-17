import os
import sys

from PyQt5.QtCore import Qt
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

        self.header = QLabel("PokeDex")
        self.input_pokemon = QLineEdit()
        self.search_btn = QPushButton("Search")

        self.initUI()

    
    def initUI(self):
        self.input_pokemon.setPlaceholderText("Search pokemon..")

        search_field = QHBoxLayout()
        search_field.addWidget(self.input_pokemon)
        search_field.addWidget(self.search_btn)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.header)
        main_layout.addLayout(search_field)

        self.setLayout(main_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    poke = PokemonViewer()
    poke.show()
    sys.exit(app.exec_())