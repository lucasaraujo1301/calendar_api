import os

from datetime import timedelta

from flask import Flask, g
from flask_jwt_extended import JWTManager

from calendar_api.blueprints import login
from calendar_api.core import Core


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        JWT_SECRET_KEY='dev',
        JWT_ACCESS_TOKEN_EXPIRES=timedelta(days=1)
    )
    JWTManager(app)

    # if test_config is None:
    #     # load the instance config, if it exists, when not testing
    #     app.config.from_pyfile('config.py', silent=True)
    # else:
    #     # load the test config if passed in
    #     app.config.from_mapping(test_config)

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
