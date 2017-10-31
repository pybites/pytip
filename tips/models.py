from sqlalchemy import Column, Sequence, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


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

    def __repr__(self):
        return "<Tip('%d', '%s')>" % (self.id, self.text)
