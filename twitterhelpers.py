import os
from twython import Twython
import logging
GAME_SCREEN_NAME = 'ThesaurusGame'


def get_twython():
    consumer_key = os.environ.get('GENIUS_CONSUMER_KEY')
    consumer_secret = os.environ.get('GENIUS_CONSUMER_SECRET')
    access_token = os.environ.get('GENIUS_ACCESS_TOKEN')
    access_token_secret = os.environ.get('GENIUS_ACCESS_TOKEN_SECRET')

    twitter = Twython(consumer_key,
                          consumer_secret,
                          access_token,
                          access_token_secret)
    return twitter

def get_tweets(twitter):
    timeline = twitter.get_user_timeline(screen_name=GAME_SCREEN_NAME)
    return [(m['id'], m['text'], m['favorited']) for m in timeline]

def post_solution(twitter, in_reply_to, answer, commit=True):

    status = "@%s %s" % (GAME_SCREEN_NAME, answer)

    logging.info("Posting status: '%s', IRT %s" % (status, in_reply_to))

    if commit:
    	twitter.update_status(
	    	status=status, 
	    	in_reply_to_status_id=in_reply_to)
    else:
    	logging.info("Not committig.")