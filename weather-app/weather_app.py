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
        self.city = QLabel("Weather App")
        self.textbox = QLineEdit()
        self.search_btn = QPushButton("Get Weather")
        self.temperature = QLabel()
        self.weather_icon = QLabel()
        self.weather = QLabel()

        self.humidity_logo = QLabel()
        self.pressure_logo = QLabel()
        self.wind_logo = QLabel()

        self.humidity = QLabel()
        self.pressure = QLabel()
        self.wind_speed = QLabel()

        self.humidity_label = QLabel()
        self.pressure_label = QLabel()
        self.wind_label = QLabel()
        
        self.icon_map, self.info_icons = self.load_icon()

        self.designUI()
        self.initUI()


    def load_icon(self):
        try:
            base_path = os.path.dirname(os.path.abspath(__file__))
            json_path = os.path.join(base_path, "weather_icons.json")

            with open(json_path, "r") as file:
                data = json.load(file)
                icon_map = data.get("icon_map", {})
                info_icons = data.get("info_icons", {})
                return icon_map, info_icons
            
        except (FileNotFoundError, json.JSONDecodeError):
            print("'weather_icons.json' not found")
            return {}, {}


    def designUI(self):
        self.city.setStyleSheet("font-size: 30px;")
        self.temperature.setStyleSheet("font-size: 95px;")
        self.weather.setStyleSheet("font-size: 15px;")

        self.humidity_label.setStyleSheet("color: #87888c; font-size: 10px;")
        self.pressure_label.setStyleSheet("color: #87888c; font-size: 10px;")
        self.wind_label.setStyleSheet("color: #87888c; font-size: 10px;")

        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0, 
                    x2: 1, y2: 1, 
                    stop: 0 #202224,
                    stop: 0.3 #101114,
                    stop: 1 #151617
                );
                margin: 2px 1px;              
            }
                           
            QLabel {
                background: transparent;
                font-size: 12px;
                color: #f0f1f7;
                font-family: MADE Outer Sans;
            }
                           
            QLineEdit, QPushButton {
                font-family: MADE Outer Sans;
                font-size: 13px;
                color: #f0f1f7;
                border-radius: 7px;
            }
             
            QLineEdit {
                padding: 8px;
                border: 1px solid #1e1f21;
                background: qlineargradient(
                    x1: 0, y1: 0, 
                    x2: 1, y2: 1, 
                    stop: 0 #202224,
                    stop: 0.3 #1e1f21,
                    stop: 1 #151617
                );
            }
                           
            QPushButton {
                padding: 8px 15px;
                border: 1px solid #5a42a8;
                background: qlineargradient(
                    x1: 0, y1: 0, 
                    x2: 1, y2: 1, 
                    stop: 0.2 #5a42a8,
                    stop: 0.4 #796aad,
                    stop: 0.9 #35256c
                );
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
        hbox2.addWidget(self.humidity_logo, alignment=Qt.AlignHCenter)
        hbox2.addWidget(self.wind_logo, alignment=Qt.AlignHCenter)
        hbox2.addWidget(self.pressure_logo, alignment=Qt.AlignHCenter)

        hbox3 = QHBoxLayout()
        hbox3.addWidget(self.humidity, alignment=Qt.AlignHCenter)
        hbox3.addWidget(self.wind_speed, alignment=Qt.AlignHCenter)
        hbox3.addWidget(self.pressure, alignment=Qt.AlignHCenter)

        hbox4 = QHBoxLayout()
        hbox4.addWidget(self.humidity_label, alignment=Qt.AlignHCenter)
        hbox4.addWidget(self.wind_label, alignment=Qt.AlignHCenter)
        hbox4.addWidget(self.pressure_label, alignment=Qt.AlignHCenter)

        vbox = QVBoxLayout()
        vbox.addWidget(self.city, alignment=Qt.AlignHCenter)
        vbox.addLayout(hbox1)
        vbox.addWidget(self.temperature, alignment=Qt.AlignHCenter)
        vbox.addSpacing(-70)
        vbox.addWidget(self.weather_icon, alignment=Qt.AlignHCenter)
        vbox.addSpacing(-50)
        vbox.addWidget(self.weather, alignment=Qt.AlignHCenter)
        vbox.addLayout(hbox2)
        vbox.addSpacing(-39)
        vbox.addLayout(hbox3)
        vbox.addSpacing(-47)
        vbox.addLayout(hbox4)
        vbox.setContentsMargins(40, 15, 40, 15)

        self.setLayout(vbox)


    def get_weather(self):
        city = self.textbox.text().strip()
        if not city:
            return ""
        
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
        if weather_data == "":
            return
        
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

        base_path = os.path.dirname(os.path.abspath(__file__))

        icon_path = self.icon_map.get(weather)
        if icon_path:
            full_icon_path = os.path.join(base_path, icon_path)
            if os.path.exists(full_icon_path):
                pixmap = QPixmap(full_icon_path)
                self.weather_icon.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            else:
                print("Icon not found: ", full_icon_path)
                self.weather_icon.clear()   
        else:
            print("No icon path for weather: ", weather)
            self.weather_icon.clear()

        for icon_label, key in [
            (self.humidity_logo, "humidity"),
            (self.pressure_logo, "pressure"),
            (self.wind_logo, "wind")
        ]:
            icon_file = self.info_icons.get(key)
            if icon_file:
                full_path = os.path.join(base_path, icon_file)
                if os.path.exists(full_path):
                    icon_label.setPixmap(QPixmap(full_path).scaled(18, 18, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        self.temperature.setText(f"{temp:.0f}°")
        self.weather.setText(weather)
        self.city.setText(f"{city_name}, {country}")
        self.humidity.setText(f"{humidity}%")
        self.pressure.setText(f"{pressure} hPa")
        self.wind_speed.setText(f"{wind_speed} m/s")

        self.humidity_label.setText("Humidity")
        self.pressure_label.setText("Pressure")
        self.wind_label.setText("Wind")


    def display_error(self):
        self.city.setText("City not found!")
        self.weather_icon.clear()
        for label in [
            self.temperature, self.weather,
            self.humidity_logo, self.pressure_logo, self.wind_logo,
            self.humidity, self.pressure, self.wind_speed,
            self.humidity_label, self.pressure_label, self.wind_label
        ]:
            label.clear()
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather = WeatherApp()
    weather.show()
    sys.exit(app.exec_())