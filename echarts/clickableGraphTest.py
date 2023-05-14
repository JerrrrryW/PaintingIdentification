from PyQt5.QtCore import Qt, QUrl, pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from pyecharts import options as opts
from pyecharts.charts import Graph
import random

# generate random data
def random_data(nodes_num=20):
    nodes = []
    links = []
    categories = [{"name": "画作"},
                  {"name": "题款"},
                  {"name": "印章"}]
    for i in range(nodes_num):
        nodes.append(
            {"name": "node" + str(i),
             "value": random.randint(1, 5),
             "category": random.choice(categories)["name"],
             "click_event": "nodeClick('node" + str(i) + "', " + str(random.randint(1, 5)) + ")"})
    for i in range(nodes_num):
        for j in range(nodes[i]["value"]):
            links.append({"source": "node" + str(i), "target": random.choice(nodes)["name"]})

    return nodes, links, categories


# 创建一个自定义的MainWindow类
class MainWindow(QMainWindow):
    def __init__(self, nodes, links, categories):
        super(MainWindow, self).__init__()

        # 创建一个QWebEngineView实例
        self.webview = QWebEngineView()

        # 创建一个QLabel实例用于显示节点信息
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText("点击节点以显示信息")

        # 创建一个垂直布局，并将QWebEngineView和QLabel添加进去
        layout = QVBoxLayout()
        layout.addWidget(self.webview)
        layout.addWidget(self.label)

        # 创建一个QWidget实例作为主窗口的中心部件
        widget = QWidget()
        widget.setLayout(layout)

        # 将QWidget设置为主窗口的中心部件
        self.setCentralWidget(widget)

        # 加载关系图的HTML文件
        self.rendered_graph_path = self.initGraph(nodes, links, categories)
        self.webview.load(QUrl('file:///' + self.rendered_graph_path))

        # 设置JavaScript交互回调函数
        self.webview.page().runJavaScript('''
            function handleClick(params) {
                // 将节点信息发送给Python代码
                window.pywebview.handleNodeClick(params.data.name);
            }

            document.addEventListener('DOMContentLoaded', function() {
                myChart.on('click', handleClick);
            });
        ''')

    # 创建关系图并返回生成的HTML文件路径
    def initGraph(self, nodes, links, categories, width=600, height=600):
        renderred_graph_path = "relative_graph.html"
        c = (
            Graph(init_opts=opts.InitOpts(width=str(width) + "px", height=str(height) + "px"))
            .add(
                "",
                nodes=nodes,
                links=links,
                categories=categories,
                layout="circular",
                is_rotate_label=False,
                linestyle_opts=opts.LineStyleOpts(color="source", curve=0.3),
                label_opts=opts.LabelOpts(position="right"),
                gravity=0.5,
            )
            .set_global_opts(
                legend_opts=opts.LegendOpts(orient="horizontal", pos_left="10%"),
            )
            .render(renderred_graph_path)
        )
        return renderred_graph_path

    # Python回调函数，处理节点点击事件
    @pyqtSlot(str)
    def handle_node_click(self, node_name):
        # 在QLabel上显示节点信息
        self.label.setText(f'Clicked Node: {node_name}')


if __name__ == "__main__":
    app = QApplication([])
    nodes, links, categories = random_data()
    window = MainWindow(nodes, links, categories)

    # 绑定JavaScript回调函数
    page = window.webview.page()
    page.runJavaScript(
        "window.pywebview = { handleNodeClick: function(node_name) { pywebview.handleNodeClick(node_name); } };")

    window.show()
    app.exec_()