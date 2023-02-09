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


def search(name='Москва, кремль'): # Принимает адрес
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "Apikey",
        "geocode": name,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        print('error geocoder', response.reason)

    json_response = response.json()

    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]

    return ','.join(toponym["Point"]["pos"].split(' '))
    # Возвращает координаты через запятую


def get_image(coords, map='map', z='12'):
    # Принимает координаты формат карты и уровень зума

    map_params = {
        "ll": coords,
        "l": map,
        "z": z,
    }

    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)

    with open('pic.png', 'wb') as picture:
        picture.write(response.content)


class MainWin(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.post_index = False
        self.z = '12'
        self.address = 'Москва, Кремль'
        self.map_type = 'map'
        self.coords = '0, 0'
        self.initUI()

    def initUI(self):
        self.search_button.clicked.connect(lambda: self.on_click_search())
        self.clean_button.clicked.connect(lambda: self.clean_map())

    def on_click_search(self):
        # Осуществляет поиск
        if self.radio_post_index.isChecked():
            self.post_index = True

        self.address = self.adress_edit.toPlainText()
        if self.address == '':
            self.address = 'Кремль, Москва'

        self.map_type = self.comboBox.currentText()

        # Поиск по адресу
        self.coords = search(self.address)

        # Обновление pic.png
        get_image(self.coords, z=self.z, map=self.map_type)
        self.map_picture_line.setPixmap(QPixmap('pic.png'))

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_W:
            # Увеличить зум

            self.z = str(int(self.z) + 1)
            get_image(self.coords, z=self.z, map=self.map_type)
            self.map_picture_line.setPixmap(QPixmap('pic.png'))
        if event.key() == QtCore.Qt.Key_S:
            # Уменьшить зум

            self.z = str(int(self.z) - 1)
            get_image(self.coords, z=self.z, map=self.map_type)
            self.map_picture_line.setPixmap(QPixmap('pic.png'))
        if event.key() == QtCore.Qt.Key_Up:
            # Увеличить координату у
            x, y = self.coords.split(',')[1]
            self.coords = x + str(float(y) + 0.05)
            get_image(self.coords, z=self.z, map=self.map_type)
            self.map_picture_line.setPixmap(QPixmap('pic.png'))
        if event.key() == QtCore.Qt.Key_Down:
            # Уменьшить координату у
            x, y = self.coords.split(',')[1]
            self.coords = x + str(float(y) - 0.05)
            get_image(self.coords, z=self.z, map=self.map_type)
            self.map_picture_line.setPixmap(QPixmap('pic.png'))
        if event.key() == QtCore.Qt.Key_Up:
            # Увеличить координату х
            x, y = self.coords.split(',')[1]
            self.coords = str(float(x) + 0.05) + y
            get_image(self.coords, z=self.z, map=self.map_type)
            self.map_picture_line.setPixmap(QPixmap('pic.png'))
        if event.key() == QtCore.Qt.Key_Down:
            # Уменьшить координату х
            x, y = self.coords.split(',')[1]
            self.coords = str(float(x) - 0.05) + y
            get_image(self.coords, z=self.z, map=self.map_type)
            self.map_picture_line.setPixmap(QPixmap('pic.png'))
        event.accept()

    def clean_map(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    Map_app = MainWin()
    Map_app.show()
    sys.exit(app.exec())
