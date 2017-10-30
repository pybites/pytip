#!/usr/bin/env python

from collections import Counter
from os import environ
import re
import sys

from sqlalchemy.orm import sessionmaker
import tweepy

from db import Base, engine, Tip, Hashtag

Base.metadata.create_all(engine)
create_session = sessionmaker(bind=engine)
session = create_session()

consumer_key = environ.get('CONSUMER_KEY')
consumer_secret = environ.get('CONSUMER_SECRET')
access_key = environ.get('ACCESS_TOKEN')
access_secret = environ.get('ACCESS_SECRET')

PYTIP_ACCOUNT = 'python_tip'


def delete_all():
    session.query(Tip).delete()
    session.query(Hashtag).delete()
    session.commit()


def save_tweets(screen_name):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    for tw in tweepy.Cursor(api.user_timeline,
                            screen_name=screen_name,
                            exclude_replies=True,
                            include_rts=False).items():
        session.add(Tip(tweetid=tw.id,
                        text=tw.text,
                        created=tw.created_at,
                        likes=tw.favorite_count,
                        retweets=tw.retweet_count))
    session.commit()


def save_hashtags():
    tips = session.query(Tip).all()
    blob = ' '.join(t.text.lower() for t in tips)
    cnt = Counter(re.findall(r'#([a-z0-9]{3,})', blob))
    cnt.pop('python', None)
    for tag, count in cnt.items():
        session.add(Hashtag(name=tag, count=count))
    session.commit()


if __name__ == '__main__':
    try:
        screen_name = sys.argv[1]
    except IndexError:
        screen_name = PYTIP_ACCOUNT

    delete_all()
    save_tweets(screen_name)
    save_hashtags()
