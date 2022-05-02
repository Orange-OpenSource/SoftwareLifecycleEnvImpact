import connexion
from flask_cors import CORS

from api import config, data_model


def create_app():
    connex_app = connexion.App(__name__, specification_dir=config.basedir)
    connex_app.add_api("swagger.yaml")

    app = connex_app.app
    app.config.from_pyfile("config.py")
    CORS(app)
    data_model.db.init_app(app)
    data_model.ma.init_app(app)

    return app
