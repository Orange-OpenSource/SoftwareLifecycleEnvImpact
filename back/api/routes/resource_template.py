from typing import Any

from impacts_model.templates import (
    get_resources_templates,
    ResourceTemplateSchema,
)


def get_resource_templates() -> Any:
    """
    GET /resourcetemplates/
    :return: all Resource templates from the model
    """
    templates = get_resources_templates()

    # Serialize
    project_schema = ResourceTemplateSchema(many=True)
    return project_schema.dump(templates)
