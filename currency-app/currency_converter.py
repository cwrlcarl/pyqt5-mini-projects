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
        self.setFixedSize(400, 420)

        self.header = QLabel("Currency Converter", objectName="header")
        self.amount_label = QLabel("Amount")
        self.amount_input  = QLineEdit()
        self.from_currency = QComboBox()
        self.converted_to_label = QLabel("Converted to")
        self.converted_amount  = QLineEdit()
        self.to_currency = QComboBox()
        self.convert_btn = QPushButton("Convert")

        self.initUI()
        self.designUI()
        self.load_currencies()


    def initUI(self):
        self.amount_input.setPlaceholderText("0")
        self.converted_amount.setPlaceholderText("0")
        self.converted_amount.setReadOnly(True)

        self.convert_btn.clicked.connect(self.convert_currency)
        self.convert_btn.setCursor(Qt.PointingHandCursor)

        self.from_currency.setCursor(Qt.PointingHandCursor)
        self.to_currency.setCursor(Qt.PointingHandCursor)

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


    def designUI(self):
        self.setStyleSheet("""
            QWidget {
                font-size: 15px;
                font-family: Poppins;        
                background-color: #f5f6f7;
            }
                           
            QLabel#header {
                font-size: 25px;
                font-weight: Bold;
            }
                           
            QLineEdit {
                font-size: 25px;
                padding: 5px;
                border: 1px solid #adacb5;
                border-radius: 5px;
            }
                           
            QComboBox {
                
            }
                           
            QPushButton {
                color: #f5f6f7;
                border-radius: 21px;
                padding: 10px;
                margin-top: 20px;
                background: qlineargradient(
                    x1: 0, y1: 0, 
                    x2: 1, y2: 1, 
                    stop: 0.2 #63aeff,
                    stop: 0.4 #8ac7ed,
                    stop: 0.9 #0e4cc9
                );
            }
        """)


    def convert_currency(self):
        data = self.get_exchange_rate()

        original_amount = self.amount_input.text().strip()

        if not original_amount or original_amount.isalpha():
            self.amount_input.clear()
            return None

        self.converted_amount.setText(original_amount)


    def get_exchange_rate(self):
        base_currency = self.from_currency.currentText()
        target_symbol = self.to_currency.currentText()

        if not base_currency or not target_symbol:
            return None
        
        params = {
            'access_key': API_KEY,
            'base': base_currency,
            'symbols': target_symbol
        }
        
        return self.make_api_request('latest', params)
        

    def load_currencies(self):
        params = {'access_key': API_KEY}

        data = self.make_api_request('symbols', params)

        if data and 'symbols' in data:
            for currency in data['symbols'].keys():
                self.from_currency.addItem(currency)
                self.to_currency.addItem(currency)
        else:
            return None


    def make_api_request(self, endpoint, params):
        try:
            response = requests.get(f"{BASE_URL}/{endpoint}", params=params)

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