import sys
import requests
import os
from dotenv import load_dotenv
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton)
from PyQt5.Qt import Qt

load_dotenv()
API_KEY = os.getenv("API_KEY")

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setFixedSize(400, 450)
        self.title = QLabel("🌥️ Weather App")
        self.textbox = QLineEdit()
        self.search_btn = QPushButton("Get Weather")
        self.city_info = QLabel(objectName="city_info")
        self.initUI()
        self.designUI()


    def designUI(self):
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                margin: 2px 1px;              
            }z
                           
            QLabel, QLineEdit, QPushButton {
                font-family: Poppins;
                font-size: 15px;
            }
                           
            QLabel {
                font-size: 30px;
            }
                           
            QLabel#city_info {
                font-size: 20px;s
            }
                           
            QLineEdit {
                padding: 10px;
            }
                           
            QPushButton {
                padding: 10px 15px;
            }
        """)


    def initUI(self):
        self.textbox.setPlaceholderText("Search for city...")
        self.textbox.returnPressed.connect(self.get_weather)

        self.search_btn.setCursor(Qt.PointingHandCursor)
        self.search_btn.clicked.connect(self.get_weather)

        hbox = QHBoxLayout()
        hbox.addWidget(self.textbox)
        hbox.addWidget(self.search_btn)

        vbox = QVBoxLayout()
        vbox.addWidget(self.title)
        vbox.addLayout(hbox)
        vbox.addWidget(self.city_info)
        vbox.setContentsMargins(30, 15, 30, 15)

        self.setLayout(vbox)


    def get_weather(self):
        city = self.textbox.text()
        if not city:
            return
        
        self.textbox.clear()
        
        try:
            base_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            response = requests.get(base_url)

            if response.status_code == 200:
                data = response.json()                  
                city_name = data["name"]
                temp = data["main"]["temp"]
                description = data["weather"][0]["description"] 
                self.city_info.setText(f"{city_name}: {description}, {temp}°C")
            else:
                self.city_info.setText("⚠️ City not found")
        except requests.exceptions.RequestException:
            return None
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather = WeatherApp()
    weather.show()
    sys.exit(app.exec_())