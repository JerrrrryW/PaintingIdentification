import sys
import os
from PyQt5 import uic
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from scalableImageLabel import scalableImageLabel


class DemoWindow:

    def __init__(self):
        self.ui = uic.loadUi('QT_UI\\flood_fill_ui.ui')
        self.ui.selectBtn1.clicked.connect(self.selectImage)
        self.ui.imageLabel1 = scalableImageLabel(self.ui.groupBox_3)
        self.ui.imageLabel1.setScaledContents(False)
        self.ui.imageLabel1.setAlignment(QtCore.Qt.AlignCenter)
        self.ui.imageLabel1.setObjectName("imageLabel1")
        self.ui.horizontalLayout_5.addWidget(self.ui.imageLabel1)
        self.ui.imageLabel2 = scalableImageLabel(self.ui.groupBox_4)
        self.ui.imageLabel2.setScaledContents(False)
        self.ui.imageLabel2.setAlignment(QtCore.Qt.AlignCenter)
        self.ui.imageLabel2.setObjectName("imageLabel2")
        self.ui.horizontalLayout_6.addWidget(self.ui.imageLabel2)

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
