import logging
import os
import sys

from datetime import timedelta
from dotenv import load_dotenv
from flask import Flask, g
from flask_jwt_extended import JWTManager

from calendar_api.blueprints import login, user
from calendar_lib.core import Core


def configure_logging():
    # Configure the logging
    logger = logging.getLogger('CalendarApi')
    logger.setLevel(logging.DEBUG if os.getenv('ENVIRONMENT') == 'dev' else logging.INFO)

    stream_handler = logging.StreamHandler(sys.stdout)
    logger.addHandler(stream_handler)

    return logger


def create_app():
    # Loading variables from .env file into the environment
    load_dotenv()

    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY'),
        JWT_SECRET_KEY=os.getenv('JWT_SECRET_KEY'),
        JWT_ACCESS_TOKEN_EXPIRES=timedelta(hours=1)
    )
    JWTManager(app)

    # Configure logging
    logger = configure_logging()
    app.logger.disabled = True
    app.logger = logger

    # Ensure the instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    @app.before_request
    def before_request():
        g.core = Core(app.logger)

    # Register blueprints
    app.register_blueprint(login.app)
    app.register_blueprint(user.app)

    return app
