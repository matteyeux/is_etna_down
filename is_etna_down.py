#!/usr/bin/python3

import sys
import datetime
from twython import Twython
from urllib.request import urlopen

CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_KEY = ''
ACCESS_SECRET = ''

api = Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET)
url = "https://intra.etna-alternance.net"
status_file = "status.txt"
now = str(datetime.datetime.now())
now = now.split('.')[0]

do_tweet = True

# just test without tweeting
if len(sys.argv) == 2:
	if sys.argv[1] == "notweet":
		do_tweet = False

try:
	r = urlopen(url)
	code = str(r.code)
	message = "OK"
except :
	code = "500" # means no internet @ etna
	message = "not available"

# open status file to get initial status code
with open(status_file, 'r') as f:
	status = f.readline()

# if status is not the same as the new one then state has changed
if status != str(code):
	# write current status code 
	with open(status_file, 'w') as f:
		f.write(str(code))
	# if code is between 200 or 300 that's OK
	if code[0] == "2" or  code[0] == "3":
		tweet = now + " ETNA intra is now up"
	else:
		tweet = now + " ETNA intra is down"

	print(tweet)
	if do_tweet is True:
		api.update_status(status=tweet)
	else :
		print("won't tweet")

	with open("is_down.log", 'a') as log:
		log.write(now + " : " + code + "\t" + message + "\n")

else:
	print("state: unchanged")
