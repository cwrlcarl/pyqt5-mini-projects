import sys
import random
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QPushButton)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.Qt import Qt
from PyQt5.QtCore import QSize


class RockPaperScissors(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setFixedSize(400, 450)
        self.set_background("pyqt5-mini-projects/rps-game/assets/bg1.png")
        
        self.title = QLabel(objectName="title")
        self.display_player_score = QLabel("You: 0")
        self.display_computer_score = QLabel("Computer: 0")

        self.player = QLabel()
        self.versus = QLabel("VS")
        self.computer = QLabel()
        
        self.rock = QPushButton()
        self.paper = QPushButton()
        self.scissors = QPushButton()
        self.reset = QPushButton(objectName="reset")

        self.player_score = 0
        self.computer_score = 0
        self.win_rules = {
            self.rock: self.scissors,
            self.paper: self.rock,
            self.scissors: self.paper
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
                color: white;
            }
                           
            QLabel#title {
                font-size: 35px;
            }
                                         
            QPushButton {
                padding: 0px;
                background-color: white;
                border: 2px solid black;
                border-radius: 5px;
            }
                           
            QPushButton#reset {
                border: none;
                background: transparent;
            }
        """)
            

    def initUI(self):
        self.update_titlecard()
        
        scoreboard = QHBoxLayout()
        scoreboard.addWidget(self.display_player_score)
        scoreboard.addWidget(self.display_computer_score)
        scoreboard.setAlignment(Qt.AlignHCenter)

        pvc_layout = QHBoxLayout()
        pvc_layout.addWidget(self.player)
        pvc_layout.addWidget(self.versus)
        pvc_layout.addWidget(self.computer)
        pvc_layout.setAlignment(Qt.AlignHCenter)
        
        self.btn_icons = {
            "rock": {
                "button": self.rock,
                "path": "pyqt5-mini-projects/rps-game/assets/rock.png"
            },
            "paper": {
                "button": self.paper,
                "path": "pyqt5-mini-projects/rps-game/assets/paper.png"
            },
            "scissors": {
                "button": self.scissors,
                "path": "pyqt5-mini-projects/rps-game/assets/scissors.png"
            }
        }

        self.pvc_icons = {
            "player": "pyqt5-mini-projects/rps-game/assets/player.png",
            "computer": "pyqt5-mini-projects/rps-game/assets/computer.png"
        }

        self.update_icon(self.player, self.pvc_icons["player"])
        self.update_icon(self.computer, self.pvc_icons["computer"])

        for choice, data in self.btn_icons.items():
            btn = data["button"]
            path = data["path"]
            btn.setIcon(QIcon(path))
            btn.setIconSize(QSize(40, 40))
            btn.setFixedSize(70, 70)
            btn.clicked.connect(self.play_game)
            btn.setCursor(Qt.PointingHandCursor)

        options = QHBoxLayout()
        options.addWidget(self.rock)
        options.addWidget(self.paper)
        options.addWidget(self.scissors)

        self.reset.setIcon(QIcon("pyqt5-mini-projects/rps-game/assets/reset_button.png"))
        self.reset.setIconSize(QSize(142, 38))
        self.reset.setFixedSize(142, 38)
        self.reset.setCursor(Qt.PointingHandCursor)
        self.reset.clicked.connect(self.reset_game)

        game_layout = QVBoxLayout()
        game_layout.addWidget(self.title, alignment=Qt.AlignHCenter)
        game_layout.addSpacing(30)
        game_layout.addLayout(pvc_layout)
        game_layout.addSpacing(30)
        game_layout.addLayout(options)
        game_layout.addWidget(self.reset, alignment=Qt.AlignHCenter)
        game_layout.addSpacing(-20)
        game_layout.addLayout(scoreboard)
        game_layout.setContentsMargins(25, 25, 25, 25)
        game_layout.setSpacing(30)

        self.setLayout(game_layout)


    def play_game(self):
        player_choice = self.sender()
        computer_choice = random.choice([self.rock, self.paper, self.scissors])

        for choice in self.btn_icons:
            if self.btn_icons[choice]["button"] == player_choice:
                self.update_icon(self.player, self.btn_icons[choice]["path"])

            if self.btn_icons[choice]["button"] == computer_choice:
                self.update_icon(self.computer, self.btn_icons[choice]["path"])
        
        if self.win_rules[player_choice] == computer_choice:
            self.player_score += 1
            self.title.setText("You Win!")
            self.display_player_score.setText(f"You: {self.player_score}")
        elif self.win_rules[computer_choice] == player_choice:
            self.computer_score += 1
            self.title.setText("You Lose!")
            self.display_computer_score.setText(f"Computer: {self.computer_score}")
        else:
            self.title.setText("Draw!")

        self.title.setAlignment(Qt.AlignCenter)


    def reset_game(self):
        self.update_titlecard()
        self.update_icon(self.player, self.pvc_icons["player"])
        self.update_icon(self.computer, self.pvc_icons["computer"])
        self.player_score = 0
        self.computer_score = 0
        self.display_player_score.setText(f"You: {self.player_score}")
        self.display_computer_score.setText(f"Computer: {self.computer_score}")


    def update_icon(self, label, path):
        pixmap = QPixmap(path)
        label.setPixmap(pixmap)
        label.setFixedSize(90, 90)
        label.setScaledContents(True)


    def update_titlecard(self):
        titlecard = QPixmap("pyqt5-mini-projects/rps-game/assets/rps_titlecard.png")
        self.title.setPixmap(titlecard)
        self.title.setFixedSize(161, 95)
        self.title.setScaledContents(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = RockPaperScissors()
    game.show()
    sys.exit(app.exec_())