from typing import Any

from impacts_model.templates import (
    load_activities_templates,
    ActivityTemplateSchema,
)


def get_activity_templates() -> Any:
    """
    GET /activities/templates
    :return: all Activity templates from the model
    """

    templates = load_activities_templates()

    # Serialize
    project_schema = ActivityTemplateSchema(many=True)
    return project_schema.dump(templates)
