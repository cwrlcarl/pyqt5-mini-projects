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
        
        self.result = QLabel("LightningTreeWater")
        self.description = QLabel("Welcome to my Game!", objectName="description")
        self.player = QLabel()
        self.versus = QLabel("vs")
        self.computer = QLabel()
        
        self.lightning = QPushButton()
        self.tree = QPushButton()
        self.water = QPushButton()
        self.reset = QPushButton("Reset")

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
                font-size: 30px;
                padding: 5px;
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
        game_layout.setContentsMargins(25, 25, 25, 25)

        self.setLayout(game_layout)


    def play_game(self):
        sender = self.sender()
        computer_choice = random.choice([self.lightning, self.tree, self.water])

        for choice in self.icons:
            if self.icons[choice]["button"] == sender:
                pixmap = QPixmap(self.icons[choice]["path"])
                self.player.setPixmap(pixmap)
                self.player.setFixedSize(100, 100)
                self.player.setScaledContents(True)

            if self.icons[choice]["button"] == computer_choice:
                pixmap = QPixmap(self.icons[choice]["path"])
                self.computer.setPixmap(pixmap)
                self.computer.setFixedSize(100, 100)
                self.computer.setScaledContents(True)

        win_rules = {
            self.lightning: self.tree,
            self.tree: self.water,
            self.water:  self.lightning
        }

        if win_rules[sender] == computer_choice:
            self.result.setText("You Win!")
        elif win_rules[computer_choice] == sender:
            self.result.setText("You Lose!")
        else:
            self.result.setText("Draw!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = LightningTreeWater()
    game.show()
    sys.exit(app.exec_())