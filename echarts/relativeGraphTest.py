from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget

import json
from pyecharts import options as opts
from pyecharts.charts import Graph

# Load the JSON data
with open("les-miserables.json", "r", encoding="utf-8") as f:
    j = json.load(f)
    nodes = j["nodes"]
    links = j["links"]
    categories = j["categories"]

# Create the graph
c = (
    Graph(init_opts=opts.InitOpts(width="1000px", height="600px"))
    .add(
        "",
        nodes=nodes,
        links=links,
        categories=categories,
        layout="circular",
        is_rotate_label=True,
        linestyle_opts=opts.LineStyleOpts(color="source", curve=0.3),
        label_opts=opts.LabelOpts(position="right"),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="Graph-Les Miserables"),
        legend_opts=opts.LegendOpts(orient="vertical", pos_left="2%", pos_top="20%"),
    )
    .render("graph_les_miserables.html")
)

# Create the PyQt window and layout
app = QApplication([])
window = QWidget()
layout = QVBoxLayout()
window.setLayout(layout)

# Create a QWebEngineView widget to display the graph
view = QWebEngineView()
websettings = QWebEngineSettings.globalSettings()
websettings.setAttribute(QWebEngineSettings.PluginsEnabled, True)
websettings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
websettings.setAttribute(QWebEngineSettings.JavascriptCanOpenWindows, True)
view.load(QUrl("file:///graph_les_miserables.html"))
layout.addWidget(view)

# Show the window
window.show()
app.exec_()
