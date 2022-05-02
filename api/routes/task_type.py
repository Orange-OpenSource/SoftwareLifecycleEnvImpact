from typing import Any

from flask import abort

from api.data_model import TaskType, TaskTypeSchema


def get_task_types() -> Any:
    """
    POST /tasktypes/
    :return: all TaskType in the database
    """
    task_types = TaskType.query.all()
    task_type_schema = TaskTypeSchema(many=True)

    return task_type_schema.dump(task_types)


def get_task_type(task_type_id: int) -> Any:
    """
    POST /tasktypes/<task_type_id>
    :return: TaskType if it exists with id, 404 else
    """
    task_type = TaskType.query.filter(TaskType.id == task_type_id).one_or_none()

    if task_type is not None:
        task_schema = TaskTypeSchema()
        return task_schema.dump(task_type)
    else:
        return abort(
            404,
            "No task type found for Id: {task_type_id}".format(
                task_type_id=task_type_id
            ),
        )
