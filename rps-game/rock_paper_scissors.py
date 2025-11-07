import sys
import random
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.Qt import Qt

class RockPaperScissors(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Rock Paper Scissors")
        self.setFixedSize(450, 400)
        self.result = QLabel("You Win!")
        self.player = QLabel("Player")
        self.versus = QLabel("vs")
        self.computer = QLabel("Computer")
        
        self.rock = QPushButton("Rock")
        self.paper = QPushButton("Paper")
        self.scissors = QPushButton("Scissors")
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
        icons = {
            "rock": "assets/rock.png",
            "paper": "assets/paper.png",
            "scissors": "assets/scissors.png"
        }

        pvc_layout = QHBoxLayout()
        pvc_layout.addWidget(self.player)
        pvc_layout.addWidget(self.versus)
        pvc_layout.addWidget(self.computer)
        pvc_layout.setAlignment(Qt.AlignHCenter)

        options = QHBoxLayout()
        options.addWidget(self.rock)
        options.addWidget(self.paper)
        options.addWidget(self.scissors)

        game_layout = QVBoxLayout()
        game_layout.addWidget(self.result, alignment=Qt.AlignHCenter)
        game_layout.addLayout(pvc_layout)
        game_layout.addLayout(options)
        game_layout.addWidget(self.reset)

        self.setLayout(game_layout)


    def play_game():
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = RockPaperScissors()
    game.show()
    sys.exit(app.exec_())