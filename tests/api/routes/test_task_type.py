import pytest
from flask import Flask
from flask.testing import FlaskClient

from api.server import create_app

tasks_type_root = "/api/v1/tasktypes"


@pytest.fixture
def app() -> Flask:
    """
    Fixture for the flask server
    :return: A flask client
    """
    return create_app()


def test_get_task_types(client: FlaskClient) -> None:
    """
    Test response of GET /tasktypes
    :param client: flask client fixture
    """
    response = client.get(tasks_type_root)
    assert response.status_code == 200


def test_get_one_task_types(client: FlaskClient) -> None:
    """
    Test response of GET /tasktypes/<id>
    :param client: flask client fixture
    """
    response = client.get(tasks_type_root + "/0")
    assert response.status_code == 200
