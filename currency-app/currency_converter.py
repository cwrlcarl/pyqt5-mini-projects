import os
import sys

import requests
from dotenv import load_dotenv
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget
)


load_dotenv()
API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.exchangeratesapi.io/v1"


class CurrencyConverter(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setFixedSize(410, 420)

        self.header = QLabel("Currency Converter")
        self.amount_label = QLabel("Amount")
        self.amount_input  = QLineEdit()
        self.from_currency = QComboBox()
        self.converted_to_label = QLabel("Converted to")
        self.converted_amount  = QLineEdit()
        self.to_currency = QComboBox()
        self.convert_btn = QPushButton("Convert")

        self.initUI()
        self.load_currencies()


    def initUI(self):
        self.convert_btn.clicked.connect(self.convert_currency)
        self.convert_btn.setCursor(Qt.PointingHandCursor)

        from_amount = QHBoxLayout()
        from_amount.addWidget(self.amount_input)
        from_amount.addWidget(self.from_currency)

        to_amount = QHBoxLayout()
        to_amount.addWidget(self.converted_amount)
        to_amount.addWidget(self.to_currency)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.header)
        main_layout.addWidget(self.amount_label)
        main_layout.addLayout(from_amount)
        main_layout.addWidget(self.converted_to_label)
        main_layout.addLayout(to_amount)
        main_layout.addWidget(self.convert_btn)

        self.setContentsMargins(30, 20, 30, 20)
        self.setLayout(main_layout)


    def get_exchange_rate(self):
        base_currency = self.to_currency.currentText()
        target_symbol = self.from_currency.currentText()

        if not base_currency or not target_symbol:
            return None
        
        params = {
            'access_key': API_KEY,
            'base': base_currency,
            'symbols': target_symbol
        }
        
        try:
            response = requests.get(f"{BASE_URL}/latest", params=params)

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
        

    def load_currencies(self):
        params = {'access_key': API_KEY}

        try:
            response = requests.get(f"{BASE_URL}/symbols", params=params)

            if response.status_code == 200:
                data = response.json()

                if data.get('success') and 'symbols' in data:
                    for currency in data['symbols'].keys():
                        self.from_currency.addItem(currency)
                        self.to_currency.addItem(currency)
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

    
    def convert_currency(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    curr = CurrencyConverter()
    curr.show()
    sys.exit(app.exec_())