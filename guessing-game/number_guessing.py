import sys
import random
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QLineEdit, QLabel, QPushButton)
from PyQt5.Qt import Qt


class NumberGuessing(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setFixedSize(400, 430)

        self.title = QLabel("Number Guessing", objectName="game")
        self.target = QLineEdit()
        self.confirm_btn = QPushButton("Confirm")
        self.description = QLabel("*Please select your target number*",
                                  objectName="desc")
        self.textbox = QLineEdit()
        self.guess_btn = QPushButton("Guess")
        self.reset_btn = QPushButton("Reset")
        self.result = QLabel("Can you guess it?", objectName="result")
        self.guess = QLabel("Attempts: 0")

        self.target_num = None
        self.secret_number = None
        self.guess_count = 0

        self.initUI()
        self.designUI()

    
    def initUI(self):
        target_layout = QHBoxLayout()
        target_layout.addWidget(self.target)
        target_layout.addWidget(self.confirm_btn)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.guess_btn)
        btn_layout.addWidget(self.reset_btn)

        widgets = [
            self.title,
            target_layout,
            self.description,
            self.textbox,
            btn_layout,
            self.result,
            self.guess
        ]

        layout = QVBoxLayout()
        
        for widget in widgets:
            if widget is not target_layout and widget is not btn_layout:
                layout.addWidget(widget, alignment=Qt.AlignCenter)
            else:
                layout.addLayout(widget)

        self.target.setPlaceholderText("Target")
        self.target.returnPressed.connect(self.random_number)
        self.confirm_btn.clicked.connect(self.random_number)

        self.textbox.setPlaceholderText("Enter guess")
        self.textbox.returnPressed.connect(self.show_result)
        self.guess_btn.clicked.connect(self.show_result)
        self.reset_btn.clicked.connect(self.reset_game)
        
        self.setLayout(layout)

        layout.setContentsMargins(30, 10, 30, 10)


    def designUI(self):
        self.setStyleSheet("""
            QLabel, QPushButton {
                font-family: FreeSans;
                font-size: 15px;
            }
                           
            QLabel#game {
                font-size: 25px;        
            }
                           
            QLabel#desc, QLabel#result {
                font-size: 12px;
                color: #3d3d3d;               
            }
                           
            QPushButton {
                font-family: FreeSans;      
            }
        """)


    def random_number_generator(self, target):
        return random.randint(1, target)


    def random_number(self):
        target = self.target.text().strip()

        if not target or target.isalpha():
            self.description.setText("*Please enter a positive number*")
            self.target.clear()
            return
        else:
            self.description.setText(f"You enter a target: {target}")
            self.target.setReadOnly(True)
        
        self.target_num = int(target)
        if self.target_num < 1:
            self.description.setText("*Please enter a positive number*")
            self.textbox.clear()
            return
        
        self.secret_number = self.random_number_generator(self.target_num)


    def show_result(self):
        if self.target.text().strip() == "":
            self.result.setText("*Please select a target first*")
            self.textbox.clear()
            return

        user_input = self.textbox.text().strip()

        if not user_input or user_input.isalpha():
            self.result.setText("*Please enter a positive number*")
            self.textbox.clear()
            return

        user_input = int(user_input)

        if user_input < 1 or user_input > self.target_num:  # Add range check
            self.result.setText(f"*Please enter a number between 1-{self.target_num}*")
            self.textbox.clear()
            return

        if user_input > self.secret_number:
            self.result.setText("Too high. Try again!")
            self.textbox.clear()
        elif user_input < self.secret_number:
            self.result.setText("Too low. Try again!")
            self.textbox.clear()
        else:
            self.textbox.setReadOnly(True)
            self.result.setText(f"You guessed the number: {self.secret_number}")
            self.guess_count += 1
            self.guess.setText(f"Attempts: {self.guess_count}")
            return

        self.guess_count += 1
        self.guess.setText(f"Attempts: {self.guess_count}")


    def reset_game(self):
        if self.target_num is None:
            return
        
        self.secret_number = self.random_number_generator(self.target_num)
        self.guess_count = 0

        self.target.clear()
        self.target.setReadOnly(False)
        self.description.setText("*Please select your target number*")
        self.textbox.clear()
        self.textbox.setReadOnly(False)
        self.result.setText("Can you guess it?")
        self.guess.setText(f"Attempts: {self.guess_count}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = NumberGuessing()
    game.show()
    sys.exit(app.exec_())