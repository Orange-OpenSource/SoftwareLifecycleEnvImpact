# BSD-3-Clause License
#
# Copyright 2017 Orange
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

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
