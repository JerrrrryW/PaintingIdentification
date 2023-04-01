import os
import random
import sys

import PyQt5.QtCore
from PyQt5 import uic
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from custom_classes.ClickableLabel import ClickableLabel
from custom_classes.ScalableImageLabel import scalableImageLabel, global_refresh_result_signal


class DemoWindow:

    def __init__(self):
        self.ui = uic.loadUi('QT_UI\\version3.ui')

        self.toolGroup = QButtonGroup()
        self.selectedImgNum = 1  # 0,1,2   0 means no img label selected
        self.selectedToolNum = -1  # -1,0,1,2,3   -1 means default moving mode
        self.selectedFeatureNum = 0  # 0,1,2..   0 means no feature selected
        self.featureItems = ["erode", "dilate", "open", "close", "gradient", "tophat", "blackhat"]  # sample

        self.initImageLabels()
        self.initToolBar()
        self.initClickedBtnConnection()
        self.initFeatureMenu()
        # self.initTabBar()

        self.originImages = [None, None]  # to store the origin images
        self.imageLabels = [self.ui.imageLabel1, self.ui.imageLabel2]  # to access the label faster
        self.originLabels = [self.ui.originImage1, self.ui.originImage2]  # to access the label faster
        self.stackedWidgets = [self.ui.processingStackedWidget, self.ui.visualizationStackedWidget,
                               self.ui.matchStackedWidget]
        self.stampLists = [self.ui.stampList1, self.ui.stampList2]

        self.onLabelSwitched(1)  # set default selected image label

        # # highlight the groupbox corresponding to the selected image label
        # global_refresh_result_signal.highlight_selected_box.connect(self.onLabelSwitched)
        # # show the processing result images on corresponding labels
        # global_refresh_result_signal.change_result_image.connect(self.refreshResultImage)

        self.Path = os.getcwd()

    def initImageLabels(self):
        # Load custom clickable origin image label
        originGroupBox1 = self.ui.originGroupBox1
        self.ui.originImage1 = ClickableLabel(originGroupBox1)
        self.ui.originImage1.setAlignment(QtCore.Qt.AlignCenter)
        self.ui.originImage1.setObjectName("originImage1")
        self.ui.originImgHLayout1 = QHBoxLayout()
        self.ui.originImgHLayout1.addWidget(self.ui.originImage1)
        originGroupBox1.setLayout(self.ui.originImgHLayout1)

        originGroupBox2 = self.ui.originGroupBox2
        self.ui.originImage2 = ClickableLabel(originGroupBox2)
        self.ui.originImage2.setAlignment(QtCore.Qt.AlignCenter)
        self.ui.originImage2.setObjectName("originImage2")
        self.ui.originImgHLayout2 = QHBoxLayout()
        self.ui.originImgHLayout2.addWidget(self.ui.originImage2)
        originGroupBox2.setLayout(self.ui.originImgHLayout2)

        # Load custom image label
        page1 = self.ui.processingPage1
        self.ui.imageLabel1 = scalableImageLabel(page1)
        self.ui.imageLabel1.setScaledContents(False)
        self.ui.imageLabel1.setAlignment(QtCore.Qt.AlignCenter)
        self.ui.imageLabel1.setObjectName("imageLabel1")
        self.ui.horizontalLayout_5 = QHBoxLayout()
        page1.setLayout(self.ui.horizontalLayout_5)
        self.ui.horizontalLayout_5.addWidget(self.ui.imageLabel1)

        page2 = self.ui.processingPage2
        self.ui.imageLabel2 = scalableImageLabel(page2)
        self.ui.imageLabel2.setScaledContents(False)
        self.ui.imageLabel2.setAlignment(QtCore.Qt.AlignCenter)
        self.ui.imageLabel2.setObjectName("imageLabel2")
        self.ui.horizontalLayout_6 = QHBoxLayout()
        page2.setLayout(self.ui.horizontalLayout_6)
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
        self.ui.selectBtn1.clicked.connect(lambda: self.openImgAndShow(1))
        self.ui.selectBtn2.clicked.connect(lambda: self.openImgAndShow(2))
        self.ui.resetBtn.clicked.connect(self.resetBtnClicked)

        self.toolGroup.buttonPressed[int].connect(lambda _:  # [int] 指定了信号传递的为触发的按钮id
                                                  self.onToolBtnClicked(_, self.imageLabels[self.selectedImgNum]))
        self.toolGroup.buttonReleased[int].connect(lambda:
                                                   self.onToolBtnReleased(self.imageLabels[self.selectedImgNum]))

        self.ui.originImage1.clicked.connect(lambda: self.onLabelSwitched(1))
        self.ui.originImage2.clicked.connect(lambda: self.onLabelSwitched(2))

        self.ui.stampBtn.clicked.connect(lambda: self.featureBtnClicked(2))
        # self.ui.stampBtn.release.connect(lambda: setattr(self, 'selectedFeatureNum', 0))  # reset the selected feature
        self.ui.inscriptionBtn.clicked.connect(lambda: self.featureBtnClicked(1))

    def initFeatureMenu(self):
        menu = QMenu(self.ui.featuresBtn)
        mapper = QSignalMapper(self.ui.featuresBtn)
        # 遍历列表创建下拉菜单项并绑定槽函数
        for i, item in enumerate(self.featureItems):
            action = menu.addAction(item)
            mapper.setMapping(action, i+3)
            action.triggered.connect(mapper.map)
        mapper.mapped[int].connect(self.featureBtnClicked)
        self.ui.featuresBtn.setMenu(menu)

    def initStampList(self, listWidget: QListWidget):
        listWidget.clear()
        listWidget.setEnabled(True)
        listWidget.setFlow(QListWidget.TopToBottom)
        listWidget.setResizeMode(QListWidget.Adjust)
        # listWidget.setStyleSheet("background-color:transparent")
        for i in range(10):
            item = QListWidgetItem(listWidget)
            stampListUi = uic.loadUi('QT_UI\\stampListItem.ui')
            item.setSizeHint(QtCore.QSize(listWidget.width(), int(listWidget.height() / 4)))

            # generate a sample stamp info TODO: link the dataset here
            stampImg = QPixmap('input\\painting2_stamp.jpg')  # .scaled(stampListUi.stampImgLabel.size(), QtCore.Qt.KeepAspectRatio)
            stampListUi.stampImgLabel.setPixmap(stampImg)
            sourceImg = QPixmap('input\\painting2.jpg')  # .scaled(stampListUi.sourceImgLabel.size(), QtCore.Qt.KeepAspectRatio)
            stampListUi.sourceImgLabel.setPixmap(sourceImg)
            stampListUi.titleLabel.setText("Title " + str(i+1))
            ranPercent = random.randint(0, 100)
            stampListUi.percentage.setText(str(ranPercent) + "%")
            stampListUi.percentageBar.setValue(ranPercent)

            listWidget.setItemWidget(item, stampListUi)

    def featureBtnClicked(self, featureNum: int):
        self.selectedFeatureNum = featureNum
        print(f"feature button clicked:{featureNum}")
        if featureNum == 2:
            self.initStampList(self.stampLists[self.selectedImgNum - 1])
        self.ui.matchStackedWidget.setCurrentIndex(2 * (self.selectedImgNum - 1) + self.selectedFeatureNum - 1)  # switch to stamp list page of the selected image

    def resetBtnClicked(self):
        imageLabel = self.imageLabels[self.selectedImgNum]
        # Scale the image to fit within the size of imageLabel
        if self.originImages[self.selectedImgNum] is not None:
            scaled_jpg = self.originImages[self.selectedImgNum].scaled(imageLabel.size(),
                                                                       QtCore.Qt.KeepAspectRatio,
                                                                       QtCore.Qt.SmoothTransformation)
            print("scaled:", scaled_jpg.width(), scaled_jpg.height())
            imageLabel.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
            imageLabel.setPixmap(scaled_jpg)
        else:
            self.showToastMessage("Please select an image first!")

        # Reset the tool selection
        self.toolGroup.setExclusive(False)
        self.toolGroup.setExclusive(True)
        self.ui.moveBtn.setChecked(True)

    def onLabelSwitched(self, index: int):
        print(f"Working image label switched to groupbox {index}")
        self.selectedImgNum = index
        for sw in self.stackedWidgets:
            if sw is not self.ui.matchStackedWidget:
                sw.setCurrentIndex(index - 1)
            else:
                sw.setCurrentIndex(2 * (index - 1) + self.selectedFeatureNum - 1)  # switch to the corresponding feature page
        # the corresponding GroupBox to blue and the other groupboxes to grey
        if index == 1:
            self.ui.imageLabel1.toolIndex = self.selectedToolNum  # Sync the tool selection
            self.ui.imageLabel1.isSelected = True
            self.ui.imageLabel2.isSelected = False
            self.ui.originGroupBox1.setStyleSheet("QGroupBox {border: 3px solid blue;}")
            self.ui.originGroupBox2.setStyleSheet("")
        elif index == 2:
            self.ui.imageLabel1.toolIndex = self.selectedToolNum
            self.ui.imageLabel1.isSelected = False
            self.ui.imageLabel2.isSelected = True
            self.ui.originGroupBox1.setStyleSheet("")
            self.ui.originGroupBox2.setStyleSheet("QGroupBox {border: 3px solid blue;}")

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

    def openImgAndShow(self, imageIndex: int):
        originLabel = self.originLabels[imageIndex - 1]
        processingLabel = self.imageLabels[imageIndex - 1]
        imgName, imgType = QFileDialog.getOpenFileName(originLabel, "打开图片", self.Path,
                                                       "*.jpg;;*.png;;All Files(*)")
        original_jpg = QPixmap(imgName)
        self.originImages[imageIndex - 1] = original_jpg
        print("origin:", original_jpg.width(), original_jpg.height())
        print("label:", originLabel.width(), originLabel.height())

        # Scale the image to fit within the size of originLabel
        scaled_jpg = original_jpg.scaled(originLabel.size(), QtCore.Qt.KeepAspectRatio)

        print("scaled:", scaled_jpg.width(), scaled_jpg.height())

        if not scaled_jpg.isNull():
            originLabel.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
            originLabel.setPixmap(scaled_jpg)
            processingLabel.setPixmap(original_jpg)

    def refreshResultImage(self, resultImg: QPixmap, labelNum):
        if labelNum == 1:
            self.ui.imageLabel1.setPixmap(resultImg)
        elif labelNum == 2:
            self.ui.imageLabel2.setPixmap(resultImg)

    def showToastMessage(self, message: str):
        msgBox = QMessageBox(parent=self.ui)
        msgBox.setText(message)
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.show()

    # def initTabBar(self):  # Tri-layer attributes tab bar on the right side
    #     primaryTabs = ["形状", "墨色", "笔法", "纹理"]
    #     secondaryTabs = [["轮廓", "结构"],  # 形状的二级指标
    #                      ["色调", "层次"],  # 墨色的二级指标
    #                      ["力量", "技巧"],  # 笔法的二级指标
    #                      ["材质", "效果"]]  # 纹理的二级指标
    #     tertiaryTabs = [[["线宽", "线锋", "线形"],  # 轮廓的三级指标
    #                      ["位置", "大小", "比例", "方向"]],  # 结构的三级指标
    #                     [["明度", "色温", "饱和度"],  # 色调的三级指标
    #                      ["变化度", "过渡度", "对比度"]],  # 层次的三级指标
    #                     [["压力", "弹性", "速度"],  # 力量的三级指标
    #                      ["熟练度", "灵活度", "变化度"]],  # 技巧的三级指标
    #                     [["类型", "质地", "吸墨性"],  # 材质的三级指标
    #                      ["光泽度", "透明度", "模糊度"]]]  # 效果的三级指标
    #
    #     self.ui.secTabStack.removeWidget(self.ui.secPage1)
    #     self.ui.terAttrStack.removeWidget(self.ui.terPage1)
    #     for i in range(len(primaryTabs)):  # retrieve the tabs
    #         self.ui.primaryTabBar.addItem(primaryTabs[i])  # fill primary indicators in listview
    #         # create pages dynamically to secondaryTabStack
    #         secPage = QtWidgets.QWidget()
    #         secPage.setObjectName(f"secondaryTabPage{i}")
    #         secLayout = QtWidgets.QHBoxLayout(secPage)
    #
    #         listview = QtWidgets.QListWidget()
    #         for j in range(len(secondaryTabs[i])):
    #             listview.addItem(secondaryTabs[i][j])
    #             # init terAttrPage in stackedWidget
    #             terPage = QtWidgets.QWidget()
    #             terPage.setObjectName(f"tertiaryAttrPage{i}-{j}")
    #             terLayout = QtWidgets.QVBoxLayout(terPage)
    #             terLayout.addWidget(self.createTertiaryAttributesGroupBox(tertiaryTabs[i][j], i, j, 1))
    #             terLayout.addWidget(self.createTertiaryAttributesGroupBox(tertiaryTabs[i][j], i, j, 2))
    #             self.ui.terAttrStack.addWidget(terPage)
    #         secLayout.addWidget(listview)
    #         listview.currentRowChanged.connect(self.on_row_changed(i))
    #
    #         self.ui.secTabStack.addWidget(secPage)
    #     self.ui.primaryTabBar.currentRowChanged.connect(self.ui.secTabStack.setCurrentIndex)

    # def createTertiaryAttributesGroupBox(self, terAttrList: [], pri, sec, pos):  # pri&sec is the parentTab num, pos means up1/down2 image
    #     attrGroupBox = QGroupBox()
    #     attrGroupBox.setTitle("Attributes")
    #     attrLayout = QVBoxLayout(attrGroupBox)
    #     for i in range(len(terAttrList)):
    #         attrLayout.addWidget(QLabel(terAttrList[i] + ": "))
    #         valueLabel = QLabel("0")
    #         valueLabel.setObjectName(f"terAttrValue{pri}-{sec}-{i}-{pos}")  # to assure objectName is unique
    #         slideBar = QSlider(Qt.Horizontal)
    #         slideBar.setObjectName(f"terAttrSlider{pri}-{sec}-{i}-{pos}")
    #         attrLayout.addWidget(valueLabel)
    #         attrLayout.addWidget(slideBar)
    #     return attrGroupBox


if __name__ == '__main__':
    app = QApplication([])
    demoWindow = DemoWindow()
    demoWindow.ui.show()
    app.exec_()
