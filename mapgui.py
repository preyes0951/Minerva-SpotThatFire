import sys
from PyQt5.QtWidgets import (QWidget, QToolTip, QPushButton, QApplication)
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from gmplot import gmplot

def GetMapHTML():
    # Place map
    gmap = gmplot.GoogleMapPlotter(34.711146877417235,-86.65393352508545, 13,'AIzaSyCW8wSRBcgSexbzbEkJb-XyUvQnFEjY11s')

    # Polygon
    golden_gate_park_lats, golden_gate_park_lons = zip(*[
        (37.771269, -122.511015),
        (37.773495, -122.464830),
        (37.774797, -122.454538),
        (37.771988, -122.454018),
        (37.773646, -122.440979),
        (37.772742, -122.440797),
        (37.771096, -122.453889),
        (37.768669, -122.453518),
        (37.766227, -122.460213),
        (37.764028, -122.510347),
        (37.771269, -122.511015)
    ])
    gmap.plot(golden_gate_park_lats, golden_gate_park_lons, 'cornflowerblue', edge_width=10)

    # Scatter points
    top_attraction_lats, top_attraction_lons = zip(*[
        (37.769901, -122.498331),
        (37.768645, -122.475328),
        (37.771478, -122.468677),
        (37.769867, -122.466102),
        (37.767187, -122.467496),
        (37.770104, -122.470436)
    ])
    gmap.scatter(top_attraction_lats, top_attraction_lons, '#3B0B39', size=40, marker=False)

    # Marker
    hidden_gem_lat, hidden_gem_lon = 37.770776, -122.461689
    gmap.marker(hidden_gem_lat, hidden_gem_lon, 'cornflowerblue')

    # Draw
    gmap.draw("my_map.html")

    f = open("my_map.html", "r")
    html = f.read()
    return html


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        mapview = QWebEngineView(self)
        mapview.setHtml(GetMapHTML())
        mapview.resize(400,400)
        mapview.move(50,50)

        self.resize(500, 500)
        self.setWindowTitle('Test')

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())