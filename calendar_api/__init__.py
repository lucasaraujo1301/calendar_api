import os

from datetime import timedelta

from dotenv import load_dotenv
from flask import Flask, g
from flask_jwt_extended import JWTManager

from calendar_api.blueprints import login, user
from calendar_lib.core import Core


def create_app():
    # loading variables from .env file into environment
    load_dotenv()

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY'),
        JWT_SECRET_KEY=os.getenv('JWT_SECRET_KEY'),
        JWT_ACCESS_TOKEN_EXPIRES=timedelta(hours=1)
    )
    JWTManager(app)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.before_request
    def before_request():
        g.core = Core()

    app.register_blueprint(login.app)
    app.register_blueprint(user.app)

    return app
