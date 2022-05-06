import connexion
import flask
from flask_cors import CORS

from api import config, data_model
from api.config import DevelopmentConfig, ProdConfig, TestConfig


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

    return app
