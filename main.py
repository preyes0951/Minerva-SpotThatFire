import bot
from mapgui import *


def main():
	posts = bot.run()
	for title, image in posts:
		print(title)


if __name__ == "__main__":
	main()