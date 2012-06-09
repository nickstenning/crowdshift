from os import environ

from flask import Flask
from flask_heroku import Heroku

from . import api

def create_app():
    app = Flask(__name__)
    app.register_blueprint(api.api)

    heroku = Heroku(app)

    return app
