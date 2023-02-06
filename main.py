from PyQt5 import uic, QtCore
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QDialog, QLabel, QPushButton, QLineEdit,
    QComboBox, QRadioButton, QTextEdit
)

import sys


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

    def clean_map(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    Map_app = MainWin()
    Map_app.show()
    sys.exit(app.exec())