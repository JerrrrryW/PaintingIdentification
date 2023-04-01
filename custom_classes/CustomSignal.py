from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap

'''自定义信号量'''
class CustomSignal(QObject):
    # Create a semaphore in demoWindow and update UI after clipping.
    change_result_image = pyqtSignal(QPixmap, int)
    # Highlight the corresponding GroupBox
    highlight_selected_box = pyqtSignal(int)
    # Refresh the tool bar
    refresh_tool_bar = pyqtSignal()

