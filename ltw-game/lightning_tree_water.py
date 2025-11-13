import sys
import random
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QPushButton)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.Qt import Qt
from PyQt5.QtCore import QSize


class LightningTreeWater(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setFixedSize(400, 450)
        self.set_background("pyqt5-mini-projects/ltw-game/assets/pixel_bg.png")
        
        self.result = QLabel("LTW Game", objectName="title")
        self.description = QLabel("Welcome to my Game!", objectName="description")
        self.display_player_score = QLabel("You: 0")
        self.display_computer_score = QLabel("Computer: 0")

        self.player = QLabel()
        self.versus = QLabel("vs")
        self.computer = QLabel()
        
        self.lightning = QPushButton()
        self.tree = QPushButton()
        self.water = QPushButton()
        self.reset = QPushButton("Reset")

        self.player_score = 0
        self.computer_score = 0
        self.win_rules = {
            self.lightning: self.tree,
            self.tree: self.water,
            self.water:  self.lightning
        }

        self.designUI()
        self.initUI()
    

    def set_background(self, image_path):
        self.bg = QLabel(self)
        pixmap = QPixmap(image_path)
        scaled_pix = pixmap.scaled(
            self.size(),
            Qt.KeepAspectRatioByExpanding,
            Qt.SmoothTransformation
        )
        self.bg.setPixmap(scaled_pix)
        self.bg.setGeometry(0, 0, self.width(), self.height())
        self.bg.setAlignment(Qt.AlignCenter)
        self.bg.lower()


    def designUI(self):
        self.setStyleSheet("""
            QLabel, QPushButton {
                font-family: Ari-W9500 Condensed Display;
            }

            QLabel {
                font-size: 20px;
                padding: 5px;
            }
                           
            QLabel#title {
                font-size: 30px;
            }
                           
            QLabel#description {
                font-size: 15px;
            }
                           
            QPushButton {
                padding: 8px 15px;
                font-size: 15px;
            }
        """)


    def initUI(self):
        scoreboard = QHBoxLayout()
        scoreboard.addWidget(self.display_player_score)
        scoreboard.addWidget(self.display_computer_score)
        scoreboard.setAlignment(Qt.AlignHCenter)

        pvc_layout = QHBoxLayout()
        pvc_layout.addWidget(self.player)
        pvc_layout.addWidget(self.versus)
        pvc_layout.addWidget(self.computer)
        pvc_layout.setAlignment(Qt.AlignHCenter)
        
        self.icons = {
            "lightning": {
                "button": self.lightning,
                "path": "pyqt5-mini-projects/ltw-game/assets/lightning.png"
            },
            "tree": {
                "button": self.tree,
                "path": "pyqt5-mini-projects/ltw-game/assets/tree.png"
            },
            "water": {
                "button": self.water,
                "path": "pyqt5-mini-projects/ltw-game/assets/water.png"
            }
        }

        for choice, data in self.icons.items():
            btn = data["button"]
            path = data["path"]
            btn.setIcon(QIcon(path))
            btn.setIconSize(QSize(40, 40))
            btn.setFixedSize(80, 80)
            btn.clicked.connect(self.play_game)

        options = QHBoxLayout()
        options.addWidget(self.lightning)
        options.addWidget(self.tree)
        options.addWidget(self.water)

        game_layout = QVBoxLayout()
        game_layout.addWidget(self.result, alignment=Qt.AlignHCenter)
        game_layout.addWidget(self.description, alignment=Qt.AlignHCenter)
        game_layout.addLayout(pvc_layout)
        game_layout.addLayout(options)
        game_layout.addWidget(self.reset)
        game_layout.addLayout(scoreboard)
        game_layout.setContentsMargins(25, 25, 25, 25)

        self.reset.clicked.connect(self.reset_game)

        self.setLayout(game_layout)


    def play_game(self):
        player_choice = self.sender()
        computer_choice = random.choice([self.lightning, self.tree, self.water])

        for choice in self.icons:
            if self.icons[choice]["button"] == player_choice:
                self.update_icon(self.player, self.icons[choice]["path"])

            if self.icons[choice]["button"] == computer_choice:
                self.update_icon(self.computer, self.icons[choice]["path"])
        
        if self.win_rules[player_choice] == computer_choice:
            self.player_score += 1
            self.result.setText("You Win!")
            self.display_player_score.setText(f"You: {self.player_score}")
        elif self.win_rules[computer_choice] == player_choice:
            self.computer_score += 1
            self.result.setText("You Lose!")
            self.display_computer_score.setText(f"Computer: {self.computer_score}")
        else:
            self.result.setText("Draw!")


    def reset_game(self):
        self.display_player_score.clear()
        self.display_computer_score.clear()
        self.result.setText("LTW Game")
        self.display_player_score.setText("You: 0")
        self.display_computer_score.setText("Computer: 0")


    def update_icon(self, label, path):
        pixmap = QPixmap(path)
        label.setPixmap(pixmap)
        label.setFixedSize(100, 100)
        label.setScaledContents(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = LightningTreeWater()
    game.show()
    sys.exit(app.exec_())