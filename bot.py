import praw
import urllib.request
import json
from datetime import datetime


# Get reddit keys from keys.json and start new reddit connection
def create_reddit_connection(subreddit_name='minervaTest'):
	with open("keys.json") as f:
		key_table = json.load(f)
		reddit_data = key_table['reddit']
		client_id = reddit_data['client-id']
		client_secret = reddit_data['client-secret']

	return praw.Reddit(client_id=client_id,
							client_secret=client_secret,
						 	user_agent="Fuego Fire Tracker v 1.0 https://github.com/preyes0951/Minerva-SpotThatFire")


# https://stackoverflow.com/questions/6407362/how-can-i-check-if-a-date-is-the-same-day-as-datetime-today
def is_same_day(day_one: datetime, day_two: datetime):
	return (day_one - day_two).days == 0


# The PRAW submission API contains a boolean value called is_self which is true if
# the submission is a pure text post.
# This method returns true if post is not a pure text post.
def is_image_post(submission):
	return not submission.is_self


def get_image(url):
	try:
		# https://stackoverflow.com/questions/3042757/downloading-a-picture-via-urllib-and-python
		image_data = urllib.request.urlopen(url)
		return image_data.read()
	except urllib.error.HTTPError:
		return None


# Run minerva bot to get today's posts on the desired subreddit
# Returns a list of images
def run(subreddit_name='minervaTest'):
	reddit = create_reddit_connection(subreddit_name)
	sub = reddit.subreddit(subreddit_name)
	today = datetime.today()

	images = []
	for submission in sub.new():
		submission_date = datetime.fromtimestamp(submission.created_utc)
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