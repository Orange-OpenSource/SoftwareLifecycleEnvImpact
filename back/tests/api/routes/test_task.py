from unittest import mock
from unittest.mock import MagicMock

import pytest
from flask.testing import FlaskClient
from flask_sqlalchemy import SQLAlchemy

from impacts_model.data_model import Model, Project, Task

tasks_root_path = "/api/v1/tasks"


@pytest.fixture(scope="function")
def task_fixture(db: SQLAlchemy) -> Task:
    """Test task fixture"""
    project = Project(name="Project test_task")
    model = Model(name="Model test_task")
    project.models = [model]
    task = Task(name="Test task")
    model.root_task = task
    db.session.add_all([project, model, task])
    db.session.commit()
    return task


def test_get_tasks(client: FlaskClient, task_fixture: Task) -> None:
    """
    Test response of GET /tasks
    :param client: flask client fixture
    :param task_fixture: Task fixture
    """
    all_tasks = Task.query.all()
    response = client.get(tasks_root_path)
    assert response.status_code == 200
    assert len(response.json) == len(all_tasks)


@mock.patch(
    "api.routes.task.get_task_template_by_id",
    MagicMock(return_value=MagicMock()),
)
def test_post_task(client: FlaskClient, task_fixture: Task) -> None:
    """
    Test response of POST /tasks
    :param client: flask client fixture
    :param task_fixture: Task fixture
    """
    response = client.post(
        tasks_root_path,
        json={"name": "Task test post", "parent_task_id": task_fixture.id},
    )

    assert response.status_code == 201
    assert response.json["name"] == "Task test post"
    assert response.json["id"] is not None

    # Test 409 project exists already
    response = client.post(
        tasks_root_path,
        json={
            "name": "Task test post",
            "parent_task_id": task_fixture.id,
        },
    )
    assert response.status_code == 409

    # Test subtasks intserstion
    response = client.post(
        tasks_root_path,
        json={
            "name": "Task with subtask",
            "parent_task_id": task_fixture.id,
        },
    )

    assert response.status_code == 201


def test_get_one_task(client: FlaskClient, db: SQLAlchemy, task_fixture: Task) -> None:
    """
    Test response of GET /tasks/<id>
    :param client: flask client fixture
    :param task_fixture: Task fixture
    """
    # Test with one task
    response = client.get(tasks_root_path + "/" + str(task_fixture.id))
    assert response.status_code == 200
    assert response.json["id"] is task_fixture.id
    assert response.json["name"] == task_fixture.name

    # Test no task 404
    db.session.delete(task_fixture)
    db.session.commit()
    response = client.get(tasks_root_path + "/" + str(task_fixture.id))
    assert response.status_code == 404


def test_patch_task(client: FlaskClient, db: SQLAlchemy, task_fixture: Task) -> None:
    """
    Test response of PATCH /tasks/<id>
    :param client: flask client fixture
    :param db: SQLAlchemy database fixture
    :param task_fixture: Task fixture
    """

    response = client.patch(
        tasks_root_path + "/" + str(task_fixture.id),
        json=[{"op": "replace", "path": "/name", "value": "newer name"}],
    )
    assert response.status_code == 200
    assert response.json["name"] == "newer name"

    # Test wrong patch format
    response = client.patch(
        tasks_root_path + "/" + str(task_fixture.id),
        json=[{"op": "replace", "path": "/nameqqsd", "value": "newer name"}],
    )
    assert response.status_code == 403

    # Test no task 404
    db.session.delete(task_fixture)
    db.session.commit()
    response = client.patch(
        tasks_root_path + "/" + str(task_fixture.id),
        json=[{"op": "replace", "path": "/name", "value": "newer name"}],
    )
    assert response.status_code == 404


def test_delete_task(client: FlaskClient, db: SQLAlchemy, task_fixture: Task) -> None:
    """
    Test response of DELETE /tasks/<id>
    :param client: flask client fixture
    :param db: SQLAlchemy database fixture
    :param task_fixture: Task fixture
    """

    # Test to delete root task
    model = Model.query.filter(Model.root_task_id == task_fixture.id).one_or_none()
    model.root_task = task_fixture
    response = client.delete(tasks_root_path + "/" + str(task_fixture.id))
    assert response.status_code == 403
    model.root_task = None

    # Test nominal

    response = client.delete(tasks_root_path + "/" + str(task_fixture.id))
    assert response.status_code == 200

    # Test that task is deleted
    response = client.get(tasks_root_path + "/" + str(task_fixture.id))
    assert response.status_code == 404

    # Test no task 404
    response = client.delete(tasks_root_path + "/" + str(task_fixture.id))
    assert response.status_code == 404


def test_get_task_impacts(
    client: FlaskClient, db: SQLAlchemy, task_fixture: Task
) -> None:
    """
    Test response of GET /tasks/<id>/impacts
    :param client: flask client fixture
    :param db: SQLAlchemy database fixture
    :param task_fixture: Task fixture
    """
    response = client.get(tasks_root_path + "/" + str(task_fixture.id) + "/impacts")
    assert response.status_code == 200
