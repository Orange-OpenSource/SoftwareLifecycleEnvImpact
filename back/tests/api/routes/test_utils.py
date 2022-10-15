from flask.testing import FlaskClient
from tests.api.routes.test_project import projects_root
from tests.api.routes.test_model import models_root
from tests.api.routes.test_task import tasks_root_path

debug_root = "/api/v1/debug"


def test_reset_db(client: FlaskClient) -> None:
    """
    Test response of GET /debug/reset
    :param client: flask client fixture
    """

    response = client.get(debug_root + "/reset")
    assert response.status_code == 204


def test_impact(client: FlaskClient) -> None:
    """
    Test that after GET /debug/reset the impact can be computed
    :param client: flask client fixture
    """
    client.get(debug_root + "/reset")
    models = client.get(projects_root)
    # response = client.get(models_root + "/" + str(model_fixture.id) + "/impact")
    # assert response.status_code == 200
    # response = client.get(tasks_root_path + "/" + str(task_fixture.id) + "/impacts")
    # assert response.status_code == 200
    # TODO should test the impact on a big project
