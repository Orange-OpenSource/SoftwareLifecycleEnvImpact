from flask.testing import FlaskClient
from impacts_model.impact_sources import impact_sources

impact_sources_root = "/api/v1/impactsources"


def test_get_impact_sources(client: FlaskClient) -> None:
    """
    Test response of GET /impactsources
    Return the id and name of all impact sources
    :param client: flask client fixture
    """
    impact_source_dict = {}
    for impact_source in impact_sources:
        impact_source_dict[impact_source.id] = impact_source.name
    response = client.get(impact_sources_root)
    assert response.status_code == 200
    assert len(response.json) == len(impact_source_dict)
