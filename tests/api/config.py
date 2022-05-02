import pytest

from api.config import connex_app


@pytest.fixture()
def app():
    connex_app.add_api("swagger.yaml")

    connex_app.config.update({
        "TESTING": True,
    })
    yield connex_app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
