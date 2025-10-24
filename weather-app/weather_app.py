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
        self.title = QLabel("Weather App", objectName="title")
        self.textbox = QLineEdit()
        self.search_btn = QPushButton("Get Weather")
        self.city = QLabel(objectName="city")
        self.temperature = QLabel(objectName="temperature")
        self.description = QLabel(objectName="description")
        self.initUI()
        self.designUI()


    def designUI(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f1f7;
                margin: 2px 1px;              
            }
                           
            QLabel, QLineEdit, QPushButton {
                font-family: Poppins;
            }
                           
            QLabel {
                font-size: 15px;
                color: #192142;
            }
                           
            QLabel#title {
                font-size: 30px;
            }
                           
            QLabel#temperature {
                font-size: 60px;
            }
            
            QLineEdit, QPushButton {
                font-size: 15px;
                border-radius: 7px;
            }
            
            QLineEdit {
                padding: 8px;
                background-color: #f0f1f7;
                color: #192142;
                border: 1px solid #85899c;
            }
                           
            QPushButton {
                padding: 10px 18px;
                color: #f0f1f7;
                background-color: #192142;
            }
        """)


    def initUI(self):
        self.textbox.setPlaceholderText("Search for place...")
        self.textbox.returnPressed.connect(self.get_weather)

        self.search_btn.setCursor(Qt.PointingHandCursor)
        self.search_btn.clicked.connect(self.get_weather)

        hbox = QHBoxLayout()
        hbox.addWidget(self.textbox)
        hbox.addWidget(self.search_btn)
        
        vbox = QVBoxLayout()
        vbox.addWidget(self.title, alignment=Qt.AlignHCenter)
        vbox.addLayout(hbox)
        vbox.addWidget(self.temperature, alignment=Qt.AlignHCenter)
        vbox.addWidget(self.city, alignment=Qt.AlignHCenter)
        vbox.addWidget(self.description, alignment=Qt.AlignHCenter)
        vbox.setContentsMargins(40, 15, 40, 15)

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
                country = data["sys"]["country"]

                self.temperature.setText(f"{temp}°")
                self.description.setText(description)
                self.city.setText(f"{city_name}, {country}")
            else:
                self.city.setText("⚠️ City not found")
        except requests.exceptions.RequestException:
            return None
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather = WeatherApp()
    weather.show()
    sys.exit(app.exec_())