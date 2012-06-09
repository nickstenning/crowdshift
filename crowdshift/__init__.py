from os import environ
from urlparse import urlparse

import redis

from flask import Flask

# redis connection
rc = None

def create_app():
    global rc

    app = Flask(__name__)

    # configure redis connection
    rc = _init_redis(environ.get('REDISTOGO_URL', 'redis://localhost:6379'))

    from . import api
    app.register_blueprint(api.api)

    return app

def _init_redis(url):
    url = urlparse(url)

    # Make sure it's a redis database.
    if url.scheme:
        assert url.scheme == 'redis'

    # Attempt to resolve database id.
    try:
        db = int(url.path.replace('/', ''))
    except (AttributeError, ValueError):
        db = 0

    return redis.StrictRedis(host=url.hostname,
                             port=url.port,
                             db=db,
                             password=url.password)
