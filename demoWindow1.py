import os
import random
import sys
from functools import partial

import PyQt5.QtCore
import cv2
from PyQt5 import uic, QtCore, QtWebEngineWidgets

from PyQt5.QtCore import Qt, QSignalMapper, QUrl
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QLabel, QHBoxLayout, QWidget, QFrame, QButtonGroup, QMenu, \
    QFileDialog, QMessageBox, QApplication

from qt_material import apply_stylesheet

from custom_classes.ClickableLabel import ClickableLabel
from custom_classes.ScalableImageLabel import scalableImageLabel, global_refresh_result_signal
from custom_classes.featureSliderWidget import featureSliderWidget, grobal_update_processed_result
from echarts.relativeGraphTest import initPyQtGraph, initGraph
from database.sqlSelector import findRelativeEntities, convert_to_nodes_and_links, findImgAndInfo
from processing.feature.erode import erode
from processing.feature.inkColor import multi_threshold_processing
from processing.feature.paintingColor import extract_color
from processing.feature.strength import sharpen_image


def initFeatureList(listWidget: QListWidget, featureIndicator):
    listWidget.clear()
    listWidget.setEnabled(True)
    listWidget.setFlow(QListWidget.TopToBottom)
    listWidget.setResizeMode(QListWidget.Adjust)
    for key in featureIndicator['params']:
        item = QListWidgetItem(listWidget)
        item.setSizeHint(
            QtCore.QSize(listWidget.width() - 20, int((listWidget.height() - 10) / len(featureIndicator['params']))))
        itemWidget = featureSliderWidget(featureIndicator['params'][key]['name'],
                                         featureIndicator['params'][key]['min'],
                                         featureIndicator['params'][key]['max'],
                                         featureIndicator['params'][key]['initial'])
        listWidget.setItemWidget(item, itemWidget)


def initStampList(listWidget: QListWidget):
    listWidget.clear()
    listWidget.setEnabled(True)
    listWidget.setFlow(QListWidget.TopToBottom)
    listWidget.setResizeMode(QListWidget.Adjust)
    # listWidget.setStyleSheet("background-color:transparent")
    for i in range(10):
        item = QListWidgetItem(listWidget)
        stampListUi = uic.loadUi('QT_UI\\stampListItem.ui')
        item.setSizeHint(QtCore.QSize(listWidget.width() - 20, int((listWidget.height() - 10) / 4)))

        # generate a sample stamp info TODO: link the dataset here
        stampImg = QPixmap(
            'input\\painting2_stamp.jpg')  # .scaled(stampListUi.stampImgLabel.size(), QtCore.Qt.KeepAspectRatio)
        stampListUi.stampImgLabel.setPixmap(stampImg)
        sourceImg = QPixmap(
            'input\\painting2.jpg')  # .scaled(stampListUi.sourceImgLabel.size(), QtCore.Qt.KeepAspectRatio)
        stampListUi.sourceImgLabel.setPixmap(sourceImg)
        stampListUi.titleLabel.setText("Title " + str(i + 1))
        ranPercent = random.randint(0, 100)
        stampListUi.percentage.setText(str(ranPercent) + "%")
        stampListUi.percentageBar.setValue(ranPercent)

        listWidget.setItemWidget(item, stampListUi)

def convertCv2ToQImage(cv2_img):
    height, width, channel = cv2_img.shape
    bytes_per_line = 3 * width
    qimage = QImage(cv2_img.data, width, height, bytes_per_line, QImage.Format_RGB888)
    return qimage


def updateProcessingResult(parameter,
                           value):  # dynamic update the processing result when the slider value changed
    print(f"{parameter} value changed to {value}")
    if parameter == "erode":
        pass

def refreshDetailBox(relatedImgLb: QLabel, relatedInfoLb: QLabel, queryid: str):
    relatedView, relatedInfo = findImgAndInfo(queryid)
    if isinstance(relatedView, str):
        relatedImgLb.setText(relatedView)
    elif isinstance(relatedView, QPixmap):
        relatedImgLb.setPixmap(relatedView)
    else:
        relatedImgLb.setText('索引')
    relatedInfoLb.setText(relatedInfo)


