"""
Main module 
"""

import sys
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtGui import QPixmap

from gui import ImageWin

def main(img: QPixmap):
    app = QtWidgets.QApplication(sys.argv)
    window = ImageWin(img)
    window.setMouseTracking(True)
    window.setWindowTitle('Livewire Demo')
    window.show()
    window.setFixedSize(window.size())
    sys.exit(app.exec_())

# if __name__ == '__main__':
#     main()