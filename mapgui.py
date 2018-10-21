import sys
from PyQt5.QtWidgets import (QWidget, QToolTip, QPushButton, QApplication)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from gmplot import gmplot

coords =   [(37.769901, -122.498331),
            (37.768645, -122.475328),
            (37.771478, -122.468677),
            (37.769867, -122.466102),
            (37.767187, -122.467496),
            (37.770104, -122.470436)]

#https://github.com/vgm64/gmplot
def GetMapHTML(coords):
    # Place map
    #San Frrancisco
    gmap = gmplot.GoogleMapPlotter(37.766956, -122.438481, 13,'AIzaSyCW8wSRBcgSexbzbEkJb-XyUvQnFEjY11s')
    #Huntsville
    #gmap = gmplot.GoogleMapPlotter(34.711146877417235,-86.65393352508545, 13,'AIzaSyCW8wSRBcgSexbzbEkJb-XyUvQnFEjY11s')

    # Scatter points
    top_attraction_lats, top_attraction_lons = zip(*coords)
    gmap.scatter(top_attraction_lats, top_attraction_lons, '#ff0000', size=40, marker=False)

    # Draw
    gmap.draw("my_map.html")

    f = open("my_map.html", "r")
    return f.read()


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        mapview = QWebEngineView(self)
        mapview.setHtml(GetMapHTML(coords))
        mapview.resize(400,400)
        mapview.move(50,50)

        self.resize(500, 500)
        self.setWindowTitle('Burn Notice')

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())