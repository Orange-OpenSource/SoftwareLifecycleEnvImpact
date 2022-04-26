from flask import abort

from data_model import TaskInput, TaskInputSchema


def get_task_inputs():
    task_inputs = TaskInput.query.all()
    task_input_schema = TaskInputSchema(many=True)

    return task_input_schema.dump(task_inputs)


def get_task_input(task_input_id):
    task_input = TaskInput.query.filter(TaskInput.id == task_input_id).one_or_none()

    if task_input is not None:
        task_schema = TaskInputSchema()
        return task_schema.dump(task_input)
    else:
        abort(
            404,
            "No task input found for Id: {task_input_id}".format(
                task_input_id=task_input_id
            ),
        )
