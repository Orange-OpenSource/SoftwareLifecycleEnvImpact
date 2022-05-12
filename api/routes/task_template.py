from typing import Any

from impacts_model.tasks import get_tasks_templates, TaskTemplate


def json_task_template(task_template: TaskTemplate) -> dict[str, Any]:
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

    for template in get_tasks_templates():
        return_json.append(json_task_template(template))

    return return_json

    # return templates.get_tasks_templates()
