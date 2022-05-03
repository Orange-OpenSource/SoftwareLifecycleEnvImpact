from typing import Any

import jsonpatch
from flask import abort, request

from api.data_model import db, Task, TaskSchema


def get_tasks() -> Any:
    """
    GET /tasks/
    :return: all Task in the database
    """
    tasks = Task.query.all()

    task_schema = TaskSchema(many=True)
    return task_schema.dump(tasks)


def get_task(task_id: int) -> Any:
    """
    GET /tasks/<task_id>
    :return: Task if it exists with id, 404 else
    """
    task = Task.query.filter(Task.id == task_id).one_or_none()

    if task is not None:
        task_schema = TaskSchema()
        return task_schema.dump(task)
    else:
        return abort(
            404,
            "No task found for Id: {task_id}".format(task_id=task_id),
        )


def update_task(task_id: int) -> Any:
    """
    PATCH /tasks/<task_id>
    Update the task with the A JSONPatch as defined by RFC 6902 in the body
    :param task_id: the id of the task to update
    :return: The updated task if it exists with id, 403 if the JSONPatch format is incorrect, 404 else
    """
    task = Task.query.filter(Task.id == task_id).one_or_none()

    if task is not None:
        try:
            task_schema = TaskSchema()
            data = task_schema.dump(task)

            patch = jsonpatch.JsonPatch(request.json)
            data = patch.apply(data)

            model = task_schema.load(data)
            db.session.commit()

            return task_schema.dump(model)
        except jsonpatch.JsonPatchConflict:
            return abort(403, "Patch format is incorrect")
    else:
        return abort(
            404,
            "No task found for Id: {task_id}".format(task_id=task_id),
        )


def delete_task(task_id: int) -> Any:
    """
    DELETE /tasks/<task_id>
    :param task_id: the id of the task to delete
    :return: 200 if the task exists and is deleted, 404 else
    """
    task = Task.query.filter(Task.id == task_id).one_or_none()

    if task is not None:
        db.session.delete(task)
        db.session.commit()
        return 200
    else:
        return abort(
            404,
            "No task found for Id: {task_id}".format(task_id=task_id),
        )


def create_task(task: dict[str, Any]) -> Any:
    """
    POST /tasks/

    :param task: task to add
    :return: the task inserted with its id
    """
    name = task.get("name")
    parent_task_id = task.get("parent_task_id")
    task_type_id = task.get("task_type_id")
    model_id = task.get("model_id")

    existing_task = (
        Task.query.filter(Task.name == name)
        .filter(Task.task_type_id == task_type_id)
        .filter(Task.parent_task_id == parent_task_id)
        .filter(Task.model_id == model_id)
        .one_or_none()
    )

    if existing_task is None:
        schema = TaskSchema()
        new_task = schema.load(task)

        db.session.add(new_task)
        db.session.commit()

        data = schema.dump(new_task)

        return data, 201
    else:
        return abort(
            409,
            "Task {task} exists already".format(task=task),
        )
