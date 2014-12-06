# -*- coding: utf-8 -*-
from twython import Twython
import re
import requests
import os
from unipath import Path
from solver import ThesaurusSolver

def get_thesaurus_text():
    index_url = "http://www.gutenberg.org/cache/epub/10681/pg10681.txt"
    index_text = requests.get(index_url).text
    relevant_text = index_text[4764:2781002]
    return relevant_text

def get_tweets(twitter):
    timeline = twitter.get_user_timeline(screen_name='ThesaurusGame')
    return list(map(lambda x: x['text'], timeline))

def get_hint_and_related(tweet):
    extract_data = re.compile('Hint: (?P<hint>.+)\\nRelated words are: (?P<related>.+)\.', re.IGNORECASE)
    matches = extract_data.search(tweet)
    
    print tweet
    
    hint = matches.groupdict()['hint']
    hint = hint.encode('utf-8').replace('●', '.').replace(' ', '')
    hint_regex = ';(?P<name>' + hint + ');'    
    
    match_regex = re.compile(hint_regex, re.IGNORECASE)
    related = matches.groupdict()['related'].split(', ')
    
    return match_regex, related, hint_regex

def get_and_solve_tweet(twitter, solver):
    tweets = get_tweets(twitter)
    last_tweet = tweets[0]
    print "Last weet was: %s" % last_tweet 
    if 'Guess the word' in last_tweet:
        try:
            match_regex, related, hint_regex = get_hint_and_related(last_tweet)
            print match_regex
            print related
            print hint_regex
            answers =  solver.solve_problem(match_regex, related)
            if len(answers) > 0:
                return answers[0][0]
            else:
                return None
        except Exception as e:
            print e
    else:
        print "No current Challenge: %s" % last_tweet

if __name__ == "__main__":

    consumer_key = os.environ.get('GENIUS_CONSUMER_KEY')
    consumer_secret = os.environ.get('GENIUS_CONSUMER_SECRET')
    access_token = os.environ.get('GENIUS_ACCESS_TOKEN')
    access_token_secret = os.environ.get('GENIUS_ACCESS_TOKEN_SECRET')

    twitter = Twython(consumer_key,
                          consumer_secret,
                          access_token,
                          access_token_secret)


    p = Path('thesaurus.txt')
    text = None
    if not p.exists():
        print "File doesn't exist, parsing from internet"
        text = get_thesaurus_text()
        p.write_file(text.encode('utf-8'))
    else:
        print "File exists, reading in"
        text = p.read_file().decode('utf-8')

    solver = ThesaurusSolver(text)
    answers = get_and_solve_tweet(twitter, solver)
    print answers