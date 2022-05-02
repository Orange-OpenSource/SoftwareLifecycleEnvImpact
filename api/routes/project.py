from typing import Any

from flask import abort

from api.config import db
from api.data_model import Model, ModelSchema, Project, ProjectSchema, Task


def get_projects() -> Any:
    """
    GET /projects/
    :return: all Project in the database
    """
    # Create the list from data
    projects = Project.query.all()

    # Serialize
    project_schema = ProjectSchema(many=True)
    return project_schema.dump(projects)


def get_project(project_id: int) -> Any:
    """
    GET /project/<project_id>
    :param project_id: id of the project to get
    :return: Project if it exists with id, 404 else
    """
    project = Project.query.filter(Project.id == project_id).one_or_none()

    if project is not None:
        project_schema = ProjectSchema()
        return project_schema.dump(project)
    else:
        return abort(
            404,
            "No project found for Id: {project_id}".format(project_id=project_id),
        )


def create_project(project: dict[str, Any]) -> Any:
    """
    POST /projects/

    :param project: project to add
    :return: the project inserted with its id
    """
    name = project.get("name")

    existing_project = Project.query.filter(Project.name == name).one_or_none()

    if existing_project is None:
        schema = ProjectSchema()
        new_project = schema.load(project, session=db.session)

        root_task = Task(
            name=name,
            task_type_id=0,  # Root task type, # TODO replace by new api architecture
        )

        model = Model(
            name=name,
        )

        model.root_task = root_task
        model.tasks = [root_task]
        new_project.base_model = model
        new_project.models = [model]

        db.session.add_all([new_project, model])

        db.session.commit()

        data = schema.dump(new_project)

        return data, 201
    else:
        return abort(
            409,
            "Project {name} exists already".format(name=name),
        )


def get_models(project_id: int) -> Any:
    """
    /projects/{project_id}/models
    :param project_id: id of the project to get the models
    :return: All the models for the project id
    """
    project = Project.query.filter(Project.id == project_id).one_or_none()

    if project is not None:
        model_schema = ModelSchema(many=True)
        return model_schema.dump(project.models)
    else:
        return abort(
            404,
            "No project found for Id: {project_id}".format(project_id=project_id),
        )
