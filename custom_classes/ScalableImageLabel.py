# -*- coding: utf-8 -*-
from threading import Thread

import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from custom_classes.CustomSignal import CustomSignal
from floodFill import floodFill, qtpixmap_to_cvimg, cvImg_to_qtImg
from pylivewire_master.gui import ImageWin
from processing.stamp import findStamp
from utils import drawOutRectgle, bgraImg_to_qtImg

global_refresh_result_signal = CustomSignal()


class scalableImageLabel(QtWidgets.QLabel):  # 不可用QMainWindow,因为QLabel继承自QWidget
    def __init__(self, parent=None):
        super(scalableImageLabel, self).__init__(parent)

        self.imgPixmap = QPixmap('input/painting2.jpg')  # 载入图片
        # self.scaledImg = self.imgPixmap.scaledToWidth(self.width())  # 初始化缩放图
        self.setText('SELECT A PAINTING TO PROCESS')
        self.scaledImg = self.imgPixmap
        self.singleOffset = QPoint(0, 0)  # 初始化偏移值

        self.isLeftPressed = bool(False)  # 图片被点住(鼠标左键)标志位
        self.isImgLabelArea = bool(True)  # 鼠标进入label图片显示区域
        self.toolIndex = -1  # 工具栏调用工具状态，0为当前未调用工具
        # self.isSelected = False
        self.rect = None  # rect的四个元素意义分别为：起点坐标x、y、x轴长度、y轴长度
        self.scaledImgTemp = None  # 用于存储临时缩放图
        self.floodFillResult = None  # 用于存储floodFill结果

    def floodFillThreadFunc(self, col, row, qPixmapImage: QPixmap, resultLabelNum):
        resultImg_bgra, oriImgMixed = floodFill(col, row, qPixmapImage)
        # global_refresh_result_signal.change_result_image.emit(resultImg, resultLabelNum)
        # show result image
        self.scaledImgTemp = self.scaledImg
        self.scaledImg = QPixmap(cvImg_to_qtImg(oriImgMixed))
        self.repaint()
        self.scaledImg = self.scaledImgTemp
        self.floodFillResult = QPixmap(bgraImg_to_qtImg(resultImg_bgra))

    def runWhenToolSelected(self):  # 当工具栏某一工具被选中时立刻执行
        if self.toolIndex == 0:  # floodFill
            pass

        elif self.toolIndex == 1:  # squareCut
            pass

        elif self.toolIndex == 2:  # freeCut
            self.freeCutWindow = ImageWin(self.scaledImg)
            self.freeCutWindow.setMouseTracking(True)
            self.freeCutWindow.setWindowTitle('Livewire Demo')
            self.freeCutWindow.exec_()
            # get result image from freeCutWindow and show it
            if self.freeCutWindow.cropped_image is not None:
                self.scaledImg = self.freeCutWindow.cropped_image
                self.imgPixmap = self.scaledImg
                self.repaint()

        elif self.toolIndex == 3:  # aiSensor
            self.scaledImgTemp = self.scaledImg
            self.scaledImg, self.cnts, self.stampSavedPath = findStamp(self.scaledImg)
            self.repaint()
            pass

    def runWhenToolReleased(self):  # 当工具栏选中的工具被释放时立刻执行
        if self.toolIndex == 0:  # floodFill
            self.scaledImg = self.floodFillResult  # 将floodFill结果显示在label上
            self.imgPixmap = self.scaledImg
            self.repaint()

        elif self.toolIndex == 1:  # squareCut
            if self.rect is not None and self.rect[2] != 0 and self.rect[3] != 0:  # square cut
                img_org = qtpixmap_to_cvimg(self.scaledImg)
                cut_y = self.rect[1] - self.singleOffset.y()
                cut_x = self.rect[0] - self.singleOffset.x()
                img_mini = img_org[cut_y:cut_y + self.rect[3], cut_x:cut_x + self.rect[2]]
                self.scaledImg = QPixmap(cvImg_to_qtImg(img_mini))
                self.imgPixmap = self.scaledImg
                self.singleOffset = QPoint(self.rect[0], self.rect[1])

            self.rect = None  # 重置矩形框
            self.repaint()

        elif self.toolIndex == 2:  # freeCut
            pass

        elif self.toolIndex == 3:  # aiSensor
            pass

    '''重载绘图: 动态绘图'''

    def paintEvent(self, event):
        self.imgPainter = QPainter()  # 用于动态绘制图片
        self.imgFramePainter = QPainter()  # 用于动态绘制图片外线框
        self.imgPainter.begin(self)  # 无begin和end,则将一直循环更新
        self.imgPainter.drawPixmap(self.singleOffset, self.scaledImg)  # 从图像文件提取Pixmap并显示在指定位置
        self.imgFramePainter.setPen(QColor(168, 34, 3))  # 不设置则为默认黑色   # 设置绘图颜色/大小/样式
        self.imgFramePainter.drawRect(10, 10, 480, 480)  # 为图片绘外线狂(向外延展1)
        self.imgPainter.end()  # 无begin和end,则将一直循环更新

        if self.toolIndex == 1:
            # 初始化矩形绘图工具
            squarePainter = QPainter()
            # 开始在窗口绘制
            squarePainter.begin(self)
            # 自定义画点方法
            if self.rect:
                self.drawRect(squarePainter)
            # 结束在窗口的绘制
            squarePainter.end()

    def setPixmap(self, a0: QtGui.QPixmap) -> None:
        self.imgPixmap = a0
        self.scaledImg = self.imgPixmap.scaledToWidth(self.width())  # 初始化缩放图
        self.singleOffset = QPoint(0, 0)  # 初始化偏移值
        self.repaint()

    # =============================================================================
    # 图片移动: 首先,确定图片被点选(鼠标左键按下)且未左键释放;
    #          其次,确定鼠标移动;
    #          最后,更新偏移值,移动图片.
    # =============================================================================
    '''重载一下鼠标按下事件(单击)'''

    def mousePressEvent(self, event):
        pressedImageLabelNum = -1  # 标识鼠标点击事件所在label
        if self.objectName() == 'imageLabel1':
            pressedImageLabelNum = 1
        elif self.objectName() == 'imageLabel2':
            pressedImageLabelNum = 2
        # if self.isSelected is False:  # avoid emitting signal frequently
        #     global_refresh_result_signal.highlight_selected_box.emit(pressedImageLabelNum)

        if event.buttons() == QtCore.Qt.LeftButton:  # 左键按下
            print("鼠标左键单击")  # 响应测试语句
            self.isLeftPressed = True;  # 左键按下(图片被点住),置Ture
            self.preMousePosition = event.pos()  # 获取鼠标当前位置
            print(event.pos())
            col = event.pos().x() - self.singleOffset.x()
            row = event.pos().y() - self.singleOffset.y()

            if self.toolIndex == 0:  # floodFill
                # 使用线程运行裁切脚本
                thread = Thread(target=self.floodFillThreadFunc, args=(col, row, self.scaledImg, pressedImageLabelNum))
                thread.start()

            elif self.toolIndex == 1:  # squareCut
                self.rect = (event.x(), event.y(), 0, 0)

            elif self.toolIndex == 2:  # freeCut
                # 本部分暂时移动至独立窗口
                # self.freeCutWindow = ImageWin(self.scaledImg)
                # self.freeCutWindow.setMouseTracking(True)
                # self.freeCutWindow.setWindowTitle('Livewire Demo')
                # self.freeCutWindow.show()
                pass

            elif self.toolIndex == 3:  # aiSensor
                for i, contour in enumerate(self.cnts):  # 遍历轮廓列表
                    dist = cv2.pointPolygonTest(contour, (event.x()-self.singleOffset.x(), event.y()-self.singleOffset.y()), False)  # 判断鼠标的坐标是否在轮廓内
                    if dist >= 0:  # 如果是
                        print(f"Clicked on contour {i}")  # 打印轮廓的下标
                        x_min, x_max, y_min, y_max = drawOutRectgle(contour)
                        img_mini = QPixmap(cvImg_to_qtImg(qtpixmap_to_cvimg(self.imgPixmap)[y_min:y_max, x_min:x_max]))
                        # global_refresh_result_signal.change_result_image.emit(img_mini, pressedImageLabelNum)
                        # show the result image
                        self.scaledImg = img_mini
                        self.imgPixmap = self.scaledImg
                        self.singleOffset = QPoint(x_min + self.singleOffset.x(), y_min + self.singleOffset.y())  # 更新偏移值
                        self.repaint()
                        break
                    print("Clicked outside of any contour")  # 如果没有点击在任何轮廓内

        elif event.buttons() == QtCore.Qt.RightButton:  # 右键按下
            print("鼠标右键单击")  # 响应测试语句
        elif event.buttons() == QtCore.Qt.MidButton:  # 中键按下
            print("鼠标中键单击")  # 响应测试语句
        elif event.buttons() == QtCore.Qt.LeftButton | QtCore.Qt.RightButton:  # 左右键同时按下
            print("鼠标左右键同时单击")  # 响应测试语句
        elif event.buttons() == QtCore.Qt.LeftButton | QtCore.Qt.MidButton:  # 左中键同时按下
            print("鼠标左中键同时单击")  # 响应测试语句
        elif event.buttons() == QtCore.Qt.MidButton | QtCore.Qt.RightButton:  # 右中键同时按下
            print("鼠标右中键同时单击")  # 响应测试语句
        elif event.buttons() == QtCore.Qt.LeftButton | QtCore.Qt.MidButton \
                | QtCore.Qt.RightButton:  # 左中右键同时按下
            print("鼠标左中右键同时单击")  # 响应测试语句

    '''重载一下鼠标键松开事件'''

    def mouseReleaseEvent(self, event):
        # super().mouseReleaseEvent(event)
        pressedImageLabelNum = -1  # 标识鼠标点击事件所在label
        if self.objectName() == 'imageLabel1':
            pressedImageLabelNum = 1
        elif self.objectName() == 'imageLabel2':
            pressedImageLabelNum = 2

        # if event.buttons() == Qt.LeftButton:  # 左键释放
        if True:
            self.isLeftPressed = False  # 左键释放(图片被点住),置False
            print("鼠标左键松开")  # 响应测试语句
            print("Moved to:", self.singleOffset)



        # elif event.button() == Qt.RightButton:  # 右键释放
        #     self.singleOffset = QPoint(0, 0)  # 置为初值
        #     self.scaledImg = self.imgPixmap.scaled(self.size())  # 置为初值
        #     self.repaint()  # 重绘
        #     print("鼠标右键松开")  # 响应测试语句

    '''重载一下滚轮滚动事件'''

    def wheelEvent(self, event):
        #        if event.delta() > 0:                                                 # 滚轮上滚,PyQt4
        # This function has been deprecated, use pixelDelta() or angleDelta() instead.
        angle = event.angleDelta() / 8  # 返回QPoint对象，为滚轮转过的数值，单位为1/8度
        angleX = angle.x()  # 水平滚过的距离(此处用不上)
        angleY = angle.y()  # 竖直滚过的距离
        scalingIndex = 0.1  # 缩放速率
        if angleY > 0:  # 滚轮上滚
            print("鼠标中键上滚")  # 响应测试语句
            self.scaledImg = self.imgPixmap.scaled(self.scaledImg.width() * (1 + scalingIndex),
                                                   self.scaledImg.height() * (1 + scalingIndex))
            # newWidth = event.x() - (self.scaledImg.width() * (event.x() - self.singleOffset.x())) \
            #            / (self.scaledImg.width() - scalingIndex)
            # newHeight = event.y() - (self.scaledImg.height() * (event.y() - self.singleOffset.y())) \
            #             / (self.scaledImg.height() - scalingIndex)
            newWidth = self.singleOffset.x() - event.x() * scalingIndex
            newHeight = self.singleOffset.y() - event.y() * scalingIndex
            print("from:", self.singleOffset)
            self.singleOffset = QPoint(newWidth, newHeight)  # 更新偏移量
            print("to:", self.singleOffset)
            self.repaint()  # 重绘
        else:  # 滚轮下滚
            print("鼠标中键下滚")  # 响应测试语句
            self.scaledImg = self.imgPixmap.scaled(self.scaledImg.width() * (1 - scalingIndex),
                                                   self.scaledImg.height() * (1 - scalingIndex))
            # newWidth = event.x() - (self.scaledImg.width() * (event.x() - self.singleOffset.x())) \
            #            / (self.scaledImg.width() + scalingIndex)
            # newHeight = event.y() - (self.scaledImg.height() * (event.y() - self.singleOffset.y())) \
            #             / (self.scaledImg.height() + scalingIndex)
            newWidth = self.singleOffset.x() + event.x() * scalingIndex
            newHeight = self.singleOffset.y() + event.y() * scalingIndex
            print("from:", self.singleOffset)
            self.singleOffset = QPoint(newWidth, newHeight)  # 更新偏移量
            print("to:", self.singleOffset)
            self.repaint()  # 重绘

    '''重载一下鼠标移动事件'''

    def mouseMoveEvent(self, event):
        if self.isLeftPressed and self.toolIndex == -1:  # 左键按下且未选中工具
            print("鼠标左键按下，移动鼠标")  # 响应测试语句
            self.endMousePosition = event.pos() - self.preMousePosition  # 鼠标当前位置-先前位置=单次偏移量
            self.singleOffset = self.singleOffset + self.endMousePosition  # 更新偏移量
            self.preMousePosition = event.pos()  # 更新当前鼠标在窗口上的位置，下次移动用
            self.repaint()  # 重绘
        if self.toolIndex == 1:
            start_x, start_y = self.rect[0:2]
            self.rect = (start_x, start_y, event.x() - start_x, event.y() - start_y)
            self.update()

    #    '''重载一下鼠标双击事件'''
    #    def mouseDoubieCiickEvent(self, event):
    #        if event.buttons() == QtCore.Qt.LeftButton:                           # 左键按下
    #            self.setText ("双击鼠标左键的功能: 自己定义")
    #
    #
    #    '''重载一下鼠标进入控件事件'''
    #    def enterEvent(self, event):
    #
    #
    #    '''重载一下鼠标离开控件事件'''
    #    def leaveEvent(self, event):
    #

    #    '''重载一下鼠标进入控件事件'''
    #    def enterEvent(self, event):
    #
    #
    #    '''重载一下鼠标离开控件事件'''
    #    def leaveEvent(self, event):
    #

    def drawRect(self, qp):
        # 创建红色，宽度为4像素的画笔
        pen = QPen(Qt.red, 2)
        qp.setPen(pen)
        qp.drawRect(*self.rect)

# '''主函数'''
# if __name__ == "__main__":
#     app = QtWidgets.QApplication(sys.argv)
#     myshow = scalableImageLabel()
#     myshow.show()
#     sys.exit(app.exec_())