class DemoWindow:

    def __init__(self):
        self.ui = uic.loadUi('QT_UI\\version3.ui')

        self.toolGroup = QButtonGroup()
        self.selectedImgNum = -1  # -1,0,1   -1 means no img label selected
        self.selectedToolNum = -1  # -1,0,1,2,3   -1 means default moving mode
        self.selectedFeatureNum = 0  # 0,1...  0 means default page1

        self.initImageLabels()
        self.initToolBar()
        self.initClickedBtnConnection()
        self.initFeatureMenu()
        refreshDetailBox(self.ui.relatedImgLb, self.ui.relatedInfoLb, 'P468')
        # self.initTabBar()

        self.originImages = [None, None]  # to store the origin images
        self.fragmentsLists = [self.ui.fragmentsList1, self.ui.fragmentsList2]  # to store the segmented fragments in visualization box
        self.imageLabels = [self.ui.imageLabel1, self.ui.imageLabel2]  # to access the label faster
        self.originLabels = [self.ui.originImage1, self.ui.originImage2]  # to access the label faster
        self.stackedWidgets = [self.ui.processingStackedWidget, self.ui.visualizationStackedWidget,
                               self.ui.matchStackedWidget]
        self.stampLists = [self.ui.stampList1, self.ui.stampList2]
        self.visualLabels = [self.ui.visualLabel1, self.ui.visualLabel2]
        self.paramLists = [self.ui.paramList1, self.ui.paramList2]
        self.webViewLists = [self.ui.webEngineView1, self.ui.webEngineView2]

        self.onLabelSwitched(1)  # set default selected image label
        self.fragmentsLists[0].setVisible(False)
        self.fragmentsLists[1].setVisible(False)
        self.segmented_fragments = []

        # refresh the toolbar when signal received
        global_refresh_result_signal.refresh_tool_bar.connect(self.resetToolBar)
        # refresh the result when signal received
        grobal_update_processed_result.update_processed_result.connect(self.updateProcessedResultByFeature)

        self.Path = os.getcwd()

    ''' 
    Initialization of features
    '''

    def initFeatureMenu(self):
        self.featureItems = {  # to store the feature items
            2: {'name': '力度（笔画）',
                'params': {
                    'kernel_size_num': {'name': 'kernel size', 'min': 1, 'max': 10, 'initial': 3},
                    'num_iterations': {'name': 'color iterations', 'min': 2, 'max': 50, 'initial': 12},
                }
            },
            3: {'name': '墨色',
                'params': {
                    'num_thresholds': {'name': 'Number of Thresholds', 'min': 2, 'max': 10, 'initial': 3},
                    'min_threshold': {'name': 'Minimum Threshold', 'min': 0, 'max': 255, 'initial': 0},
                    'max_threshold': {'name': 'Maximum Threshold', 'min': 0, 'max': 255, 'initial': 255},
                }
            },
            4: {'name': '力度（全局）',
                'params': {
                    'alpha': {'name': 'sharp degree', 'min': 1, 'max': 30, 'initial': 10},
                }
            },
            5: {'name': '画色',
                'params': {
                    'tolerance': {'name': 'Color Tolerance', 'min': 1, 'max': 50, 'initial': 10},
                    'limit_number': {'name': 'Number of Colors', 'min': 1, 'max': 20, 'initial': 10},
                }
            }

        }

        menu = QMenu(self.ui.featuresBtn)
        mapper = QSignalMapper(self.ui.featuresBtn)
        # 遍历列表创建下拉菜单项并绑定槽函数
        for key in self.featureItems.keys():
            action = menu.addAction(self.featureItems[key]['name'])
            mapper.setMapping(action, key)
            action.triggered.connect(mapper.map)
        mapper.mapped[int].connect(self.featureBtnClicked)
        self.ui.featuresBtn.setMenu(menu)

    def featureBtnClicked(self, featureNum: int):
        if self.originImages[self.selectedImgNum] is None:
            self.showToastMessage("Please select an image first!", title="NO IMAGE SELECTED")
            return
        self.selectedFeatureNum = featureNum
        print(f"feature button clicked:{featureNum}")

        imageLabel = self.imageLabels[self.selectedImgNum]
        image = imageLabel.scaledImg
        resultImage = None

        if featureNum == 0:  # OCR
            pass
        elif featureNum == 1:  # stamp
            initStampList(self.stampLists[self.selectedImgNum])
        elif featureNum == 2:  # erode
            initFeatureList(self.paramLists[self.selectedImgNum], self.featureItems[featureNum])
            resultImage = erode(image, has_background=imageLabel.hasBackground,
                                kernel_size_num=int(self.featureItems[featureNum]['params']['kernel_size_num']['initial']),
                                num_iterations=int(self.featureItems[featureNum]['params']['num_iterations']['initial']))
        elif featureNum == 3:  # ink color
            initFeatureList(self.paramLists[self.selectedImgNum], self.featureItems[featureNum])
            resultImage = multi_threshold_processing(image,
                                                     num_thresholds=int(self.featureItems[featureNum]['params']['num_thresholds']['initial']),
                                                     min_threshold=int(self.featureItems[featureNum]['params']['min_threshold']['initial']),
                                                     max_threshold=int(self.featureItems[featureNum]['params']['max_threshold']['initial']))
        elif featureNum == 4:  # global erode
            initFeatureList(self.paramLists[self.selectedImgNum], self.featureItems[featureNum])
            resultImage = sharpen_image(image, alpha=float(self.featureItems[featureNum]['params']['alpha']['initial']))
        elif featureNum == 5:  # extract color
            initFeatureList(self.paramLists[self.selectedImgNum], self.featureItems[featureNum])
            resultImage = extract_color(image,
                                        tolerance=int(self.featureItems[featureNum]['params']['tolerance']['initial']),
                                        limit_number=int(self.featureItems[featureNum]['params']['limit_number']['initial']))
        elif featureNum == 6:  # generate relationship network
            result = findRelativeEntities('Y95')
            nodes, links = convert_to_nodes_and_links(result)
            print('nodes:', nodes, '\nlinks:', links)
            width = self.webViewLists[self.selectedImgNum].width()
            height = self.webViewLists[self.selectedImgNum].height()
            renderred_graph_path = initGraph(nodes, links, [{"name": "绘画"}, {"name": "题款"}, {"name": "印鉴"}], width=width-20, height=height-20)
            # initPyQtGraph(nodes, links, [{"name": "painting"}, {"name": "inscription"}, {"name": "seal"}], self.webViewLists[self.selectedImgNum])
            self.webViewLists[self.selectedImgNum].load(QUrl('file:///' + renderred_graph_path))


        if resultImage is not None:
            self.visualLabels[self.selectedImgNum].setPixmap(resultImage)

        # switch to the corresponding page
        if featureNum <= 2:
            self.ui.matchStackedWidget.setCurrentIndex(
                4 * self.selectedImgNum + self.selectedFeatureNum)  # switch to stamp list page of the selected image
        elif featureNum == 6:
            self.ui.matchStackedWidget.setCurrentIndex(4 * self.selectedImgNum + 3)
        else:
            self.ui.matchStackedWidget.setCurrentIndex(4 * self.selectedImgNum + 2)  # all features use the same page

    def updateProcessedResultByFeature(self, featureName: str, featureValue: int):
        resultImg = None
        imageLabel = self.imageLabels[self.selectedImgNum]
        image = imageLabel.scaledImg
        if self.selectedFeatureNum == 2:
            item1 = self.paramLists[self.selectedImgNum].item(0)
            item2 = self.paramLists[self.selectedImgNum].item(1)
            resultImg = erode(image, has_background=imageLabel.hasBackground,
                              kernel_size_num=int(self.paramLists[self.selectedImgNum].itemWidget(item1).value_label.text()),
                              num_iterations=int(self.paramLists[self.selectedImgNum].itemWidget(item2).value_label.text()))

            if resultImg is not None:
                self.visualLabels[self.selectedImgNum].setPixmap(resultImg)
        elif self.selectedFeatureNum == 3:
            item1 = self.paramLists[self.selectedImgNum].item(0)
            item2 = self.paramLists[self.selectedImgNum].item(1)
            item3 = self.paramLists[self.selectedImgNum].item(2)
            resultImg = multi_threshold_processing(image,
                                                   num_thresholds=int(self.paramLists[self.selectedImgNum].itemWidget(item1).value_label.text()),
                                                   min_threshold=int(self.paramLists[self.selectedImgNum].itemWidget(item2).value_label.text()),
                                                   max_threshold=int(self.paramLists[self.selectedImgNum].itemWidget(item3).value_label.text()))
        elif self.selectedFeatureNum == 4:
            item1 = self.paramLists[self.selectedImgNum].item(0)
            resultImg = sharpen_image(image, alpha=float(self.paramLists[self.selectedImgNum].itemWidget(item1).value_label.text()))
        elif self.selectedFeatureNum == 5:
            item1 = self.paramLists[self.selectedImgNum].item(0)
            item2 = self.paramLists[self.selectedImgNum].item(1)
            resultImg = extract_color(image,
                                      tolerance=int(self.paramLists[self.selectedImgNum].itemWidget(item1).value_label.text()),
                                      limit_number=int(self.paramLists[self.selectedImgNum].itemWidget(item2).value_label.text()))

        if resultImg is not None:
            self.visualLabels[self.selectedImgNum].setPixmap(resultImg)

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
            self.showToastMessage("Please select an image first!", title="NO IMAGE SELECTED")

        # Reset the tool selection
        self.toolGroup.setExclusive(False)
        self.toolGroup.setExclusive(True)
        self.ui.moveBtn.setChecked(True)

        # Reset the visual label
        self.visualLabels[self.selectedImgNum].clear()
        self.visualLabels[self.selectedImgNum].setText("Visual Result " + str(self.selectedImgNum + 1))

    def onLabelSwitched(self, index: int):
        print(f"Working image label switched to groupbox {index}")
        self.selectedImgNum = index - 1
        for sw in self.stackedWidgets:
            if sw is not self.ui.matchStackedWidget:
                sw.setCurrentIndex(index - 1)
            else:
                sw.setCurrentIndex(
                    4 * (index - 1) + min(self.selectedFeatureNum, 2))  # switch to the corresponding feature page
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

    def resetToolBar(self):
        self.toolGroup.setExclusive(False)
        self.toolGroup.setExclusive(True)
        self.ui.moveBtn.setChecked(True)
        self.selectedToolNum = -1
        self.imageLabels[self.selectedImgNum].toolIndex = -1


    def onToolBtnClicked(self, clickedBtnID, selectedImageLb: scalableImageLabel):
        selectedImageLb.runWhenToolReleased()
        if clickedBtnID != 5:
            selectedImageLb.toolIndex = self.selectedToolNum = clickedBtnID
        else:
            selectedImageLb.toolIndex = self.selectedToolNum = -1
        selectedImageLb.runWhenToolSelected()
        if clickedBtnID == 2 or clickedBtnID == 4:  # reset tool bar after independent window return
            self.resetToolBar()

    def onToolBtnReleased(self, selectedImageLb: scalableImageLabel):
        # selectedImageLb.toolIndex = -1
        # selectedImageLb.runWhenToolReleased()
        pass

    def initFragmentsList(self, list_widget, image_list):
        # 设置列表的滚动模式为水平滚动
        list_widget.setFlow(QListWidget.LeftToRight)
        list_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        list_widget.setFrameShape(QFrame.NoFrame)

        # 创建水平布局
        layout = QHBoxLayout()
        layout.setSpacing(10)  # 设置项之间的空隙

        for i, img in enumerate(image_list):
            # 创建 QListWidgetItem
            item = QListWidgetItem(list_widget)

            # 创建 QLabel，并设置图像
            label = QLabel()
            qpixmap = QPixmap.fromImage(convertCv2ToQImage(img))
            label.setPixmap(qpixmap.scaledToHeight(100))
            label.setAlignment(Qt.AlignCenter)  # 图片居中显示

            # 将 QLabel 添加到 QListWidgetItem
            item.setSizeHint(label.sizeHint())
            list_widget.addItem(item)
            list_widget.setItemWidget(item, label)

        # 将布局设置为列表的布局
        list_widget.setLayout(layout)
        list_widget.itemDoubleClicked.connect(self.handleItemDoubleClicked)


    def openImgAndShow(self, imageIndex: int):
        originLabel = self.originLabels[imageIndex - 1]
        processingLabel = self.imageLabels[imageIndex - 1]
        fragmentsList = self.fragmentsLists[imageIndex - 1]
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

            for filename in os.listdir('segment_anything_gui/segmented_output'):
                if filename.endswith('.jpg') or filename.endswith('.png'):
                    self.segmented_fragments.append(cv2.cvtColor(cv2.imread('segment_anything_gui\\segmented_output\\' + filename), cv2.COLOR_BGR2RGB))
            # init fragments list
            self.initFragmentsList(fragmentsList, self.segmented_fragments)
            fragmentsList.setVisible(True)

    def handleItemDoubleClicked(self, item):
        index = self.fragmentsLists[self.selectedImgNum].row(item)
        if index < len(self.segmented_fragments):
            img = self.segmented_fragments[index]
            self.refreshResultImage(QPixmap.fromImage(convertCv2ToQImage(img)), self.selectedImgNum)

    def refreshResultImage(self, resultImg: QPixmap, labelNum):
        if labelNum == 0:
            self.ui.imageLabel1.setPixmap(resultImg)
        elif labelNum == 1:
            self.ui.imageLabel2.setPixmap(resultImg)

    def showToastMessage(self, message: str, title: str = "CAPAT"):
        msgBox = QMessageBox(parent=self.ui)
        msgBox.setWindowTitle(title)
        msgBox.setText(message)
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.show()

    '''
    initialization of the UI widgets
    '''

    def initImageLabels(self):  # load custom image processing labels
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
        self.toolGroup.addButton(self.ui.samBtn, 4)
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

        self.ui.inscriptionBtn.clicked.connect(lambda: self.featureBtnClicked(0))
        self.ui.stampBtn.clicked.connect(lambda: self.featureBtnClicked(1))
        self.ui.relativeNetworkBtn.clicked.connect(lambda: self.featureBtnClicked(6))
        # self.ui.stampBtn.release.connect(lambda: setattr(self, 'selectedFeatureNum', 0))  # reset the selected feature


if __name__ == '__main__':
    app = QApplication([])
    demoWindow = DemoWindow()

    extra = {
        'font_family': 'Arial',
        'font_size': 30,
    }
    apply_stylesheet(app, theme='light_amber.xml', invert_secondary=True, extra=extra)

    demoWindow.ui.show()
    app.exec_()
