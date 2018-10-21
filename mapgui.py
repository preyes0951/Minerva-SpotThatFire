import sys
from PyQt5.QtWidgets import (QWidget, QToolTip, QPushButton, QApplication)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from gmplot import gmplot

default_location = (34.711146877417235, -86.65393352508545)


# Returns first latitude and longitude of data set or default
def get_first_coord(coord):
	if len(coord) > 0:
		return coord[0]
	else:
		return default_location


# https://github.com/vgm64/gmplot
def GetMapHTML(coords):
	first_lat, first_long = get_first_coord(coords)
	gmap = gmplot.GoogleMapPlotter(first_lat, first_long, 13, 'AIzaSyCW8wSRBcgSexbzbEkJb-XyUvQnFEjY11s')

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
		# mapview.setHtml(GetMapHTML(coords))
		mapview.resize(400, 400)
		mapview.move(50, 50)

		self.resize(500, 500)
		self.setWindowTitle('Burn Notice')

		self.show()


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Example()
	sys.exit(app.exec_())
