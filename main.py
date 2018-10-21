import bot
from mapgui import *


# Runs a prototype instance of BurnNotice
def main():
	app = QApplication(sys.argv)
	the_burn = BurnNoticeExampleWidget()
	sys.exit(app.exec_())


# Displays locations of posts on the minervaTest subreddit from the last 24 hours using Google Maps and PyQt5
class BurnNoticeExampleWidget(QWidget):
	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):
		mapview = QWebEngineView(self)
		mapview.setHtml(GetMapHTML(self.get_coords()))
		mapview.resize(400, 400)
		mapview.move(50, 50)

		self.resize(500, 500)
		self.setWindowTitle('Burn Notice')

		self.show()

	def get_coords(self):
		posts = bot.run()
		return bot.extract_location_from_posts(posts)


if __name__ == "__main__":
	main()
