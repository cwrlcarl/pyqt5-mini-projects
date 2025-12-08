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
        self.target_input = QLineEdit()
        self.confirm_target_btn = QPushButton("Confirm")
        self.status_label = QLabel("*Please select your target number*",
                                  objectName="status")
        self.guess_input = QLineEdit()
        self.guess_btn = QPushButton("Guess")
        self.reset_btn = QPushButton("Reset")
        self.feedback_label = QLabel("Can you guess it?", objectName="feedback")
        self.hidden_number_label = QLabel("Hidden Number: ?")
        self.attempts_label  = QLabel("Attempts: 0")

        self.target_num = None
        self.secret_number = None
        self.guess_count = 0

        self.initUI()
        self.designUI()

    
    def initUI(self):
        target_layout = QHBoxLayout()
        target_layout.addWidget(self.target_input)
        target_layout.addWidget(self.confirm_target_btn)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.guess_btn)
        btn_layout.addWidget(self.reset_btn)

        game_info_layout = QHBoxLayout()
        game_info_layout.addWidget(self.hidden_number_label)
        game_info_layout.addWidget(self.attempts_label)
        game_info_layout.setAlignment(Qt.AlignHCenter)

        vertical_layout = [
            self.title,
            target_layout,
            self.status_label,
            self.guess_input,
            btn_layout,
            self.feedback_label,
            game_info_layout
        ]

        horizontal_layout = [
            target_layout,
            btn_layout,
            game_info_layout
        ]

        game_layout = QVBoxLayout()
        
        for layout in vertical_layout:
            if layout in horizontal_layout:
                game_layout.addLayout(layout)
            else:
                game_layout.addWidget(layout, alignment=Qt.AlignCenter)

        self.target_input.setPlaceholderText("Enter a target number")
        self.target_input.returnPressed.connect(self.random_number)
        self.confirm_target_btn.clicked.connect(self.random_number)

        self.guess_input.setPlaceholderText("Enter your guess")
        self.guess_input.returnPressed.connect(self.show_result)
        self.guess_btn.clicked.connect(self.show_result)
        self.reset_btn.clicked.connect(self.reset_game)
        
        self.setLayout(game_layout)

        game_layout.setContentsMargins(30, 10, 30, 10)


    def designUI(self):
        self.setStyleSheet("""
            QLabel, QPushButton {
                font-family: FreeSans;
                font-size: 15px;
            }
                           
            QLabel#game {
                font-size: 25px;        
            }
                           
            QLabel#status, QLabel#feedback {
                font-size: 12px;
                color: #eb5e5e;               
            }
                           
            QPushButton {
                font-family: FreeSans;      
            }
        """)


    def random_number_generator(self, target):
        return random.randint(1, target)


    def random_number(self):
        target = self.target_input.text().strip()

        if not target or target.isalpha():
            self.status_label.setText("*Please enter a positive number*")
            self.target_input.clear()
            return
        else:
            self.status_label.setText(f"Guess a number between 1-{target}")
            self.target_input.setReadOnly(True)
        
        self.target_num = int(target)
        if self.target_num < 1:
            self.status_label.setText("*Please enter a positive number*")
            self.guess_input.clear()
            return
        
        self.secret_number = self.random_number_generator(self.target_num)


    def show_result(self):
        if self.target_input.text().strip() == "":
            self.feedback_label.setText("*Please select a target first*")
            self.guess_input.clear()
            return

        user_input = self.guess_input.text().strip()

        if not user_input or user_input.isalpha():
            self.feedback_label.setText("*Please enter a positive number*")
            self.guess_input.clear()
            return

        user_input = int(user_input)

        if user_input < 1 or user_input > self.target_num:
            self.feedback_label.setText(f"*Please enter a number between 1-{self.target_num}*")
            self.guess_input.clear()
            return

        if user_input > self.secret_number:
            self.feedback_label.setText("Too high. Try again!")
            self.guess_input.clear()
        elif user_input < self.secret_number:
            self.feedback_label.setText("Too low. Try again!")
            self.guess_input.clear()
        else:
            self.guess_input.setReadOnly(True)
            self.feedback_label.setText(f"Congratulations. You guessed the number!")
            self.hidden_number_label.setText(f"Hidden Number: {self.secret_number}")
            self.attempts_label.setText(f"Attempts: {self.guess_count+1}")
            return

        self.guess_count += 1
        self.attempts_label.setText(f"Attempts: {self.guess_count}")


    def reset_game(self):
        if self.target_num is None:
            return
        
        self.secret_number = self.random_number_generator(self.target_num)
        self.guess_count = 0

        self.target_input.clear()
        self.target_input.setReadOnly(False)
        self.status_label.setText("*Please select your target number*")
        self.guess_input.clear()
        self.guess_input.setReadOnly(False)
        self.feedback_label.setText("Can you guess it?")
        self.attempts_label.setText(f"Attempts: {self.guess_count}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = NumberGuessing()
    game.show()
    sys.exit(app.exec_())   