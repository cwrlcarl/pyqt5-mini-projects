import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout,
                             QVBoxLayout, QLineEdit, QPushButton)
from PyQt5.Qt import Qt

class Calculator(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setFixedSize(350, 500)

        self.display = QLineEdit()

        self.designUI()
        self.initUI()


    def designUI(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f7f6;
            }
                           
            QLineEdit, QPushButton {
                color: #363636;
                margin: 1px;
                padding: 15px;
                font-family: Joystix;
                border-radius: 10px;
                background-color: white;
            }
                                                                      
            QLineEdit {
                font-size: 54px;
                border: 2px solid #363636;
                background-color: #dbafd0;
            }
                           
            QPushButton {
                font-size: 25px;            
                border: 1px solid #363636;
            }
                           
            QPushButton:hover {
                background-color: #f7f7f7;
                color: #242526;
                border: 2px solid #363636;
            }
        """)


    def initUI(self):
        self.display.setAlignment(Qt.AlignRight)
        self.display.setPlaceholderText("0")
        self.display.setReadOnly(True)

        buttons = {
            "<-": (0, 0), "C": (0, 1), "%": (0, 2), "÷": (0, 3),
            "7": (1, 0), "8": (1, 1), "9": (1, 2), "×": (1, 3),
            "4": (2, 0), "5": (2, 1), "6": (2, 2), "-": (2, 3),
            "1": (3, 0), "2": (3, 1), "3": (3, 2), "+": (3, 3),
            "0": (4, 0), ".": (4, 1), "=": (4, 2)
        }

        grid = QGridLayout()

        for btn, pos in buttons.items():
            button = QPushButton(btn)
            grid.addWidget(button, pos[0], pos[1])
            button.setCursor(Qt.PointingHandCursor)
            button.clicked.connect(self.show_display)

        layout = QVBoxLayout()
        layout.addWidget(self.display)
        layout.addLayout(grid)
        layout.setContentsMargins(20, 10, 20, 10)

        self.setLayout(layout)


    def show_display(self):
        button = self.sender().text()

        if button == "C":
            self.display.clear()
        elif button == "<-":
            self.display.backspace()
        elif button == "=":
            self.result()
        else:
            self.display.insert(button)


    def result(self):
        try:
            self.display.setText(str(eval(self.display.text())))
        except Exception:
            self.display.setText("Error")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())