from io import BytesIO
import sys
import requests
from PIL import Image
from PyQt5 import uic
from PyQt5 import QtCore
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QDialog, QLabel, QPushButton, QLineEdit,
    QComboBox, QRadioButton, QTextEdit
)

toponym_to_find = 'Москва'


def search(name='Москва, кремль'):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "69112cab-042a-47a0-b2c3-b53694ca4271",
        "geocode": name,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        pass

    json_response = response.json()

    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]

    return toponym["Point"]["pos"]


def get_image(coords, delta="0.005", map='map'): # coords: "coords_x coords_y"
    toponym_longitude, toponym_lattitude = coords.split(" ")

    map_params = {
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        "spn": ",".join([delta, delta]),
        "l": map,
    }

    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)

    return BytesIO(response.content)


class MainWin(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.post_index = False
        self.initUI()

    def initUI(self):
        self.search_button.clicked.connect(lambda: self.on_click_search())
        self.clean_button.clicked.connect(lambda: self.clean_map())

    def on_click_search(self):
        if self.radio_post_index.isChecked():
            self.post_index = True
        address = self.adress_edit.toPlainText()
        map_type = self.comboBox.currentText()
        Image.open(get_image(search(address), map=map_type)).show()

    def clean_map(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    Map_app = MainWin()
    Map_app.show()
    sys.exit(app.exec())
