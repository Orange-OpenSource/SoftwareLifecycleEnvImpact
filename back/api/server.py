import json
import connexion
import flask
from flask_cors import CORS
from marshmallow import ValidationError

from api import config
from api.config import DevelopmentConfig, ProdConfig, TestConfig
from impacts_model import data_model


def handle_validation_exceptions(error):
    """Handle invalid marshmallow validation request exception."""
    # return error.messages, 400
    response = flask.Response()
    # replace the body with JSON
    response.status = 400   
    response.data = json.dumps(error.messages)
    response.content_type = "application/json"
    return response


def create_app(env: str = "") -> flask.app.Flask:
    """
    Flask application factory following
    https://flask.palletsprojects.com/en/2.1.x/patterns/appfactories/
    Follows the env settings passed as parameter, prod by default
    :param: "DEV", "TEST" or none
    :return: a Flask application
    """
    connex_app = connexion.App(__name__, specification_dir=config.basedir)
    connex_app.add_api("swagger.yaml")

    app: flask.app.Flask = connex_app.app

    if env == "DEV":
        app.config.from_object(DevelopmentConfig)
    elif env == "TEST":
        app.config.from_object(TestConfig)
    else:
        app.config.from_object(ProdConfig)
    CORS(app)
    data_model.db.init_app(app)
    data_model.ma.init_app(app)

    with app.app_context():
        data_model.db.create_all()

    # Register validation exceptions
    app.register_error_handler(ValidationError, handle_validation_exceptions)

    return app
