from PyQt5.QtCore import QUrl, QObject, pyqtSignal
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget
import random
from pyecharts import options as opts
from pyecharts.charts import Graph

class WebEnginePage(QObject):
    nodeClicked = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

    @staticmethod
    def on_node_clicked(node_name):
        WebEnginePage.nodeClicked.emit(node_name)

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
             "click_event": "nodeClick('" + "node" + str(i) + "')"})
    for i in range(nodes_num):
        for j in range(nodes[i]["value"]):
            links.append({"source": "node" + str(i), "target": random.choice(nodes)["name"]})

    return nodes, links, categories


def initGraph(nodes, links, categories, width, height):
    # Create the graph
    renderred_graph_path = "relative_graph.html"
    # JavaScript function for handling node click event
    c = (
        Graph(init_opts=opts.InitOpts(width=str(width) + "px", height=str(height)+"px"))
        .add(
            "",
            nodes=nodes,
            links=links,
            categories=categories,
            layout="circular",
            is_rotate_label=False,
            linestyle_opts=opts.LineStyleOpts(color="source", curve=0.3),
            label_opts=opts.LabelOpts(position="right", font_size=20),
            tooltip_opts=opts.TooltipOpts(textstyle_opts=opts.TextStyleOpts(font_size=20)),
            gravity=0.5,
        )
        .set_global_opts(
            legend_opts=opts.LegendOpts(orient="horizontal", pos_left="center", textstyle_opts=opts.TextStyleOpts(font_size=30), padding=5),
            # init_opts=opts.InitOpts(bg_color="transparent")
        )
        .render(renderred_graph_path)
    )
    return renderred_graph_path


# Create the PyQt widget
def initPyQtGraph(nodes, links, categories, width=600, height=600, view:QWebEngineView = None):
    # Create a QWebEngineView widget to display the graph
    if view is None:
        view = QWebEngineView()
    websettings = QWebEngineSettings.globalSettings()
    websettings.setAttribute(QWebEngineSettings.PluginsEnabled, True)
    websettings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
    websettings.setAttribute(QWebEngineSettings.JavascriptCanOpenWindows, True)

    renderred_graph_path = initGraph(nodes, links, categories, width, height)

    view.load(QUrl('file:///' + renderred_graph_path))

    return view


if __name__ == "__main__":
    app = QApplication([])
    nodes, links, categories = random_data()
    view = initPyQtGraph(nodes, links, categories)
    view.show()
    app.exec_()
