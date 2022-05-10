from typing import Any

from model import templates
from model.tasks import TaskTemplate


def json_task_template(task_template: TaskTemplate):
    # TODO maybe move ?
    return {
        "name": task_template.name,
        "subtasks": [json_task_template(t) for t in task_template.subtasks],
        "resources": [{"name": r.name} for r in task_template.resources],
    }


def get_task_templates() -> Any:
    """
    GET /tasktemplates/
    :return: all Task templates from the model
    """
    # TODO implement a chache mecanism
    return_json = []

    for template in templates.get_tasks_templates():
        return_json.append(json_task_template(template))

    return return_json

    # return templates.get_tasks_templates()
