from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLabel


class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super(ClickableLabel, self).__init__(parent)
        self.setText("pls select image")

    def mousePressEvent(self, event):
        self.clicked.emit()
        print(f"ClickableLabel {self.objectName()} is clicked!")
        QLabel.mousePressEvent(self, event)
