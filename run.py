# -*- coding: utf-8 -*-
import re
import os
import time
import logging

import arrow

from twitterhelpers import get_twython, get_tweets, post_solution
from thesaurus import get_thesaurus_text
from solver import ThesaurusSolver

SLEEP_MIN = os.environ.get('SOLVE_INTERVAL', 50)

log_fmt = "%(levelname)-6s %(filename)-12s:%(lineno)-4d at %(asctime)s: %(message)s"
logging.basicConfig(level=logging.DEBUG, format=log_fmt)

def main_loop(twitter, solver):
    # Once per human-reasonable hour, attempt to solve.

    while True:
        pac_time = arrow.utcnow().to('US/Pacific')

        if reasonable_human_hour(pac_time.hour):
            logging.info("Solving problem, it's a reasonable hour :: %s" % pac_time)
            solve_problem_and_post_solution(twitter, solver)
        else:
            logging.info("If I was a human right now I'd be asleep. Don't try to solve.")

        logging.info("Will try again in %s minutes" % SLEEP_MIN)
        seconds_sleep = SLEEP_MIN * 60
        time.sleep(seconds_sleep)
        logging.info("Waking up.")

def reasonable_human_hour(pac_hour):
    return pac_hour >= 8 and pac_hour <= 20

def solve_problem_and_post_solution(twitter, solver):
    answer = get_and_solve_tweet(twitter, solver)

    if answer:
        logging.info("Candidate Answer: %s" % answer)
        post_solution(twitter, answer)
        return True
    else:
        logging.info("No candidate answers")
        return False

def get_and_solve_tweet(twitter, solver):
    tweets = get_tweets(twitter)
    last_tweet = tweets[0]
    logging.info("Last tweet was: %s" % last_tweet)
    if 'Guess the word' in last_tweet:
        try:
            match_regex, related, hint_regex = get_hint_and_related(last_tweet)
 
            logging.debug("Hint Regex: %s" % hint_regex) 
            logging.debug("Related Words: %s" % related) 

            answers =  solver.solve_problem(match_regex, related)
            logging.info("Possible answers: %s" % answers)
            if len(answers) > 0:
                return answers[0][0]
            else:
                return None
        except Exception as e:
            print e
    else:
        logging.info("No current Challenge: %s" % last_tweet)

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

if __name__ == "__main__":
    
    twitter = get_twython()
    text = get_thesaurus_text()
    solver = ThesaurusSolver(text)

    main_loop(twitter, solver)
    
