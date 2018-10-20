import praw
import urllib.request

client_id = 'KOaqBIKzJYhhsg'
client_secret = "sDRORt1IXXygdTmajuyGVOcm1B0"

def run():
	reddit = praw.Reddit(client_id=client_id,
						 client_secret=client_secret,
						 user_agent="Fuego Fire Tracker v 1.0 https://github.com/preyes0951/Minerva-SpotThatFire")
	sub = reddit.subreddit('minervaTest')
	for submission in sub.new():
		# https://stackoverflow.com/questions/3042757/downloading-a-picture-via-urllib-and-python
		image = urllib.request.urlopen(submission.url).read()
		with open('image.jpg', 'wb') as f:
			f.write(image)

def main():
	run()

main()