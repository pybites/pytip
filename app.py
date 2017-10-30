from collections import Counter
import os
import re

from bottle import route, run, request, static_file, view

from tweets import get_tweets_db


def get_hashtags(tips):
    blob = ' '.join(t['text'].lower() for t in tips)
    cnt = Counter(re.findall(r'#([a-z]{3,})', blob))
    cnt.pop('python', None)
    return sorted(cnt.items())


@route('/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root='static')


@route('/')
@route('/<tag>')
@view('index')
def index(tag=None):
    if tag is None:
        tag = request.query.get('tag') or None

    tips = get_tweets_db()
    popular_tags = get_hashtags(tips)

    if tag is not None and re.match(r'^[a-z]+$', tag):
        # 2nd db call need to enhance
        tips = get_tweets_db(tag)

    return {'tag': tag or '',
            'popular_tags': popular_tags,
            'tips': tips}


if os.environ.get('APP_LOCATION') == 'heroku':
    run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
else:
    run(host='localhost', port=8080, debug=True, reloader=True)
