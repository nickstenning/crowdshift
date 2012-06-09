from os import environ

from flask import Flask
from flask_heroku import Heroku

redis = None

def create_app():
    global redis

    app = Flask(__name__)

    # configure app from Heroku environment
    Heroku(app)

    # configure redis connection
    redis = redis.Redis(host=app.config['REDIS_HOST'],
                        port=app.config['REDIS_PORT'],
                        db=0,
                        password=app.config['REDIS_PASSWORD'])

    from . import api
    app.register_blueprint(api.api)

    return app
