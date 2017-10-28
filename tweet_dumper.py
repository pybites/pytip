#!/usr/bin/env python

from collections import namedtuple
from contextlib import contextmanager
from os import environ
import sqlite3

import tweepy

consumer_key = environ.get('CONSUMER_KEY')
consumer_secret = environ.get('CONSUMER_SECRET')
access_key = environ.get('ACCESS_TOKEN')
access_secret = environ.get('ACCESS_SECRET')

DB = 'pytips.db'
PYTIP_ACCOUNT = 'python_tip'
SQL = '''INSERT INTO tweets (id, text, created_at, favorite_count, retweet_count)
         VALUES (?, ?, ?, ?, ?)'''

tweet = namedtuple('Tweet', 'id text created likes retweets')


def connect_twitter_api():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    return tweepy.API(auth)


@contextmanager
def connect_db(db=DB):
    '''https://github.com/pybites/100DaysOfCode - day 25'''
    try:
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        yield cursor
    finally:
        conn.commit()
        conn.close()


def create_db():
    with connect_db() as cursor:
        cursor.execute('''DROP TABLE IF EXISTS tweets''')
        cursor.execute('''CREATE TABLE tweets
                        (id, text, created_at, favorite_count, retweet_count)''')


def get_all_tweets(screen_name):
    api = connect_twitter_api()

    # http://docs.tweepy.org/en/v3.5.0/cursor_tutorial.html
    for tw in tweepy.Cursor(api.user_timeline,
                            screen_name=screen_name,
                            exclude_replies=True,
                            include_rts=False).items():
        yield tweet(id=tw.id,
                    text=tw.text,
                    created=tw.created_at,
                    likes=tw.favorite_count,
                    retweets=tw.retweet_count)


def save_tweets(tweets):
    with connect_db() as cursor:
        cursor.executemany(SQL, list(tweets))


if __name__ == '__main__':
    create_db()

    tweets = list(get_all_tweets(PYTIP_ACCOUNT))

    save_tweets(tweets)
