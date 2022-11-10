from typing import Any

from impacts_model.templates import (
    load_tasks_templates,
    TaskTemplateSchema,
)


def get_task_templates() -> Any:
    """
    GET /tasktemplates/
    :return: all Task templates from the model
    """

    templates = load_tasks_templates()

    # Serialize
    project_schema = TaskTemplateSchema(many=True)
    return project_schema.dump(templates)
