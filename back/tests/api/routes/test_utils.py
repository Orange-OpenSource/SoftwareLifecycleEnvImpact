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
    model_id = models.json[0]["models"][0]["id"] # retrieve the id of the first model
    
    response = client.get(models_root + "/" + str(model_id) + "/impact")
    assert response.status_code == 200
