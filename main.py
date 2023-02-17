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
        "apikey": "69112cab-042a-47a0-b2c3-b53694ca4271",
        "geocode": name,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        print('error geocoder', response.reason)

    json_response = response.json()

    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]


    ind = toponym['metaDataProperty']['GeocoderMetaData']['Address'].get('postal_code', None)
    return (','.join(toponym["Point"]["pos"].split(' ')),
            toponym['metaDataProperty']['GeocoderMetaData']['text'],
            ind)
    # Возвращает координаты через запятую, адрес, индекс


def get_image(coords, coords_flag, map='map', z='12'):
    # Принимает координаты формат карты и уровень зума

    if coords_flag is None:
        map_params = {
            "ll": coords,
            "l": map,
            "z": z,
        }
    else:
        map_params = {
            "ll": coords,
            "l": map,
            "z": z,
            "pt": f"{coords_flag},flag"
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
        self.z = 12
        self.address = 'Москва, Кремль'
        self.map_type = 'map'
        self.coords = '55.000000,37.000000'
        self.coords_flag = None
        self.initUI()

    def initUI(self):
        self.search_button.clicked.connect(lambda: self.on_click_search())
        self.clean_button.clicked.connect(lambda: self.clean_map())

    def on_click_search(self):
        # Осуществляет поиск
        if self.radio_post_index.isChecked():
            self.post_index = True
        else:
            self.post_index = False

        self.address = self.adress_edit.toPlainText()
        if self.address == '':
            self.address = 'Кремль, Москва'

        self.map_type = self.comboBox.currentText()

        # Поиск по адресу
        self.coords, self.address, postal_code = search(self.address)
        self.coords_flag = self.coords

        if self.post_index and not (postal_code is None):
            self.adress_edit.setPlainText(self.address + ', ' + postal_code)
        else:
            self.adress_edit.setPlainText(self.address)
        # Обновление pic.png
        get_image(self.coords, self.coords_flag, z=self.z, map=self.map_type)
        self.map_picture_line.setPixmap(QPixmap('pic.png'))

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_W:
            # Увеличить зум

            self.z += 1 if self.z < 17 else 0
            get_image(self.coords, self.coords_flag, z=str(self.z), map=self.map_type)
            self.map_picture_line.setPixmap(QPixmap('pic.png'))
        if event.key() == QtCore.Qt.Key_S:
            # Уменьшить зум

            self.z -= 1 if self.z > 0 else 0
            get_image(self.coords, self.coords_flag, z=str(self.z), map=self.map_type)
            self.map_picture_line.setPixmap(QPixmap('pic.png'))
        if event.key() == QtCore.Qt.Key_Up:
            # Увеличить координату у
            x, y = self.coords.split(',')
            diff = 360 / 2 ** self.z
            self.coords = x + ',' + str(float(y) + (diff if float(y) + diff <= 90 else 0))
            get_image(self.coords, self.coords_flag, z=self.z, map=self.map_type)
            self.map_picture_line.setPixmap(QPixmap('pic.png'))
        if event.key() == QtCore.Qt.Key_Down:
            # Уменьшить координату у
            x, y = self.coords.split(',')
            diff = 360 / 2 ** self.z
            self.coords = x + ',' + str(float(y) - (diff if float(y) - diff >= -90 else 0))
            get_image(self.coords, self.coords_flag, z=self.z, map=self.map_type)
            self.map_picture_line.setPixmap(QPixmap('pic.png'))
        if event.key() == QtCore.Qt.Key_Right:
            # Увеличить координату х
            x, y = self.coords.split(',')
            diff = 720 / 2 ** self.z
            self.coords = str(float(x) + (diff if float(x) + diff <= 180 else 0)) + ',' + y
            get_image(self.coords, self.coords_flag, z=self.z, map=self.map_type)
            self.map_picture_line.setPixmap(QPixmap('pic.png'))
        if event.key() == QtCore.Qt.Key_Left:
            # Уменьшить координату х
            x, y = self.coords.split(',')
            diff = 720 / 2 ** self.z
            self.coords = str(float(x) - (diff if float(x) - diff >= -180 else 0)) + ',' + y
            get_image(self.coords, self.coords_flag, z=self.z, map=self.map_type)
            self.map_picture_line.setPixmap(QPixmap('pic.png'))
        event.accept()

    def clean_map(self):
        self.address = 'Москва'
        self.z = 12
        self.map_type = 'map'
        self.coords = '55.000000,37.000000'
        self.coords_flag = None
        get_image(self.coords, self.coords_flag, z=self.z, map=self.map_type)
        self.map_picture_line.setPixmap(QPixmap('pic.png'))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    Map_app = MainWin()
    Map_app.show()
    sys.exit(app.exec())
