import os

import bottle
from bottle.ext import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Column, Sequence, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine(os.environ.get('DATABASE_URL'), echo=True)

app = bottle.Bottle()
plugin = sqlalchemy.Plugin(engine, Base.metadata)
app.install(plugin)


class Hashtag(Base):
    __tablename__ = 'hashtags'
    id = Column(Integer, Sequence('id_seq'), primary_key=True)
    name = Column(String(20))
    count = Column(Integer)

    def __repr__(self):
        return "<Hashtag('%s', '%d')>" % (self.name, self.count)


class Tip(Base):
    __tablename__ = 'tips'
    id = Column(Integer, Sequence('id_seq'), primary_key=True)
    tweetid = Column(String(22))
    text = Column(String(300))
    created = Column(DateTime)
    likes = Column(Integer)
    retweets = Column(Integer)

    def __init__(self, tweetid, text, created, likes, retweets):
        self.tweetid = tweetid
        self.text = text
        self.created = created
        self.likes = likes
        self.retweets = retweets

    def __repr__(self):
        return "<Tip('%d', '%s')>" % (self.id, self.text)