from flask import abort

from data_model import TaskType, TaskTypeSchema


def get_task_types():
    task_types = TaskType.query.all()
    task_type_schema = TaskTypeSchema(many=True)

    return task_type_schema.dump(task_types)


def get_task_type(task_type_id):
    task_type = TaskType.query.filter(TaskType.id == task_type_id).one_or_none()

    if task_type is not None:
        task_schema = TaskTypeSchema()
        return task_schema.dump(task_type)
    else:
        abort(
            404,
            "No task type found for Id: {task_type_id}".format(
                task_type_id=task_type_id
            ),
        )
