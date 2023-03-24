import os

from datetime import timedelta

from flask import Flask, g
from flask_jwt_extended import JWTManager

from calendar_api.blueprints import login
from calendar_lib.core import Core


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        JWT_SECRET_KEY='dev',
        JWT_ACCESS_TOKEN_EXPIRES=timedelta(days=1)
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

    return app
