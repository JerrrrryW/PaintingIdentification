import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QListWidgetItem
from PyQt5.uic import loadUi


class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Complex List Example')
        self.setGeometry(100, 100, 800, 600)

        self.listWidget = QListWidget(self)
        self.listWidget.setWordWrap(True)
        self.listWidget.setFlow(QListWidget.TopToBottom)
        self.listWidget.setResizeMode(QListWidget.Adjust)
        self.listWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        for i in range(10):
            item = QListWidgetItem(self.listWidget)
            ui_file = loadUi('stampListItem.ui')
            item.setSizeHint(ui_file.sizeHint())
            self.listWidget.setItemWidget(item, ui_file)

        self.setCentralWidget(self.listWidget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())
