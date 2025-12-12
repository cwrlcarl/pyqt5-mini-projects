import os
import sys

import requests
from dotenv import load_dotenv
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget
)


load_dotenv()
API_KEY = os.getenv("API_KEY")
BASE_URL = f"https://api.exchangeratesapi.io/v1/latest"


class CurrencyConverter(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setFixedSize(400, 420)

        self.header = QLabel("Currency Converter")
        self.currency = QLabel("PHP | USD")
        self.amount_input  = QLineEdit()
        self.converted_result  = QLineEdit()
        self.convert_btn = QPushButton("Convert")

        self.initUI()


    def initUI(self):
        converter_layout = QHBoxLayout()
        converter_layout.addWidget(self.amount_input)
        converter_layout.addWidget(self.converted_result)

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


    def get_exchange_rate(self):
        base_currency = self.amount_input.text().strip()
        target_symbol = self.converted_result.text().strip()

        if not base_currency or not target_symbol:
            return None
        
        parameters = {
            'access_key': API_KEY,
            'base': base_currency,
            'symbols': target_symbol
        }
        
        try:
            response = requests.get(BASE_URL, params=parameters)

            if response.status_code == 200:
                data = response.json()

                if data.get('success'):
                    return data
                else:
                    error_msg = data.get('error', {}).get('info', 'Unknown error')
                    print(f"API Error: {error_msg}")
                    return None
            else:
                print(f"HTTP Error: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}") 
            return None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    curr = CurrencyConverter()
    curr.show()
    sys.exit(app.exec_())