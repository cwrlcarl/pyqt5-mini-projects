import json
import os
import requests
import sys
from dotenv import load_dotenv
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton)
from PyQt5.QtGui import QPixmap
from PyQt5.Qt import Qt

load_dotenv()
API_KEY = os.getenv("API_KEY")

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setFixedSize(400, 450)
        self.city = QLabel("Weather App", objectName="city")
        self.textbox = QLineEdit()
        self.search_btn = QPushButton("Get Weather")
        self.weather_icon = QLabel()
        self.temperature = QLabel(objectName="temperature")
        self.weather = QLabel(objectName="weather")
        self.humidity = QLabel(objectName="humidity")
        self.pressure = QLabel(objectName="pressure")
        self.wind_speed = QLabel(objectName="wind_speed")
        self.icon_map = self.load_icon()
        self.designUI()
        self.initUI()


    def load_icon(self):
        try:
            base_path = os.path.dirname(os.path.abspath(__file__))
            json_path = os.path.join(base_path, "weather_icons.json")

            with open(json_path, "r") as file:
                return json.load(file)
            
        except (FileNotFoundError, json.JSONDecodeError):
            print("⚠️ weather_icons.json not found")
            return {}


    def designUI(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #151617;
                margin: 2px 1px;              
            }
                           
            QLineEdit, QPushButton {
                font-family: MADE Outer Sans;
                font-size: 13px;
                border-radius: 7px;
            }
                           
            QLabel {
                background: transparent;
                font-size: 16px;
                color: #f0f1f7;
                font-family: MADE Outer Sans;
            }
                           
            QLabel#city {
                font-size: 30px;
            }
                                  
            QLabel#temperature {
                font-size: 95px;
            }
            
            QLineEdit {
                padding: 8px;
                background-color: #1e1f21;
                color: #f0f1f7;
            }
                           
            QPushButton {
                padding: 10px 18px;
                color: #151617;
                background-color: #fabb03;
            }
        """)


    def initUI(self):
        self.textbox.setPlaceholderText("Search place")
        self.textbox.returnPressed.connect(self.display_weather)

        self.search_btn.setCursor(Qt.PointingHandCursor)
        self.search_btn.clicked.connect(self.display_weather)

        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.textbox)
        hbox1.addWidget(self.search_btn)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.humidity, alignment=Qt.AlignHCenter)
        hbox2.addWidget(self.pressure, alignment=Qt.AlignHCenter)
        hbox2.addWidget(self.wind_speed, alignment=Qt.AlignHCenter)
        
        vbox = QVBoxLayout()
        vbox.addWidget(self.city, alignment=Qt.AlignHCenter)
        vbox.addLayout(hbox1)
        vbox.addSpacing(6)
        vbox.addWidget(self.temperature, alignment=Qt.AlignHCenter)
        vbox.addSpacing(-70)
        vbox.addWidget(self.weather_icon, alignment=Qt.AlignHCenter)
        vbox.addSpacing(-50)
        vbox.addWidget(self.weather, alignment=Qt.AlignHCenter)
        vbox.addLayout(hbox2)
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
                return {
                    "city_name": data["name"],
                    "temp": data["main"]["temp"],
                    "weather": data["weather"][0]["main"],
                    "country": data["sys"]["country"],
                    "humidity":data["main"]["humidity"],
                    "pressure": data["main"]["pressure"],
                    "wind_speed":data["wind"]["speed"]
                }
            else:
                return None

        except requests.exceptions.RequestException as e:
            print("Error fetching weather: ", e)
            return None
        

    def display_weather(self):
        weather_data = self.get_weather()
        if not weather_data:
            self.display_error()
            return
        
        city_name = weather_data["city_name"]
        temp = weather_data["temp"]
        weather = weather_data["weather"]
        country = weather_data["country"]
        humidity = weather_data["humidity"]
        pressure = weather_data["pressure"]
        wind_speed = weather_data["wind_speed"]

        icon_path = self.icon_map.get(weather)
        if icon_path:
            base_path = os.path.dirname(os.path.abspath(__file__))
            full_icon_path = os.path.join(base_path, icon_path)

            if os.path.exists(full_icon_path):
                pixmap = QPixmap(full_icon_path)
                self.weather_icon.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            else:
                print("❌ Icon not found:", full_icon_path)
                self.weather_icon.clear()
                
        else:
            print("⚠️ No icon path for weather:", weather)
            self.weather_icon.clear()

        self.temperature.setText(f"{temp:.0f}°")
        self.weather.setText(weather)
        self.city.setText(f"{city_name}, {country}")
        self.humidity.setText(f"{humidity}%")
        self.pressure.setText(f"{pressure} hPa")
        self.wind_speed.setText(f"{wind_speed} m/s")


    def display_error(self):
        self.city.setText("⚠️ City not found")
        self.weather_icon.clear()
        self.temperature.clear()
        self.weather.clear()
        self.humidity.clear()
        self.pressure.clear()
        self.wind_speed.clear()
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather = WeatherApp()
    weather.show()
    sys.exit(app.exec_())