import pytest
from flask import Flask
from flask.testing import FlaskClient

from api.server import create_app

models_root = "/api/v1/models"


@pytest.fixture
def app() -> Flask:
    """
    Fixture for the flask server
    :return: A flask client
    """
    return create_app()


def test_get_models(app: FlaskClient) -> None:
    """
    Test response of GET /models
    :param client: flask client fixture
    """
    response = app.get(models_root)
    assert response.status_code == 200


def test_get_one_model(client: FlaskClient) -> None:
    """
    Test response of GET /models/<id>
    :param client: flask client fixture
    """
    response = client.get(models_root + "/0")
    assert response.status_code == 200


def test_get_model_tasks(client: FlaskClient) -> None:
    """
    Test response of GET /models/<id>/tasks
    :param client: flask client fixture
    """
    response = client.get(models_root + "/0/tasks")
    assert response.status_code == 200
