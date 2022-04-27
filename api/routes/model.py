from flask import abort

from config import db
from data_model import Model, ModelSchema
from routes.task import get_task


def get_models():
    models = Model.query.all()

    model_schema = ModelSchema(many=True)
    return model_schema.dump(models)


def get_model(model_id):
    model = Model.query.filter(Model.id == model_id).one_or_none()

    if model is not None:
        model_schema = ModelSchema()
        return model_schema.dump(model)
    else:
        abort(
            404,
            "No model found for Id: {model_id}".format(model_id=model_id),
        )

def get_tasks(model_id):
    model = Model.query.filter(Model.id == model_id).one_or_none()

    if model is not None:
        return get_task(model.root_task_id)
    else:
        abort(
            404,
            "No model found for Id: {model_id}".format(model_id=model_id),
        )

def create_model(model):
    name = model.get("name")
    project_id = model.get("project_id")

    existing_model = (
        Model.query.filter(Model.name == name)
        .filter(Model.project_id == project_id)
        .one_or_none()
    )

    if existing_model is None:
        schema = ModelSchema()
        new_model = schema.load(model, session=db.session)

        db.session.add(new_model)
        db.session.commit()

        data = schema.dump(new_model)

        return data, 201
    else:
        abort(
            409,
            "Model {name} exists already".format(name=name),
        )
