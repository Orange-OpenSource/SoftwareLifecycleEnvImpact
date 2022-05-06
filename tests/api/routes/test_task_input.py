import pytest
from flask.testing import FlaskClient
from flask_sqlalchemy import SQLAlchemy

from api.data_model import Model, Project, Task, TaskInput, TaskType

tasks_inputs_root = "/api/v1/taskinputs"


@pytest.fixture(scope="function")
def task_input_fixture(db: SQLAlchemy):
    project = Project(name="Project test_task")
    model = Model(name="Model test_task")
    project.models = [model]
    task_type = TaskType(name="Tasktype test_task ")
    task = Task(name="Test task")
    model.tasks = [task]
    task.task_type = task_type
    task_input = TaskInput(name="TaskInput test", kind="kind")
    task.inputs = [task_input]
    db.session.add_all([project, model, task_type, task, task_input])
    db.session.commit()
    return task_input


def test_get_inputs(client: FlaskClient, task_input_fixture: TaskInput) -> None:
    """
    Test response of GET /taskinputs
    :param client: flask client fixture
    :param task_input_fixture: Task input fixture
    """
    task_inputs = TaskInput.query.all()
    response = client.get(tasks_inputs_root)
    assert response.status_code == 200
    assert len(response.json) == len(task_inputs)


def test_get_one_task_input(
    client: FlaskClient, db: SQLAlchemy, task_input_fixture: TaskInput
) -> None:
    """
    Test response of GET /taskinputs/<id>
    :param client: flask client fixture
    :param db: SQLAlchemy database fixture
    :param task_input_fixture: Task input fixture
    """
    response = client.get(tasks_inputs_root + "/" + str(task_input_fixture.id))
    assert response.status_code == 200
    assert response.json["id"] is task_input_fixture.id
    assert response.json["name"] == task_input_fixture.name

    # Test no task input 404
    db.session.delete(task_input_fixture)
    db.session.commit()
    response = client.get(tasks_inputs_root + "/" + str(task_input_fixture.id))
    assert response.status_code == 404


def test_patch_task_input(
    client: FlaskClient, db: SQLAlchemy, task_input_fixture: TaskInput
) -> None:
    """
    Test response of PATCH /taskinputs/<id>
    :param client: flask client fixture
    :param db: SQLAlchemy database fixture
    :param task_input_fixture: Task input fixture
    """

    response = client.patch(
        tasks_inputs_root + "/" + str(task_input_fixture.id),
        json=[{"op": "replace", "path": "/name", "value": "newer name"}],
    )
    assert response.status_code == 200
    assert response.json["name"] == "newer name"

    # Test wrong patch format
    response = client.patch(
        tasks_inputs_root + "/" + str(task_input_fixture.id),
        json=[{"op": "replace", "path": "/nameqqsd", "value": "newer name"}],
    )
    assert response.status_code == 403

    # Test no task input 404
    db.session.delete(task_input_fixture)
    db.session.commit()
    response = client.patch(
        tasks_inputs_root + "/" + str(task_input_fixture.id),
        json=[{"op": "replace", "path": "/name", "value": "newer name"}],
    )
    assert response.status_code == 404


def test_delete_task_input(client: FlaskClient, task_input_fixture: TaskInput) -> None:
    """
    Test response of DELETE /taskinputs/<id>
    :param client: flask client fixture
    :param task_input_fixture: Task input fixture
    """
    response = client.delete(tasks_inputs_root + "/" + str(task_input_fixture.id))
    assert response.status_code == 200

    # Test that model is deleted
    response = client.get(tasks_inputs_root + "/" + str(task_input_fixture.id))
    assert response.status_code == 404

    # Test no model 404
    response = client.delete(tasks_inputs_root + "/" + str(task_input_fixture.id))
    assert response.status_code == 404
