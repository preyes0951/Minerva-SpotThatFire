import praw
import urllib.request
import json
from datetime import datetime


# Takes reddit post titles and returns a list of tuples formatted like (latitude, longitude)
# reddit post must contain format of "latitude longitude" or function returns a tuple of None values
def extract_location_from_title(post_title: str):
	invalid_data = (None, None)
	attempted_data_process = post_title.split(sep=' ', maxsplit=2)
	if len(attempted_data_process) > 1:
		location = (extract_float_value(attempted_data_process[0]), extract_float_value(attempted_data_process[1]))
	else:
		location = invalid_data
	return location


# Protected float to string conversion
def extract_float_value(s:str):
	try:
		return float(s)
	except ValueError as val_error:
		return None


def extract_location_from_posts(posts):
	locations = []
	for title, _ in posts:
		locations.append(extract_location_from_title(title))
	return filter_none_values(locations)


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


# Returns image if url was read successfully or None if image wasn't successful
# If implementing this project for real then one would need to validate that only
# image urls are passed into the get_image function. Otherwise the function
# throws the ugly URLError exception.
def get_image(url: str):
	try:
		with urllib.request.urlopen(url) as urlstream:
			image = urlstream.read()
	except urllib.error.HTTPError:
		image = None
	except urllib.error.URLError:
		image = None
	return image


# Removes posts if they have None images
def filter_none_values(images):
	return [(title, image) for title, image in images if image is not None]


# Run minerva bot to get today's posts on the desired subreddit
# Returns a list of tuples organized like: (title, image)
def run(subreddit_name='minervaTest'):
	reddit = create_reddit_connection(subreddit_name)
	sub = reddit.subreddit(subreddit_name)
	today = datetime.today()
	images = []
	for submission in sub.new():
		submission_date = datetime.fromtimestamp(submission.created_utc)
		if is_same_day(today, submission_date) and is_image_post(submission):
			title = submission.title
			image = get_image(submission.url)
			images.append((title, image))
	return filter_none_values(images)


# Test minerva bot
def main():
	todays_images = run()
	image_counter = 0
	for title, image in todays_images:
		with open('file' + str(image_counter) + '.jpg', 'wb') as f:
			f.write(image)
			image_counter += 1


if __name__ == "__main__":
	main()