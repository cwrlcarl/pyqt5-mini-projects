from PyQt5.QtWidgets import (
    QApplication,
    QStackedWidget,
    QVBoxLayout,
    QWidget
)
from homepage import HomePage
from pokemon_info import PokemonInfo
import sys


class PokemonViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pokemon Viewer")
        self.setFixedSize(500, 620)

        self.stacked_widget = QStackedWidget()

        self.homepage = HomePage(on_search_callback=self.view_pokemon)
        self.pokemon_info = PokemonInfo(on_back_callback=self.go_to_homepage)

        self.stacked_widget.addWidget(self.homepage)
        self.stacked_widget.addWidget(self.pokemon_info)

        self.initUI()
        self.styleUI()

    
    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stacked_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)


    def styleUI(self):
        self.setStyleSheet("""
            QWidget {
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
        """)


    def view_pokemon(self, pokemon_name):
        success = self.pokemon_info.display_pokemon(pokemon_name.lower())
        if success:
            self.stacked_widget.setCurrentIndex(1)
        else:   
            print(f"Pokemon {pokemon_name} not found!")


    def go_to_homepage(self):
        self.stacked_widget.setCurrentIndex(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = PokemonViewer()
    viewer.show()
    sys.exit(app.exec_())