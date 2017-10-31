import os

from bottle import route, run, request, static_file, view

from db import get_tags, get_tips


@route('/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root='static')


@route('/')
@route('/<tag>')
@view('index')
def index(tag=None):
    if tag is None:
        tag = request.query.get('tag') or None

    popular_tags = get_tags()

    tips = get_tips(tag)

    return {'search_tag': tag or '',
            'popular_tags': popular_tags,
            'tips': tips}


if os.environ.get('APP_LOCATION') == 'heroku':
    run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
else:
    run(host='localhost', port=8080, debug=True, reloader=True)
