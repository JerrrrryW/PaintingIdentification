import sys
from PyQt5.QtWidgets import QApplication, QWidget, QListWidget, QStackedWidget, QHBoxLayout


class SideBar(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 创建一个水平布局
        layout = QHBoxLayout()
        # 创建一个列表部件作为一级菜单
        self.list_widget = QListWidget()
        # 添加一级菜单项
        self.list_widget.addItem("菜单1")
        self.list_widget.addItem("菜单2")
        self.list_widget.addItem("菜单3")
        # 创建一个堆叠部件作为二级菜单容器
        self.stack_widget = QStackedWidget()
        # 创建三个列表部件作为二级菜单
        self.sub_list1 = QListWidget()
        self.sub_list2 = QListWidget()
        self.sub_list3 = QListWidget()
        # 添加二级菜单项
        self.sub_list1.addItem("选项1-1")
        self.sub_list1.addItem("选项1-2")
        self.sub_list2.addItem("选项2-1")
        self.sub_list2.addItem("选项2-2")
        self.sub_list3.addItem("选项3-1")
        self.sub_list3.addItem("选项3-2")

        # 将二级菜单添加到堆叠部件中

        for sub_list in [self.sub_list1, self.sub_list2, self.sub_list3]:
            sub_list.setFixedWidth(100)  # 设置固定宽度，可根据需要调整
            sub_list.setFixedHeight(200)  # 设置固定高度，可根据需要调整
            sub_list.setStyleSheet('background-color: lightgray')  # 设置背景颜色，可根据需要调整
            sub_list.setSpacing(10)  # 设置间距，可根据需要调整
            sub_list.itemClicked.connect(self.on_sub_item_clicked)  # 连接点击事件的槽函数，可根据需要实现不同的功能
            self.stack_widget.addWidget(sub_list)

        # 将列表部件和堆叠部件添加到水平布局中
        layout.addWidget(self.list_widget)
        layout.addWidget(self.stack_widget)
        layout.setSpacing(0)  # 设置布局间距为0，可根据需要调整

        # 将水平布局设置为窗口的主布局
        self.setLayout(layout)

        # 连接一级菜单的currentRowChanged信号和堆叠部件的setCurrentIndex方法
        self.list_widget.currentRowChanged.connect(self.stack_widget.setCurrentIndex)


    def on_sub_item_clicked(self, item):
        print(item.text())  # 打印点击的二级菜单项的文本，可根据需要实现不同的功能


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sidebar = SideBar()
    sidebar.show()
    sys.exit(app.exec_())