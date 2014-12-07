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
    return list(map(lambda x: x['text'], timeline))

def post_solution(twitter, answer):
    logging.info("Posting solution.")
    #twitter.send_direct_message(screen_name=GAME_SCREEN_NAME, text=answer)
