from typing import Any

import jsonpatch
from flask import abort, request

from impacts_model.data_model import (
    db,
    Model,
    Resource,
    Task,
    TaskSchema,
)
from impacts_model.impacts import (
    TaskImpactSchema,
)
from impacts_model.templates import get_task_template_by_id, TaskTemplate
from typing import Optional


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
    task = db.session.query(Task).get_or_404(task_id)
    task_schema = TaskSchema()
    return task_schema.dump(task)


def update_task(task_id: int) -> Any:
    """
    PATCH /tasks/<task_id>
    Update the task with the A JSONPatch as defined by RFC 6902 in the body
    :param task_id: the id of the task to update
    :return: The updated task if it exists with id, 403 if the JSONPatch format is incorrect, 404 else
    """
    task = db.session.query(Task).get_or_404(task_id)
    old_parent = task.parent_task_id  # Parent task a to be saved before patch

    try:
        task_schema = TaskSchema()
        data = task_schema.dump(task)

        patch = jsonpatch.JsonPatch(request.json)
        data = patch.apply(data)
        task = task_schema.load(data)

        for operation in patch:
            if operation["path"] == "/parent_task_id":
                _exchange_parent(int(operation["value"]), task, old_parent)
        db.session.commit()

        return task_schema.dump(task)
    except jsonpatch.JsonPatchConflict:
        return abort(403, "Patch format is incorrect")


def _exchange_parent(parent_id_to_set: int, task: Task, old_parent_id: int) -> None:
    # Check when changing the parent of a task, if its by one of its subtasks
    # If it is, it will set the subtask parent as this of the task
    # For a tree 1 -> 2 -> 3 and task 2 goes under 3, 3 parent will be set as 1
    # Recursive to check for all subtasks

    # Iterate through subtasks
    for i in range(len(task.subtasks)):
        # Recursive call for each subtask
        _exchange_parent(parent_id_to_set, task.subtasks[i], task.parent_task_id)

        # If subtask id is the one we want to set as parent
        if task.subtasks[i].id == parent_id_to_set:
            # Replace subtask id by this of the task parent
            task.subtasks[i].parent_task_id = old_parent_id


def get_task_impacts(task_id: int) -> Any:
    """
    GET /tasks/<task_id>/impacts
    Get a task environmental impact
    :param task_id: the id of the task to get the impact
    :return: TaskImpact if task exist, 404 else
    """
    task: Task = db.session.query(Task).get_or_404(task_id)
    task_impact = task.get_impact()
    schema = TaskImpactSchema()
    return schema.dump(task_impact)


def delete_task(task_id: int) -> Any:
    """
    DELETE /tasks/<task_id>
    :param task_id: the id of the task to delete
    :return: 200 if the task exists and is deleted, 404 else
    """
    task = db.session.query(Task).get_or_404(task_id)

    model = Model.query.filter(Model.root_task_id == task.id).one_or_none()
    if model != None:
        return abort(
            403,
            "Cannot delete task {task_id} as it is the root of model {model}".format(
                task_id=task_id, model=model.root_task_id
            ),
        )
    db.session.delete(task)
    db.session.commit()
    return 200


def insert_task_db(
    new_task: Task, template_id: Optional[int] = None
) -> None:  # TODO remove from here
    if template_id is not None:
        task_template: TaskTemplate = get_task_template_by_id(template_id)

        for impact_source in task_template.impact_sources:
            new_task.resources.append(
                Resource(
                    impact_source_id=impact_source.id,
                    amount=1,
                )
            )

    db.session.add(new_task)
    db.session.commit()


def create_task_from_template(task: dict[str, Any]) -> Any:
    """
    POST /tasks/templates

    :param task: task to add
    :return: the task inserted with its id
    """
    name = task.get("name")
    parent_task_id = task.get("parent_task_id")
    template_id = task.get("template_id")

    existing_task = (
        Task.query.filter(Task.name == name)
        .filter(Task.parent_task_id == parent_task_id)
        .one_or_none()
    )

    if existing_task is None:
        schema = TaskSchema()
        task.pop("template_id")
        new_task = schema.load(task)
        insert_task_db(new_task, template_id)
        data = schema.dump(new_task)
        return data, 201
    else:
        return abort(
            409,
            "Task {task} exists already".format(task=task),
        )


def create_task(task: dict[str, Any]) -> Any:
    """
    POST /tasks/

    :param task: task to add
    :return: the task inserted with its id
    """
    name = task.get("name")
    parent_task_id = task.get("parent_task_id")

    existing_task = (
        Task.query.filter(Task.name == name)
        .filter(Task.parent_task_id == parent_task_id)
        .one_or_none()
    )

    if existing_task is None:
        schema = TaskSchema()
        new_task = schema.load(task)
        insert_task_db(new_task)
        data = schema.dump(new_task)
        return data, 201
    else:
        return abort(
            409,
            "Task {task} exists already".format(task=task),
        )
