import sys
import random
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout,
                             QLineEdit, QLabel, QPushButton)
from PyQt5.Qt import Qt


class NumberGuessing(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setFixedSize(400, 430)

        self.title = QLabel("Number Guessing")
        self.description = QLabel("Guess a number from 1-100",
                                  objectName="desc")
        self.textbox = QLineEdit()
        self.guess_btn = QPushButton("Guess")
        self.reset_btn = QPushButton("Reset")
        self.result = QLabel("Can you guess it?")
        self.guess = QLabel("Attempts: 0")

        self.guess_count = 0

        self.initUI()
        self.designUI()

    
    def initUI(self):
        widgets = [
            self.title,
            self.description,
            self.textbox,
            self.guess_btn,
            self.reset_btn,
            self.result,
            self.guess
        ]

        layout = QVBoxLayout()
        
        for widget in widgets:
            layout.addWidget(widget, alignment=Qt.AlignCenter)

        self.guess_btn.clicked.connect(self.show_result)
        self.reset_btn.clicked.connect(self.reset_game)
        
        self.setLayout(layout)


    def designUI(self):
        self.setStyleSheet("""
            QLabel {
                font-family: Arial;
                font-size: 25px;
            }
                           
            QLabel#desc {
                font-size: 15px;        
            }
        """)


    def show_result(self):
        user_input = self.textbox.text()
        secret_number = str(random.randint(1, 101))

        if user_input > secret_number:
            self.result.setText("Too high. Try again!")
        elif user_input < secret_number:
            self.result.setText("Too low. Try again!")
        else:
            self.result.setText(f"You guessed the number: {secret_number}")

        self.guess_count += 1
        self.guess.setText(f"Attempts: {self.guess_count}")


    def reset_game(self):
        guess_count = 0

        self.result.setText("Can you guess it?")
        self.guess.setText(f"Attempts: {guess_count}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = NumberGuessing()
    game.show()
    sys.exit(app.exec_())