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
    EnvironmentalImpactSchema,
    TaskImpact,
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


def get_task_impacts(task_id: int) -> Any:  # TODO update test
    """
    GET /tasks/<task_id>/impacts
    Get a task environmental impact
    :param task_id: the id of the task to get the impact
    :return: TaskImpact if task exist, 404 else
    """
    task = Task.query.filter(Task.id == task_id).one_or_none()

    if task is not None:
        task_impact = TaskImpact(
            task_id,
            task.get_environmental_impact(),
            task.get_subtasks_impact(),
            task.get_impact_by_resource_type(),
        )
        schema = TaskImpactSchema()
        return schema.dump(task_impact)
    else:
        return abort(
            404,
            "No task found for Id: {task_id}".format(task_id=task_id),
        )


def get_task_subtasks_impacts(task_id: int) -> Any:
    task = Task.query.filter(Task.id == task_id).one_or_none()

    if task is not None:
        impacts_list = []
        for subtask in task.subtasks:
            impacts_list.append(subtask.get_environmental_impact())
        schema = EnvironmentalImpactSchema(many=True)
        return schema.dump(impacts_list)
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
    else:
        return abort(
            404,
            "No task found for Id: {task_id}".format(task_id=task_id),
        )


def insert_task_db(
    new_task: Task, template_id: Optional[int] = None
) -> None:  # TODO remove from here
    if template_id is not None:
        task_template: TaskTemplate = get_task_template_by_id(template_id)

        for impact_source in task_template.impact_sources:
            new_task.resources.append(
                Resource(
                    impact_source_id=impact_source.id,
                    input=1,
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
