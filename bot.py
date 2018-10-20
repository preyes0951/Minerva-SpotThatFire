import praw
import urllib.request
from datetime import datetime, date
import time

client_id = 'KOaqBIKzJYhhsg'
client_secret = "sDRORt1IXXygdTmajuyGVOcm1B0"


def is_same_day(day_one: datetime, day_two: datetime):
	return day_one.day == day_two.day


# Run minerva bot to get today's posts on the minerva subreddit
# Returns a list of images
def run(subreddit_name='minervaTest'):
	reddit = praw.Reddit(client_id=client_id,
						 client_secret=client_secret,
						 user_agent="Fuego Fire Tracker v 1.0 https://github.com/preyes0951/Minerva-SpotThatFire")
	sub = reddit.subreddit(subreddit_name)
	today = datetime.today()

	print(datetime.utcnow().day)
	images = []
	for submission in sub.new():
		# https://stackoverflow.com/questions/3042757/downloading-a-picture-via-urllib-and-python
		if datetime.fromtimestamp(submission.created_utc).day == today.day:
			images.append(urllib.request.urlopen(submission.url).read())
	return images


# Test minerva bot
def main():
	todays_images = run()
	image_counter = 0
	for image in todays_images:
		with open('file' + str(image_counter) + '.jpg', 'wb') as f:
			f.write(image)
		image_counter += 1


if __name__ == "__main__":
	main()