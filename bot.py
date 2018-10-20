import praw
import urllib.request
from datetime import datetime

client_id = 'KOaqBIKzJYhhsg'
client_secret = "sDRORt1IXXygdTmajuyGVOcm1B0"


def create_reddit_connection(subreddit_name='minervaTest'):
	return praw.Reddit(client_id=client_id,
						 client_secret=client_secret,
						 user_agent="Fuego Fire Tracker v 1.0 https://github.com/preyes0951/Minerva-SpotThatFire")


def is_same_day(day_one: datetime, day_two: datetime):
	if day_one.day == day_two.day and day_one.month == day_two.month and day_one.year == day_two.year:
		return True
	return False


def is_image(url_request):
	return url_request.info().get_content_type().find('image') != -1


def get_image(url):
	# https://stackoverflow.com/questions/12474406/python-how-to-get-the-content-type-of-an-url
	try:
		image_data = urllib.request.urlopen(url)
		return image_data.read()
	except urllib.error.HTTPError:
		return None

# Run minerva bot to get today's posts on the minerva subreddit
# Returns a list of images
def run(subreddit_name='minervaTest'):
	reddit = create_reddit_connection(subreddit_name)
	sub = reddit.subreddit(subreddit_name)
	today = datetime.today()

	images = []
	for submission in sub.new():
		# https://stackoverflow.com/questions/3042757/downloading-a-picture-via-urllib-and-python
		submission_date = datetime.fromtimestamp(submission.created_utc)
		# https://stackoverflow.com/questions/12474406/python-how-to-get-the-content-type-of-an-url
		if is_same_day(today, submission_date) and not submission.is_self:
			image = get_image(submission.url)
			if image is not None:
				images.append(image)

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