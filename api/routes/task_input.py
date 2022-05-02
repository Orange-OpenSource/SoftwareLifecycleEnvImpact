from typing import Any

from flask import abort

from api.data_model import TaskInput, TaskInputSchema


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
