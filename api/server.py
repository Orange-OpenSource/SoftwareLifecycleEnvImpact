import connexion
import flask
from flask_cors import CORS

from api import config, data_model


def create_app() -> flask.app.Flask:
    """
    Flask application factory following
    https://flask.palletsprojects.com/en/2.1.x/patterns/appfactories/
    :return: a Flask application
    """
    connex_app = connexion.App(__name__, specification_dir=config.basedir)
    connex_app.add_api("swagger.yaml")

    app: flask.app.Flask = connex_app.app
    app.config.from_pyfile("config.py")
    CORS(app)
    data_model.db.init_app(app)
    data_model.ma.init_app(app)

    return app
