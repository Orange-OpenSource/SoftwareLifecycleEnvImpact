from flask import abort

from config import db
from data_model import Model, ModelSchema, Project, ProjectSchema, Task


def get_projects():
    # Create the list from data
    projects = Project.query.all()

    # Serialize
    project_schema = ProjectSchema(many=True)
    return project_schema.dump(projects)


def get_project(project_id):
    project = Project.query.filter(Project.id == project_id).one_or_none()

    if project is not None:
        project_schema = ProjectSchema()
        return project_schema.dump(project)
    else:
        abort(
            404,
            "No project found for Id: {project_id}".format(project_id=project_id),
        )


def create_project(project):
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
        abort(
            409,
            "Project {name} exists already".format(name=name),
        )


def get_models(project_id):
    project = Project.query.filter(Project.id == project_id).one_or_none()

    if project is not None:
        model_schema = ModelSchema(many=True)
        return model_schema.dump(project.models)
    else:
        abort(
            404,
            "No project found for Id: {project_id}".format(project_id=project_id),
        )
