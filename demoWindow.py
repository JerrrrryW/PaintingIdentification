from PyQt5.QtWidgets import QApplication, QMessageBox, QFileDialog, QGridLayout
from PyQt5.QtGui import QPainter, QPixmap, QIcon
from PyQt5 import uic, QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt, QPoint
# from plot2 import Ui_MainWindow  # 这里的plot2是通过plot2.ui转成的plot2.py文件
import sys
import os
from scalableImageLabel import scalableImageLabel


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)
        self.btnArray1 = [self.floodFillBtn1, self.sqareCutBtn1, self.freeCutBtn1, self.sensorBtn1]
        self.btnArray2 = [self.floodFillBtn2, self.sqareCutBtn2, self.freeCutBtn2, self.sensorBtn2]
        self.initClickedBtnConnection()
        self.Path = os.getcwd()

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

    def ToolBtnClicked(self, clickedBtn: QtWidgets.QToolButton, btnArray):
        # self.floodFillBtn1.setCheckable(True)
        if clickedBtn.isChecked() is True:
            print(clickedBtn.objectName(), "is clicked and checked!")
            for i, btn in enumerate(btnArray):
                if btn is not clickedBtn:
                    btn.setEnabled(False)
        else:
            print(clickedBtn.objectName(), "is clicked and unchecked!")
            for i, btn in enumerate(btnArray):
                if btn is not clickedBtn:
                    btn.setEnabled(True)

    def initClickedBtnConnection(self):
        self.selectBtn1.clicked.connect(lambda: self.open(self.imageLabel1))
        self.selectBtn2.clicked.connect(lambda: self.open(self.imageLabel2))
        self.floodFillBtn1.clicked.connect(
            lambda: self.ToolBtnClicked(clickedBtn=self.floodFillBtn1, btnArray=self.btnArray1))
        self.sqareCutBtn1.clicked.connect(
            lambda: self.ToolBtnClicked(clickedBtn=self.sqareCutBtn1, btnArray=self.btnArray1))
        self.freeCutBtn1.clicked.connect(
            lambda: self.ToolBtnClicked(clickedBtn=self.freeCutBtn1, btnArray=self.btnArray1))
        self.sensorBtn1.clicked.connect(
            lambda: self.ToolBtnClicked(clickedBtn=self.sensorBtn1, btnArray=self.btnArray1))
        self.floodFillBtn2.clicked.connect(
            lambda: self.ToolBtnClicked(clickedBtn=self.floodFillBtn2, btnArray=self.btnArray2))
        self.sqareCutBtn2.clicked.connect(
            lambda: self.ToolBtnClicked(clickedBtn=self.sqareCutBtn2, btnArray=self.btnArray2))
        self.freeCutBtn2.clicked.connect(
            lambda: self.ToolBtnClicked(clickedBtn=self.freeCutBtn2, btnArray=self.btnArray2))
        self.sensorBtn2.clicked.connect(
            lambda: self.ToolBtnClicked(clickedBtn=self.sensorBtn2, btnArray=self.btnArray2))

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1600, 900)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout.setContentsMargins(-1, -1, 1000, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.selectBtn1 = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.selectBtn1.sizePolicy().hasHeightForWidth())
        self.selectBtn1.setSizePolicy(sizePolicy)
        self.selectBtn1.setObjectName("selectBtn1")
        self.horizontalLayout.addWidget(self.selectBtn1)
        self.selectBtn2 = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.selectBtn2.sizePolicy().hasHeightForWidth())
        self.selectBtn2.setSizePolicy(sizePolicy)
        self.selectBtn2.setObjectName("selectBtn2")
        self.horizontalLayout.addWidget(self.selectBtn2)
        self.saveBtn = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.saveBtn.sizePolicy().hasHeightForWidth())
        self.saveBtn.setSizePolicy(sizePolicy)
        self.saveBtn.setObjectName("saveBtn")
        self.horizontalLayout.addWidget(self.saveBtn)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.verticalLayout.setObjectName("verticalLayout")
        self.floodFillBtn1 = QtWidgets.QToolButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.floodFillBtn1.sizePolicy().hasHeightForWidth())
        self.floodFillBtn1.setSizePolicy(sizePolicy)
        self.floodFillBtn1.setCheckable(True)
        self.floodFillBtn1.setMinimumSize(QtCore.QSize(40, 40))
        self.floodFillBtn1.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.floodFillBtn1.setIcon(QIcon(QPixmap("icon/magic_wand.png")))
        self.floodFillBtn1.setObjectName("floodFillBtn1")
        self.verticalLayout.addWidget(self.floodFillBtn1)
        self.sqareCutBtn1 = QtWidgets.QToolButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sqareCutBtn1.sizePolicy().hasHeightForWidth())
        self.sqareCutBtn1.setSizePolicy(sizePolicy)
        self.sqareCutBtn1.setMinimumSize(QtCore.QSize(40, 40))
        self.sqareCutBtn1.setObjectName("sqareCutBtn1")
        self.sqareCutBtn1.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.sqareCutBtn1.setIcon(QIcon(QPixmap("icon/square.png")))
        self.sqareCutBtn1.setCheckable(True)
        self.verticalLayout.addWidget(self.sqareCutBtn1)
        self.freeCutBtn1 = QtWidgets.QToolButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.freeCutBtn1.sizePolicy().hasHeightForWidth())
        self.freeCutBtn1.setSizePolicy(sizePolicy)
        self.freeCutBtn1.setMinimumSize(QtCore.QSize(40, 40))
        self.freeCutBtn1.setObjectName("freeCutBtn1")
        self.freeCutBtn1.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.freeCutBtn1.setIcon(QIcon(QPixmap("icon/free_select.png")))
        self.freeCutBtn1.setCheckable(True)
        self.verticalLayout.addWidget(self.freeCutBtn1)
        self.sensorBtn1 = QtWidgets.QToolButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sensorBtn1.sizePolicy().hasHeightForWidth())
        self.sensorBtn1.setSizePolicy(sizePolicy)
        self.sensorBtn1.setMinimumSize(QtCore.QSize(40, 40))
        self.sensorBtn1.setObjectName("sensorBtn1")
        self.sensorBtn1.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.sensorBtn1.setIcon(QIcon(QPixmap("icon/sensor.png")))
        self.sensorBtn1.setCheckable(True)
        self.verticalLayout.addWidget(self.sensorBtn1)
        self.horizontalLayout_4.addLayout(self.verticalLayout)
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setObjectName("groupBox_3")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.imageLabel1 = scalableImageLabel(self.groupBox_3)
        # self.imageLabel1.setMaximumSize(QtCore.QSize(471, 539))
        self.imageLabel1.setScaledContents(False)
        self.imageLabel1.setAlignment(QtCore.Qt.AlignCenter)
        self.imageLabel1.setObjectName("imageLabel1")
        self.horizontalLayout_5.addWidget(self.imageLabel1)
        self.horizontalLayout_4.addWidget(self.groupBox_3)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.floodFillBtn2 = QtWidgets.QToolButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.floodFillBtn2.sizePolicy().hasHeightForWidth())
        self.floodFillBtn2.setSizePolicy(sizePolicy)
        self.floodFillBtn2.setMinimumSize(QtCore.QSize(40, 40))
        self.floodFillBtn2.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.floodFillBtn2.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.floodFillBtn2.setIcon(QIcon(QPixmap("icon/magic_wand.png")))
        self.floodFillBtn2.setObjectName("floodFillBtn2")
        self.floodFillBtn2.setCheckable(True)
        self.verticalLayout_2.addWidget(self.floodFillBtn2)
        self.sqareCutBtn2 = QtWidgets.QToolButton(self.centralwidget)
        self.sqareCutBtn2.setMinimumSize(QtCore.QSize(40, 40))
        self.sqareCutBtn2.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.sqareCutBtn2.setIcon(QIcon(QPixmap("icon/square.png")))
        self.sqareCutBtn2.setObjectName("sqareCutBtn2")
        self.sqareCutBtn2.setCheckable(True)
        self.verticalLayout_2.addWidget(self.sqareCutBtn2)
        self.freeCutBtn2 = QtWidgets.QToolButton(self.centralwidget)
        self.freeCutBtn2.setMinimumSize(QtCore.QSize(40, 40))
        self.freeCutBtn2.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.freeCutBtn2.setIcon(QIcon(QPixmap("icon/free_select.png")))
        self.freeCutBtn2.setObjectName("freeCutBtn2")
        self.freeCutBtn2.setCheckable(True)
        self.verticalLayout_2.addWidget(self.freeCutBtn2)
        self.sensorBtn2 = QtWidgets.QToolButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sensorBtn2.sizePolicy().hasHeightForWidth())
        self.sensorBtn2.setSizePolicy(sizePolicy)
        self.sensorBtn2.setMinimumSize(QtCore.QSize(40, 40))
        self.sensorBtn2.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.sensorBtn2.setIcon(QIcon(QPixmap("icon/sensor.png")))
        self.sensorBtn2.setObjectName("sensorBtn2")
        self.sensorBtn2.setCheckable(True)
        self.verticalLayout_2.addWidget(self.sensorBtn2)
        self.horizontalLayout_4.addLayout(self.verticalLayout_2)
        self.groupBox_4 = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_4.sizePolicy().hasHeightForWidth())
        self.groupBox_4.setSizePolicy(sizePolicy)
        self.groupBox_4.setObjectName("groupBox_4")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.groupBox_4)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.imageLabel2 = scalableImageLabel(self.groupBox_4)
        # self.imageLabel2.setMaximumSize(QtCore.QSize(471, 539))
        self.imageLabel2.setScaledContents(False)
        self.imageLabel2.setAlignment(QtCore.Qt.AlignCenter)
        self.imageLabel2.setObjectName("imageLabel2")
        self.horizontalLayout_6.addWidget(self.imageLabel2)
        self.horizontalLayout_4.addWidget(self.groupBox_4)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.resultImage1 = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.resultImage1.sizePolicy().hasHeightForWidth())
        self.resultImage1.setSizePolicy(sizePolicy)
        self.resultImage1.setMaximumSize(QtCore.QSize(471, 539))
        self.resultImage1.setScaledContents(False)
        self.resultImage1.setAlignment(QtCore.Qt.AlignCenter)
        self.resultImage1.setObjectName("resultImage1")
        self.horizontalLayout_2.addWidget(self.resultImage1)
        self.verticalLayout_3.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.resultImage2 = QtWidgets.QLabel(self.groupBox_2)
        self.resultImage2.setMaximumSize(QtCore.QSize(471, 539))
        self.resultImage2.setScaledContents(False)
        self.resultImage2.setAlignment(QtCore.Qt.AlignCenter)
        self.resultImage2.setObjectName("resultImage2")
        self.horizontalLayout_3.addWidget(self.resultImage2)
        self.verticalLayout_3.addWidget(self.groupBox_2)
        self.horizontalLayout_4.addLayout(self.verticalLayout_3)
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "魔棒效果demo"))
        self.selectBtn1.setText(_translate("MainWindow", "Select Image1"))
        self.selectBtn2.setText(_translate("MainWindow", "Select Image2"))
        self.saveBtn.setText(_translate("MainWindow", "Save Result"))
        self.floodFillBtn1.setText(_translate("MainWindow", "魔棒"))
        self.sqareCutBtn1.setText(_translate("MainWindow", "方形"))
        self.freeCutBtn1.setText(_translate("MainWindow", "自由"))
        self.sensorBtn1.setText(_translate("MainWindow", "检测"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Compared Image 1"))
        self.imageLabel1.setText(_translate("MainWindow", "Origin Image Here"))
        self.floodFillBtn2.setText(_translate("MainWindow", "魔棒"))
        self.sqareCutBtn2.setText(_translate("MainWindow", "方形"))
        self.freeCutBtn2.setText(_translate("MainWindow", "自由"))
        self.sensorBtn2.setText(_translate("MainWindow", "检测"))
        self.groupBox_4.setTitle(_translate("MainWindow", "Compared Image 2"))
        self.imageLabel2.setText(_translate("MainWindow", "Compared Image Here"))
        self.groupBox.setTitle(_translate("MainWindow", "Result 1"))
        self.resultImage1.setText(_translate("MainWindow", "Origin Image Result"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Result 2"))
        self.resultImage2.setText(_translate("MainWindow", "Compared Image Result"))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mywindow = MyWindow()
    mywindow.show()
    sys.exit(app.exec_())
