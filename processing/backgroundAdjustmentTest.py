import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
import cv2
from PyQt5.QtGui import QImage, QPixmap

RGB_BACKGROUND_COLOR = (233, 219, 193)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")

        # Add the text label for the color bar
        self.color_label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)  # Set the font to bold
        self.color_label.setFont(font)
        self.color_label.setAlignment(QtCore.Qt.AlignCenter)
        self.color_label.setObjectName("color_label")
        self.color_label.setText("Standard Color")  # Set the text of the label

        # Add the color label to the vertical layout
        self.verticalLayout.addWidget(self.color_label)
        # Add a QFrame widget for the color bar
        self.color_bar = QtWidgets.QFrame(self.centralwidget)
        self.color_bar.setObjectName("color_bar")
        self.color_bar.setFixedHeight(10)  # Set the height of the color bar
        self.color_bar.setStyleSheet(f"background-color: rgb{RGB_BACKGROUND_COLOR};")  # Set the background color

        # Add the color bar to the vertical layout
        self.verticalLayout.addWidget(self.color_bar)

        # Add the image label widget
        self.image_label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.image_label.sizePolicy().hasHeightForWidth())
        self.image_label.setSizePolicy(sizePolicy)
        self.image_label.setText("")
        self.image_label.setObjectName("image_label")
        self.verticalLayout.addWidget(self.image_label)

        # Add the reset button widget
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
        self.original_image = cv2.imread('../input/painting1.jpg')
        if self.original_image is None:
            print('Failed to read image file')
            # 退出程序或进行其他错误处理操作
        else:
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

        # Check if clicked position is within image boundaries
        if x < 0 or x >= self.image.shape[1] or y < 0 or y >= self.image.shape[0]:
            return

        bgr_color = self.image[y, x]
        print('BGR color: ', bgr_color)
        hsv_color = cv2.cvtColor(bgr_color.reshape(1, 1, 3), cv2.COLOR_BGR2HSV).flatten()
        print('HSV color: ', hsv_color)
        self.adjust_color(hsv_color)

    # Calculates and adds the difference between the selected background color and image in HSV color space to each channel
    def adjust_color(self, hsv_color, background_color=RGB_BACKGROUND_COLOR):
        hsv_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)  # Convert image to hsv
        h, s, v = hsv_image[:, :, 0], hsv_image[:, :, 1], hsv_image[:, :, 2]  # Split channels
        if isinstance(background_color, tuple):  # RGB format
            background_color = cv2.cvtColor(np.array([[background_color]], dtype=np.uint8), cv2.COLOR_RGB2HSV)[0, 0]
        h += int(hsv_color[0] - background_color[0])  # Adjust hue
        s += int(hsv_color[1] - background_color[1])  # Adjust saturation
        v += int(hsv_color[2] - background_color[2])  # Adjust value
        hsv_image = cv2.merge([h, s, v])  # Merge channels
        self.image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)  # Convert image back to bgr
        self.display_image()


app = QtWidgets.QApplication([])
window = MainWindow()
window.show()
app.exec_()
