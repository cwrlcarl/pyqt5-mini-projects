import sys
import random
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.Qt import Qt
from PyQt5.QtCore import QSize

class RockPaperScissors(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setFixedSize(400, 450)
        
        self.result = QLabel("You Win!")
        self.player = QLabel("P")
        self.versus = QLabel("vs")
        self.computer = QLabel("C")
        
        self.rock = QPushButton()
        self.paper = QPushButton()
        self.scissors = QPushButton()
        self.reset = QPushButton("Reset")

        self.designUI()
        self.initUI()
    

    def designUI(self):
        self.setStyleSheet("""
            QLabel, QPushButton {
                font-family: MADE Outer Sans;
            }

            QLabel {
                font-size: 30px;
                padding: 5px;
            }
                           
            QPushButton {
                padding: 8px 15px;
                font-size: 15px;
            }
        """)


    def initUI(self):
        pvc_layout = QHBoxLayout()
        pvc_layout.addWidget(self.player)
        pvc_layout.addWidget(self.versus)
        pvc_layout.addWidget(self.computer)
        pvc_layout.setAlignment(Qt.AlignHCenter)
        
        icons = {
            self.rock: "rps-game/assets/rock.png",
            self.paper: "rps-game/assets/paper.png",
            self.scissors: "rps-game/assets/scissors.png"
        }

        for btn, path in icons.items():
            btn.setIcon(QIcon(path))
            btn.setIconSize(QSize(80, 80))
            btn.setFixedSize(100, 100)

        options = QHBoxLayout()
        options.addWidget(self.rock)
        options.addWidget(self.paper)
        options.addWidget(self.scissors)

        game_layout = QVBoxLayout()
        game_layout.addWidget(self.result, alignment=Qt.AlignHCenter)
        game_layout.addLayout(pvc_layout)
        game_layout.addLayout(options)
        game_layout.addWidget(self.reset)
        game_layout.setContentsMargins(25, 25, 25, 25)

        self.setLayout(game_layout)


    def play_game():
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = RockPaperScissors()
    game.show()
    sys.exit(app.exec_())