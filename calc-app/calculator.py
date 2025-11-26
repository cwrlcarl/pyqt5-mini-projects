import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout,
                             QVBoxLayout, QLineEdit, QPushButton)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
from PyQt5.Qt import Qt


class Calculator(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setFixedSize(330, 500)

        self.display = QLineEdit()
        self.is_error = False

        self.initUI()
        self.designUI()


    def initUI(self):
        self.display.setFixedSize(290, 115)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setPlaceholderText("0")
        self.display.setReadOnly(True)

        buttons = {
            "<-": (0, 0), "C": (0, 1), "%": (0, 2), "÷": (0, 3),
            "7": (1, 0), "8": (1, 1), "9": (1, 2), "×": (1, 3),
            "4": (2, 0), "5": (2, 1), "6": (2, 2), "-": (2, 3),
            "1": (3, 0), "2": (3, 1), "3": (3, 2), "+": (3, 3),
            "0": (4, 0), ".": (4, 1), "=": (4, 2, 1, 2)
        }

        grid = QGridLayout()

        for btn, pos in buttons.items():
            button = QPushButton(btn)

            if btn == "<-":
                self.backspace_btn = button
                button.setIcon(QIcon("pyqt5-mini-projects/calc-app/assets/arrow-left.png"))
                button.setIconSize(QSize(25, 30))
                button.setText("")

            if btn == "=":
                self.equal_btn = button
                grid.addWidget(self.equal_btn, pos[0], pos[1], pos[2], pos[3])
            else:
                grid.addWidget(button, pos[0], pos[1])
            button.setCursor(Qt.PointingHandCursor)
            button.clicked.connect(self.show_display)

        layout = QVBoxLayout()
        layout.addWidget(self.display)
        layout.addLayout(grid)
        layout.setContentsMargins(20, 20, 20, 20)

        self.setLayout(layout)


    def designUI(self):
        self.equal_btn.setStyleSheet("""
            border: 1px solid #b5aee8;
            background: qlineargradient(
                x1: 0, y1: 0, 
                x2: 1, y2: 1, 
                stop: 0.1 #b5aee8, 
                stop: 0.5 #7a72f2,
                stop: 0.9 #4e39c4
            );
        """)
        
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0, 
                    x2: 1, y2: 1, 
                    stop: 0 #202224,
                    stop: 0.3 #101114,
                    stop: 1 #1a1a1c
                );
            }
                           
            QLineEdit, QPushButton {
                color: #e8e6f0;
                margin: 1px;
                padding: 15px;
                font-family: Joystix;
                border-radius: 10px;
            }
                                                                      
            QLineEdit {
                font-size: 50px;
                border: 1px solid #303336;
                background: qlineargradient(
                    x1: 0, y1: 0, 
                    x2: 1, y2: 1, 
                    stop: 0.1 #303336,
                    stop: 0.4 #1f2123,
                    stop: 0.8 #181a1b
                );
            }
                           
            QPushButton {
                font-size: 25px;   
                border: 1px solid #1e1f21;
                background: qlineargradient(
                    x1: 0, y1: 0, 
                    x2: 1, y2: 1, 
                    stop: 0 #202224,
                    stop: 0.3 #1e1f21,
                    stop: 1 #151617
                );        
            }
                           
            QPushButton:hover {
                border: 1px solid #b5aee8;
                background: qlineargradient(
                    x1: 0, y1: 0, 
                    x2: 1, y2: 1, 
                    stop: 0.1 #b5aee8,  
                    stop: 0.5 #7a72f2,
                    stop: 0.9 #4e39c4
                );
            }
        """)


    def show_display(self):
        sender = self.sender()
        button = self.sender().text()
        text = self.display.text()
        operators = "÷×-+%."
        last_char = text[-1:] if text else ""

        if button == "C":
            self.display.clear()
            self.is_error = False
        elif sender == self.backspace_btn:
            if self.is_error:
                self.display.clear()
                self.is_error = False
            else:
                self.display.backspace()
        elif button == "=":
            self.result()

        elif text == "0" and button.isdigit():
            self.display.setText(button)
        elif text == "0" and button == ".":
            self.display.insert(button)
        elif text == "0" and button == "0":
            return
        elif last_char in operators and button in operators:
            return
        
        else:
            if self.is_error == False:
                self.display.insert(button)
            else:
                self.display.setText(button)
                self.is_error = False


    def result(self):
        try:
            expr = self.display.text().replace("÷", "/").replace("×", "*")
            if expr.strip() == "":
                return
            else:
                self.display.setText(str(eval(expr)))
        except Exception:
            self.display.setText("(˘︹˘)")
            self.display.setStyleSheet("font-family: Monocraft")
            self.is_error = True


if __name__ == "__main__":
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())