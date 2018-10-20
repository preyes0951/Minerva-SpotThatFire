import praw
import urllib.request
import json
from datetime import datetime


# Get reddit keys from keys.json and start new reddit onnection
def create_reddit_connection(subreddit_name='minervaTest'):
	with open("keys.json") as f:
		key_table = json.load(f)
		reddit_data = key_table['reddit']
		client_id = reddit_data['client-id']
		client_secret = reddit_data['client-secret']

	return praw.Reddit(client_id=client_id,
							client_secret=client_secret,
						 	user_agent="Fuego Fire Tracker v 1.0 https://github.com/preyes0951/Minerva-SpotThatFire")


def is_same_day(day_one: datetime, day_two: datetime):
	if day_one.day == day_two.day and day_one.month == day_two.month and day_one.year == day_two.year:
		return True
	return False


# The PRAW submission API contains a boolean value called is_self which is true if
# the submission is a pure text post.
# This method returns true if post is not a pure text post.
def is_image_post(submission):
	return not submission.is_self


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
		if is_same_day(today, submission_date) and is_image_post(submission):
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