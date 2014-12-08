# -*- coding: utf-8 -*-
import re
import os
import time
import logging
import click
import arrow

from twitterhelpers import get_twython, get_tweets, post_solution
from thesaurus import get_thesaurus_text
from solver import ThesaurusSolver

SLEEP_MIN = os.environ.get('SOLVE_INTERVAL', 50)
MY_NAME = 'wordchallenger'

log_fmt = "%(levelname)-6s %(filename)-12s:%(lineno)-4d at %(asctime)s: %(message)s"
logging.basicConfig(level=logging.DEBUG, format=log_fmt)

def main_loop(twitter, solver, commit=False):
    # Once per human-reasonable hour, attempt to solve.

    while True:
        pac_time = arrow.utcnow().to('US/Pacific')

        if reasonable_human_hour(pac_time.hour):
            logging.info("Solving problem, it's a reasonable hour :: %s" % pac_time)
            try:
                solve_problem_and_post_solution(twitter, solver, commit)
            except Exception as e:
                logging.exception(e)
        else:
            logging.info("If I was a human right now I'd be asleep. Don't try to solve.")

        logging.info("Will try again in %s minutes" % SLEEP_MIN)
        seconds_sleep = SLEEP_MIN * 60
        time.sleep(seconds_sleep)
        logging.info("Waking up.")

def reasonable_human_hour(pac_hour):
    return pac_hour >= 8 and pac_hour <= 20

def solve_problem_and_post_solution(twitter, solver, commit):

    tweets = get_tweets(twitter)

    if not tweets:
        logging.error("No tweets returned!")
        return

    favorite_winning_tweets(twitter, tweets, commit=commit)

    last_tweet_id = tweets[0][0]
    last_tweet_text = tweets[0][1]

    answer = get_and_solve_tweet(last_tweet_text, solver)

    if answer:
        logging.info("Candidate Answer: %s" % answer)
        post_solution(twitter, last_tweet_id, answer, commit=commit)
        return True
    else:
        logging.info("No candidate answers")
        return False


def favorite_winning_tweets(twitter, tweets, commit):
    for tweet_id, tweet_text, favorited in tweets:
        if MY_NAME in tweet_text and not favorited:
            logging.info("Favoriting tweet: %s" % tweet_text)
            
            if commit:
                twitter.create_favorite(id=tweet_id)
            else:
                logging.info("Not committing")

            logging.info("Sleeping a little...")
            time.sleep(5) # Sleep a few seconds before posting again


def get_and_solve_tweet(tweet_text, solver):
    
    logging.info("Last tweet was: %s" % tweet_text)
    if 'Guess the word' in tweet_text:
        match_regex, related, hint_regex = get_hint_and_related(tweet_text)

        logging.debug("Hint Regex: %s" % hint_regex) 
        logging.debug("Related Words: %s" % related) 

        answers =  solver.solve_problem(match_regex, related)
        logging.info("Possible answers: %s" % answers)
        if len(answers) > 0:
            return answers[0][0]
        else:
            return None
    else:
        logging.info("No current Challenge: %s" % tweet_text)

def get_hint_and_related(tweet):

    # Pull out the hint and related text
    extract_data = re.compile('.*int. (?P<hint>.+)\n.+words are: (?P<related>.+)[\.]*', re.IGNORECASE)
    matches = extract_data.search(tweet)
        
    # Turn the hint into regex
    hint = matches.groupdict()['hint']
    hint = hint.encode('utf-8').replace('●', '.').replace(' ', '')
    hint_regex_text = ';(?P<name>' + hint + ');'    
    match_regex = re.compile(hint_regex_text, re.IGNORECASE)

    # Get related words
    related = matches.groupdict()['related'].split(', ')
    
    return match_regex, related, hint_regex_text


@click.command()
@click.option('--oneoff',
              default=False,
              is_flag=True,
              help='Run script as oneoff. Default is to run as loop.')
@click.option('--commit',
                default=False,
                is_flag=True,
                help='Whether to post to twitter.')
def main(oneoff, commit):
    
    twitter = get_twython()
    text = get_thesaurus_text()
    solver = ThesaurusSolver(text)

    if oneoff:
        solve_problem_and_post_solution(twitter, solver, commit)
    else:
        main_loop(twitter, solver, commit=commit)

if __name__ == "__main__":

    main()
