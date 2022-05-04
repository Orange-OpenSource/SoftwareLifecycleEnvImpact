import pytest
from flask import Flask
from flask.testing import FlaskClient

from api.server import create_app

tasks_inputs_root = "/api/v1/taskinputs"


@pytest.fixture
def app() -> Flask:
    """
    Fixture for the flask server
    :return: A flask client
    """
    return create_app()


def test_get_inputs(client: FlaskClient) -> None:
    """
    Test response of GET /taskinputs
    :param client: flask client fixture
    """
    response = client.get(tasks_inputs_root)
    assert response.status_code == 200


def test_get_one_input(client: FlaskClient) -> None:
    """
    Test response of GET /taskinputs/<id>
    :param client: flask client fixture
    """
    response = client.get(tasks_inputs_root + "/0")
    assert response.status_code == 200
