from flask.testing import FlaskClient
from impacts_model.impact_sources import impact_sources

impact_sources_root = "/api/v1/impactsources"


def test_get_impact_sources(client: FlaskClient) -> None:
    """
    Test response of GET /impactsources
    :param client: flask client fixture
    """
    all_impact_sources = impact_sources
    response = client.get(impact_sources_root)
    assert response.status_code == 200
    assert len(response.json) == len(all_impact_sources)
