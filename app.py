import os
import re

from bottle import route, run, request, static_file, view
from sqlalchemy.orm import sessionmaker

from db import Base, engine, Tip, Hashtag

Base.metadata.create_all(engine)
create_session = sessionmaker(bind=engine)
session = create_session()


@route('/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root='static')


@route('/')
@route('/<tag>')
@view('index')
def index(tag=None):
    if tag is None:
        tag = request.query.get('tag') or None

    popular_tags = session.query(Hashtag).all()

    if tag is not None and re.match(r'^[a-z0-9]+$', tag.lower()):
        filter_ = "%{}%".format(tag.lower())
        tips = session.query(Tip)
        tips = tips.filter(Tip.text.ilike(filter_))
    else:
        tips = session.query(Tip)

    tips = tips.order_by(Tip.likes.desc())
    tips = tips.all()

    return {'search_tag': tag or '',
            'popular_tags': popular_tags,
            'tips': tips}


if os.environ.get('APP_LOCATION') == 'heroku':
    run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
else:
    run(host='localhost', port=8080, debug=True, reloader=True)
