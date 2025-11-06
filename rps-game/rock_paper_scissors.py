import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton)
from PyQt5.QtGui import QPixmap
from PyQt5.Qt import Qt

class RockPaperScissors(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Rock Paper Scissors")
        self.setFixedSize(400, 450)

        self.designUI()
        self.initUI()
    

    def designUI(self):
        pass


    def initUI(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = RockPaperScissors()
    game.show()
    sys.exit(app.exec_())