import sys
import random
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout,
                             QLineEdit, QLabel, QPushButton)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.Qt import Qt
from PyQt5.QtCore import QSize


class NumberGuessing(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setFixedSize(400, 430)

        self.title = QLabel("Number Guessing")
        self.description = QLabel("I am thingking of a number between 1-100.\nCan you guess it?",
                                  objectName="desc")
        self.textbox = QLineEdit()
        self.guess_btn = QPushButton("Guess")
        self.result = QLabel("You guessed it!")
        self.guess = QLabel("Number of guesses: 0")

        self.initUI()
        self.designUI()

    
    def initUI(self):
        widgets = [
            self.title,
            self.description,
            self.textbox,
            self.guess_btn,
            self.result,
            self.guess
        ]

        layout = QVBoxLayout()
        
        for widget in widgets:
            layout.addWidget(widget, alignment=Qt.AlignCenter)

        self.setLayout(layout)


    def designUI(self):
        self.setStyleSheet("""
            QLabel {
                font-family: MADE Outer Sans;
                font-size: 20px;
            }
                           
            QLabel#desc {
                font-size: 10px;        
            }
        """)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = NumberGuessing()
    game.show()
    sys.exit(app.exec_())