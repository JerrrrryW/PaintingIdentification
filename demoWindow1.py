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

        self.toolGroup = QButtonGroup()
        self.selectedImgNum = 0  # 0,1,2   0 means no img label selected
        self.selectedToolNum = -1  # -1,0,1,2,3   -1 means default moving mode

        self.initImageLabels()
        self.initToolBar()
        self.initClickedBtnConnection()
        self.initTabBar()

        self.imageLabels = [self.ui.imageLabel1, self.ui.imageLabel2]  # to access the label faster

        # highlight the groupbox corresponding to the selected image label
        global_refresh_result_signal.highlight_selected_box.connect(self.onLabelSwitched)
        # show the processing result images on corresponding labels
        global_refresh_result_signal.change_result_image.connect(self.refreshResultImage)

        self.Path = os.getcwd()

    def refreshResultImage(self, resultImg: QPixmap, labelNum):
        if labelNum == 1:
            self.ui.resultImage1.setPixmap(resultImg)
        elif labelNum == 2:
            self.ui.resultImage2.setPixmap(resultImg)

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
        self.toolGroup.addButton(self.ui.moveBtn, 5)
        self.toolGroup.addButton(self.ui.floodFillBtn, 0)
        self.toolGroup.addButton(self.ui.squareCutBtn, 1)
        self.toolGroup.addButton(self.ui.freeCutBtn, 2)
        self.toolGroup.addButton(self.ui.sensorBtn, 3)
        self.toolGroup.setExclusive(True)
        self.ui.moveBtn.setChecked(True)  # the default tool

    def initClickedBtnConnection(self):
        # image file uploading
        self.ui.selectBtn1.clicked.connect(lambda: self.open(self.ui.imageLabel1))
        self.ui.selectBtn2.clicked.connect(lambda: self.open(self.ui.imageLabel2))

        self.toolGroup.buttonPressed[int].connect(lambda _:  # [int] ??????????????????????????????????????????id
                                                  self.onToolBtnClicked(_, self.imageLabels[self.selectedImgNum]))
        self.toolGroup.buttonReleased[int].connect(lambda:
                                                   self.onToolBtnReleased(self.imageLabels[self.selectedImgNum]))

    def initTabBar(self):  # Tri-layer attributes tab bar on the right side
        primaryTabs = ["??????", "??????", "??????", "??????"]
        secondaryTabs = [["??????", "??????"],  # ?????????????????????
                         ["??????", "??????"],  # ?????????????????????
                         ["??????", "??????"],  # ?????????????????????
                         ["??????", "??????"]]  # ?????????????????????
        tertiaryTabs = [[["??????", "??????", "??????"],  # ?????????????????????
                         ["??????", "??????", "??????", "??????"]],  # ?????????????????????
                        [["??????", "??????", "?????????"],  # ?????????????????????
                         ["?????????", "?????????", "?????????"]],  # ?????????????????????
                        [["??????", "??????", "??????"],  # ?????????????????????
                         ["?????????", "?????????", "?????????"]],  # ?????????????????????
                        [["??????", "??????", "?????????"],  # ?????????????????????
                         ["?????????", "?????????", "?????????"]]]  # ?????????????????????

        self.ui.secTabStack.removeWidget(self.ui.secPage1)
        self.ui.terAttrStack.removeWidget(self.ui.terPage1)
        for i in range(len(primaryTabs)):  # retrieve the tabs
            self.ui.primaryTabBar.addItem(primaryTabs[i])  # fill primary indicators in listview
            # create pages dynamically to secondaryTabStack
            secPage = QtWidgets.QWidget()
            secPage.setObjectName(f"secondaryTabPage{i}")
            secLayout = QtWidgets.QHBoxLayout(secPage)

            listview = QtWidgets.QListWidget()
            for j in range(len(secondaryTabs[i])):
                listview.addItem(secondaryTabs[i][j])
                # init terAttrPage in stackedWidget
                terPage = QtWidgets.QWidget()
                terPage.setObjectName(f"tertiaryAttrPage{i}-{j}")
                terLayout = QtWidgets.QVBoxLayout(terPage)
                terLayout.addWidget(self.createTertiaryAttributesGroupBox(tertiaryTabs[i][j], i, j, 1))
                terLayout.addWidget(self.createTertiaryAttributesGroupBox(tertiaryTabs[i][j], i, j, 2))
                self.ui.terAttrStack.addWidget(terPage)
            secLayout.addWidget(listview)
            listview.currentRowChanged.connect(self.on_row_changed(i))

            self.ui.secTabStack.addWidget(secPage)
        self.ui.primaryTabBar.currentRowChanged.connect(self.ui.secTabStack.setCurrentIndex)

    def on_row_changed(self, i):
        return lambda row: self.ui.terAttrStack.setCurrentIndex(2 * i + row)

    def createTertiaryAttributesGroupBox(self, terAttrList: [], pri, sec, pos):  # pri&sec is the parentTab num, pos means up1/down2 image
        attrGroupBox = QGroupBox()
        attrGroupBox.setTitle("Attributes")
        attrLayout = QVBoxLayout(attrGroupBox)
        for i in range(len(terAttrList)):
            attrLayout.addWidget(QLabel(terAttrList[i] + ": "))
            valueLabel = QLabel("0")
            valueLabel.setObjectName(f"terAttrValue{pri}-{sec}-{i}-{pos}")  # to assure objectName is unique
            slideBar = QSlider(Qt.Horizontal)
            slideBar.setObjectName(f"terAttrSlider{pri}-{sec}-{i}-{pos}")
            attrLayout.addWidget(valueLabel)
            attrLayout.addWidget(slideBar)
        return attrGroupBox

    def onLabelSwitched(self, index: int):
        print(f"Working image label switched to groupbox {index}")
        self.selectedImgNum = index - 1
        # the corresponding GroupBox to blue and the other groupboxes to grey
        if index == 1:
            self.ui.imageLabel1.toolIndex = self.selectedToolNum  # Sync the tool selection
            self.ui.imageLabel1.isSelected = True
            self.ui.imageLabel2.isSelected = False
            self.ui.image1GroupBox.setStyleSheet("QGroupBox {border: 3px solid blue;}")
            self.ui.image2GroupBox.setStyleSheet("")
        elif index == 2:
            self.ui.imageLabel1.toolIndex = self.selectedToolNum
            self.ui.imageLabel1.isSelected = False
            self.ui.imageLabel2.isSelected = True
            self.ui.image1GroupBox.setStyleSheet("")
            self.ui.image2GroupBox.setStyleSheet("QGroupBox {border: 3px solid blue;}")

    def onToolBtnClicked(self, clickedBtnID, selectedImageLb: scalableImageLabel):
        selectedImageLb.runWhenToolReleased()
        if clickedBtnID != 5:
            selectedImageLb.toolIndex = self.selectedToolNum = clickedBtnID
        else:
            selectedImageLb.toolIndex = self.selectedToolNum = -1
        selectedImageLb.runWhenToolSelected()

    def onToolBtnReleased(self, selectedImageLb: scalableImageLabel):
        # selectedImageLb.toolIndex = -1
        # selectedImageLb.runWhenToolReleased()
        pass

    def open(self, imageLabel):
        self.imgName, imgType = QFileDialog.getOpenFileName(imageLabel, "????????????", self.Path,
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
