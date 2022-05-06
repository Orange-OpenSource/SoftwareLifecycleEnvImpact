from typing import Any

import jsonpatch
from flask import abort, request

from api.data_model import db, TaskInput, TaskInputSchema


def get_task_inputs() -> Any:
    """
    GET /taskinputs/
    :return: all TaskInput in the database
    """
    task_inputs = TaskInput.query.all()
    task_input_schema = TaskInputSchema(many=True)

    return task_input_schema.dump(task_inputs)


def get_task_input(task_input_id: int) -> Any:
    """
    GET /taskinputs/<task_input_id>
    :return: TaskInput if it exists with id, 404 else
    """
    task_input = TaskInput.query.filter(TaskInput.id == task_input_id).one_or_none()

    if task_input is not None:
        task_schema = TaskInputSchema()
        return task_schema.dump(task_input)
    else:
        return abort(
            404,
            "No task input found for Id: {task_input_id}".format(
                task_input_id=task_input_id
            ),
        )


def update_task_input(task_input_id: int) -> Any:
    """
    PATCH /taskinputs/<task_input_id>
    Update the task_input with the A JSONPatch as defined by RFC 6902 in the body
    :param task_input_id: the id of the task input to update
    :return: The updated task input if it exists with id, 403 if the JSONPatch format is incorrect, 404 else
    """
    task_input = TaskInput.query.filter(TaskInput.id == task_input_id).one_or_none()

    if task_input is not None:
        try:
            task_schema = TaskInputSchema()
            data = task_schema.dump(task_input)

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
            "No task input found for Id: {task_input_id}".format(
                task_input_id=task_input_id
            ),
        )


def delete_task_input(task_input_id: int) -> Any:
    """
    DELETE /taskinputs/<task_input_id>
    :param task_input_id: the id of the task input to delete
    :return: 200 if the task input exists and is deleted, 404 else
    """
    task_input = TaskInput.query.filter(TaskInput.id == task_input_id).one_or_none()

    if task_input is not None:
        db.session.delete(task_input)
        db.session.commit()
        return 200
    else:
        return abort(
            404,
            "No task input found for Id: {task_input_id}".format(
                task_input_id=task_input_id
            ),
        )


def create_task_input(task_input: dict[str, Any]) -> Any:
    """
    POST /taskinputs/

    :param task_input: task input to add
    :return: the task input inserted with its id
    """
    name = task_input.get("name")
    kind = task_input.get("kind")
    value = task_input.get("value")
    task_id = task_input.get("task_id")

    existing_task_input = (
        TaskInput.query.filter(TaskInput.name == name)
        .filter(TaskInput.kind == kind)
        .filter(TaskInput.value == value)
        .filter(TaskInput.task_id == task_id)
        .one_or_none()
    )

    if existing_task_input is None:
        schema = TaskInputSchema()
        new_task_input = schema.load(task_input)

        db.session.add(new_task_input)
        db.session.commit()

        data = schema.dump(new_task_input)

        return data, 201
    else:
        return abort(
            409,
            "Task task input {task_input} exists already".format(task_input=task_input),
        )
