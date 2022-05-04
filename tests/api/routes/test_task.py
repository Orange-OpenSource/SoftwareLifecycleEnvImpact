import pytest
from flask import Flask
from flask.testing import FlaskClient

from api.server import create_app

tasks_root = "/api/v1/tasks"


@pytest.fixture
def app() -> Flask:
    """
    Fixture for the flask server
    :return: A flask client
    """
    return create_app()


def test_get_tasks(client: FlaskClient) -> None:
    """
    Test response of GET /tasks
    :param client: flask client fixture
    """
    response = client.get(tasks_root)
    assert response.status_code == 200


def test_get_one_task(client: FlaskClient) -> None:
    """
    Test response of GET /tasks/<id>
    :param client: flask client fixture
    """
    response = client.get(tasks_root + "/0")
    assert response.status_code == 200
