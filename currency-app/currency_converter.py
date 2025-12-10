import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QLineEdit, QLabel, QPushButton)
from PyQt5.Qt import Qt


class CurrencyConverter(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setFixedSize(400, 420)

        self.header = QLabel("Currency Converter")
        self.currency = QLabel("PHP | USD")
        self.amount = QLineEdit()
        self.value = QLineEdit()
        self.convert_btn = QPushButton("Convert")

        self.initUI()


    def initUI(self):
        converter_layout = QHBoxLayout()
        converter_layout.addWidget(self.amount)
        converter_layout.addWidget(self.value)

        vertical_layout = [
            self.header,
            self.currency,
            converter_layout,
            self.convert_btn
        ]

        main_layout = QVBoxLayout()
        
        for layout in vertical_layout:
            if layout is not converter_layout:
                main_layout.addWidget(layout)
            else:
                main_layout.addLayout(layout)

        self.setContentsMargins(30, 20, 30, 20)
        self.setLayout(main_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    curr = CurrencyConverter()
    curr.show()
    sys.exit(app.exec_())