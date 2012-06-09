from os import environ

from flask import Flask
from flask_heroku import Heroku
from flaskext.redis import init_redis

redis = None

def create_app():
    global redis

    app = Flask(__name__)

    # configure app from Heroku environment
    Heroku(app)

    # configure redis connection
    redis = init_redis(app)

    from . import api
    app.register_blueprint(api.api)

    return app
