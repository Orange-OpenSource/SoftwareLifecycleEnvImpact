import pytest
from flask import Flask
from flask.testing import FlaskClient

from api.server import create_app

projects_root = "/api/v1/projects"


@pytest.fixture
def app() -> Flask:
    """
    Fixture for the flask server
    :return: A flask client
    """
    return create_app()


def test_get_projects(client: FlaskClient) -> None:
    """
    Test response of GET /projects
    :param client: flask client fixture
    """
    response = client.get(projects_root)
    assert response.status_code == 200


def test_get_one_project(client: FlaskClient) -> None:
    """
    Test response of GET /project/<id>
    :param client: flask client fixture
    """
    response = client.get(projects_root + "/0")
    assert response.status_code == 200


def test_get_project_models(client: FlaskClient) -> None:
    """
    Test response of GET /project/<id>/models
    :param client: flask client fixture
    """
    response = client.get(projects_root + "/0/models")
    assert response.status_code == 200
