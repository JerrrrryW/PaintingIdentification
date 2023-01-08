import sys
import os
from PyQt5 import uic
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class DemoWindow:

    def __init__(self):
        self.ui = uic.loadUi('QT_UI\\flood_fill_ui.ui')
        self.ui.select_btn.clicked.connect(self.selectImage)
        self.Path = os.getcwd()

    def selectImage(self):
        print('Select Button Clicked!')
        imgName, imgType = QFileDialog.getOpenFileName(None, "打开图片", self.Path, "*.jpg;;*.png;;All Files(*)")
        jpg = QtGui.QPixmap(imgName).scaledToWidth(self.ui.origin_image_lb.width())
        self.ui.origin_image_lb.setPixmap(jpg)


if __name__ == '__main__':
    app = QApplication([])
    demoWindow = DemoWindow()
    demoWindow.ui.show()
    app.exec_()
