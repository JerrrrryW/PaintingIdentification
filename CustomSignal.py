from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap

'''自定义信号量'''
class CustomSignal(QObject):
    # 在demoWindow中实例化全局信号量，当裁剪子进程处理完毕后刷新UI
    change_result_image = pyqtSignal(QPixmap, int)
