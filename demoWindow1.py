import sys
import os
from PyQt5 import uic
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from scalableImageLabel import scalableImageLabel, global_refresh_result_signal


class DemoWindow:

    def __init__(self):
        self.ui = uic.loadUi('QT_UI\\flood_fill_ui.ui')
        self.initImageLabels()

        self.toolGroup = QButtonGroup()
        self.initToolBar()

        self.selectedImgNum = 0
        self.imageLabels = [self.ui.imageLabel1, self.ui.imageLabel2]  # to access the label faster

        self.initClickedBtnConnection()

        self.Path = os.getcwd()

    def initImageLabels(self):
        # Load custom image label
        self.ui.imageLabel1 = scalableImageLabel(self.ui.image1GroupBox)
        self.ui.imageLabel1.setScaledContents(False)
        self.ui.imageLabel1.setAlignment(QtCore.Qt.AlignCenter)
        self.ui.imageLabel1.setObjectName("imageLabel1")
        self.ui.horizontalLayout_5.addWidget(self.ui.imageLabel1)
        self.ui.imageLabel2 = scalableImageLabel(self.ui.image2GroupBox)
        self.ui.imageLabel2.setScaledContents(False)
        self.ui.imageLabel2.setAlignment(QtCore.Qt.AlignCenter)
        self.ui.imageLabel2.setObjectName("imageLabel2")
        self.ui.horizontalLayout_6.addWidget(self.ui.imageLabel2)

    def initToolBar(self):
        self.toolGroup.addButton(self.ui.floodFillBtn, 0)
        self.toolGroup.addButton(self.ui.squareCutBtn, 1)
        self.toolGroup.addButton(self.ui.freeCutBtn, 2)
        self.toolGroup.addButton(self.ui.sensorBtn, 3)
        self.toolGroup.setExclusive(True)

    def initClickedBtnConnection(self):
        # image file uploading
        self.ui.selectBtn1.clicked.connect(lambda: self.open(self.ui.imageLabel1))
        self.ui.selectBtn2.clicked.connect(lambda: self.open(self.ui.imageLabel2))
        # highlight the groupbox corresponding to the selected image label
        global_refresh_result_signal.highlight_selected_box.connect(self.onLabelClicked)

        self.toolGroup.buttonPressed[int].connect(lambda _:  # [int] 指定了信号传递的为触发的按钮id
                                                  self.onToolBtnClicked(_, self.imageLabels[self.selectedImgNum]))
        self.toolGroup.buttonReleased[int].connect(lambda:
                                                   self.onToolBtnReleased(self.imageLabels[self.selectedImgNum]))

    def onLabelClicked(self, index: int):
        # the corresponding GroupBox to blue and the other groupboxes to grey
        print(f"groupbox {index} clicked!")
        if index == 1:
            self.ui.imageLabel1.isSelected = True
            self.ui.imageLabel2.isSelected = False
            self.ui.image1GroupBox.setStyleSheet("QGroupBox {border: 3px solid blue;}")
            self.ui.image2GroupBox.setStyleSheet("")
        elif index == 2:
            self.ui.imageLabel1.isSelected = False
            self.ui.imageLabel2.isSelected = True
            self.ui.image1GroupBox.setStyleSheet("")
            self.ui.image2GroupBox.setStyleSheet("QGroupBox {border: 3px solid blue;}")

    def onToolBtnClicked(self, clickedBtnID, selectedImageLb: scalableImageLabel):
        selectedImageLb.toolIndex = clickedBtnID
        selectedImageLb.runWhenToolSelected()

    def onToolBtnReleased(self, selectedImageLb: scalableImageLabel):
        selectedImageLb.toolIndex = -1
        selectedImageLb.runWhenToolReleased()

    def open(self, imageLabel):
        self.imgName, imgType = QFileDialog.getOpenFileName(imageLabel, "打开图片", self.Path,
                                                            "*.jpg;;*.png;;All Files(*)")
        self.jpg = QPixmap(self.imgName)
        print("origin:", self.jpg.width(), self.jpg.height())
        print("label:", imageLabel.width(), imageLabel.height())
        # self.jpg = self.jpg.scaledToWidth(imageLabel.width(), imageLabel.height())
        print("scaled:", self.jpg.width(), self.jpg.height())
        # self.label.setPixmap(jpg)
        if not self.jpg.isNull():
            imageLabel.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
            imageLabel.setPixmap(self.jpg)


if __name__ == '__main__':
    app = QApplication([])
    demoWindow = DemoWindow()
    demoWindow.ui.show()
    app.exec_()
