from PyQt5 import QtCore, QtGui, QtWidgets
import cv2
from PyQt5.QtGui import QImage, QPixmap


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.image_label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.image_label.sizePolicy().hasHeightForWidth())
        self.image_label.setSizePolicy(sizePolicy)
        self.image_label.setText("")
        self.image_label.setObjectName("image_label")
        self.verticalLayout.addWidget(self.image_label)
        self.reset_button = QtWidgets.QPushButton(self.centralwidget)
        self.reset_button.setObjectName("reset_button")
        self.verticalLayout.addWidget(self.reset_button)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.reset_button.setText(_translate("MainWindow", "Reset"))


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.reset_button.clicked.connect(self.reset_image)
        self.original_image = cv2.imread('./input/painting1.jpg')
        self.image = self.original_image.copy()
        self.display_image()
        self.image_label.mousePressEvent = self.get_color

    def display_image(self):  # Display image from opencv in pyqt
        rgb_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qimage = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)
        self.image_label.setPixmap(pixmap)

    def reset_image(self):  # Reset image to original
        self.image = self.original_image.copy()
        self.display_image()

    def get_color(self, event):  # Get color from clicked position
        x = event.pos().x()
        y = event.pos().y()
        bgr_color = self.image[y, x]
        hsv_color = cv2.cvtColor(bgr_color.reshape(1, 1, 3), cv2.COLOR_BGR2HSV).flatten()
        self.adjust_color(hsv_color)

    # Calculates and adds the difference between the selected background color and image in HSV color space to each channel
    def adjust_color(self, hsv_color):
        hsv_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)  # Convert image to hsv
        h, s, v = hsv_image[:, :, 0], hsv_image[:, :, 1], hsv_image[:, :, 2]  # Split channels
        h += int(hsv_color[0] - h.mean())  # Adjust hue
        s += int(hsv_color[1] - s.mean())  # Adjust saturation
        v += int(hsv_color[2] - v.mean())  # Adjust value
        hsv_image = cv2.merge([h, s, v])  # Merge channels
        self.image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)  # Convert image back to bgr
        self.display_image()


app = QtWidgets.QApplication([])
window = MainWindow()
window.show()
app.exec_()
