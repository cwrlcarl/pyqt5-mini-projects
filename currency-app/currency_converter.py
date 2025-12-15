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
        self.setFixedSize(400, 440)

        self.header = QLabel("Currency Converter💲", objectName="header")
        self.amount_label = QLabel("Amount", objectName="amount")
        self.amount_input  = QLineEdit()
        self.from_currency = QComboBox()
        self.converted_to_label = QLabel("Converted to", objectName="converted")
        self.converted_amount  = QLineEdit()
        self.to_currency = QComboBox()
        self.exchange_rate_label = QLabel("1 EUR = 69.20 PHP", objectName="rate")
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

        from_amount_back_container = QWidget(objectName="from")
        from_amount_back_layout = QVBoxLayout()

        from_amount_container = QWidget(objectName="from_inner")
        from_amount_layout = QHBoxLayout()
        from_amount_layout.addWidget(self.amount_input)
        from_amount_layout.addWidget(self.from_currency)
        from_amount_container.setLayout(from_amount_layout)

        from_amount_back_layout.addWidget(from_amount_container)
        from_amount_back_container.setLayout(from_amount_back_layout)
        

        to_amount_back_container = QWidget(objectName="to")
        to_amount_back_layout = QVBoxLayout()

        to_amount_container = QWidget(objectName="to_inner")
        to_amount_layout = QHBoxLayout()
        to_amount_layout.addWidget(self.converted_amount)
        to_amount_layout.addWidget(self.to_currency)
        to_amount_container.setLayout(to_amount_layout)

        to_amount_back_layout.addWidget(to_amount_container)
        to_amount_back_container.setLayout(to_amount_back_layout)
        
        widgets = [
            self.header, self.amount_label, from_amount_back_container,
            self.converted_to_label, to_amount_back_container,
            self.exchange_rate_label, self.convert_btn
        ]

        main_layout = QVBoxLayout()
        for widget in widgets:
            main_layout.addWidget(widget)

        self.setContentsMargins(30, 20, 30, 20)
        self.setLayout(main_layout)


    def designUI(self):
        self.setStyleSheet("""                           
            QWidget{
                font-size: 15px;
                font-family: Poppins;
                color: #1f1f21;     
                background-color: white;
            }
                           
            QWidget#from, QWidget#to {
                background-color: #f5f6f7;
                border-radius: 20%;
                border: 1px solid #f2f2f2;
            }
                           
            QWidget#from_inner, QWidget#to_inner {
                border-radius: 16%;
            }
                           
            QLabel {
                background-color: transparent;
            }
                           
            QLabel#header {
                font-size: 25px;
                font-weight: Bold;
            }
                           
            QLabel#amount, QLabel#converted {
                font-size: 13px;
                color: #5f5f63;
            }
                           
            QLabel#rate {
                font-weight: Bold;
                padding-top: 10px;
            }
                           
            QLineEdit {
                font-size: 25px;
                padding: 5px;
                border: None;
                border-radius: 5px;
                background-color: transparent;
            }
                           
            QComboBox {
                border-radius: 5px;
                padding-left: 8px;
                background-color: #f5f6f7;
                border: 1px solid #f2f2f2;
                width: 35px;
            }
                           
            QComboBox::drop-down {
                image: url(pyqt5-mini-projects/currency-app/assets/down-arrow (1).png);
                width: 13px;
                height: 13px;
                padding-top: 7px;
                padding-right: 7px;
            }
                           
            QPushButton {
                color: #f5f6f7;
                border-radius: 21px;
                padding: 10px;
                margin-top: 5px;
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
        original_amount = self.amount_input.text().strip()

        if not original_amount.isdigit():
            self.amount_input.clear()
            return None
        
        original_amount = float(original_amount)

        data = self.get_exchange_rate()
        base_currency = self.from_currency.currentText()
        currency_code = self.to_currency.currentText()

        if data and 'rates' in data:
            rate = data['rates'].get(currency_code)
            result = original_amount * rate
            result = f"{result:.2f}"
            self.converted_amount.setText(result)
            self.exchange_rate_label.setText(f"1 {base_currency} = {rate:.2f} {currency_code}")
        else:
            return None


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

            self.from_currency.setCurrentText("EUR")
            self.to_currency.setCurrentText("PHP")
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