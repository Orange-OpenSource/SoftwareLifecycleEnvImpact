from typing import Any

import jsonpatch
from flask import abort, request

from impacts_model.data_model import db, Resource, ResourceSchema, Activity
from impacts_model.impacts import ImpactSourceImpactSchema


def get_resources() -> Any:
    """
    GET /resources/
    :return: all Resource in the database
    """
    resources = Resource.query.all()

    resource_schema = ResourceSchema(many=True)
    return resource_schema.dump(resources)


def create_resource(resource: dict[str, Any]) -> Any:
    """
    POST /resources/

    :param resource: resource to create
    :return: the resource inserted with its id
    """

    activity_id = resource.get("activity_id")

    existing_activity = Activity.query.filter(Activity.id == activity_id).one_or_none()

    if existing_activity is not None:
        schema = ResourceSchema()
        loaded_resource = schema.load(resource)
        db.session.add(loaded_resource)
        db.session.commit()

        data = schema.dump(loaded_resource)
        return data, 201
    else:
        return abort(
            409,
            "Activity does not exist",
        )


def get_resource(resource_id: int) -> Any:
    """
    GET /resources/<resource_id>
    :param resource_id: Id of the resource to get
    :return: Resource if it exists with id, 404 else
    """
    resource = db.session.query(Resource).get_or_404(resource_id)
    resource_schema = ResourceSchema()
    return resource_schema.dump(resource)


def update_resource(resource_id: int) -> Any:
    """
    PATCH /resources/<resource_id>
    Update the resource with the A JSONPatch as defined by RFC 6902 in the body
    :param resource_id: the id of the resource to update
    :return: The updated resource if it exists with id, 403 if the JSONPatch format is incorrect, 404 else
    """
    resource = db.session.query(Resource).get_or_404(resource_id)

    try:
        resource_schema = ResourceSchema()
        data = resource_schema.dump(resource)

        patch = jsonpatch.JsonPatch(request.json)
        data = patch.apply(data)

        resource = resource_schema.load(data)
        db.session.merge(
            resource
        )  # Required for quantites, updates not workging without
        db.session.commit()

        return resource_schema.dump(resource)
    except jsonpatch.JsonPatchConflict:
        return abort(403, "Patch format is incorrect")


def delete_resource(resource_id: int) -> Any:
    """
    DELETE /resources/<resource_id>
    :param resource_id: the id of the resource to delete
    :return: 200 if the resource exists and is deleted, 404 else
    """
    resource = db.session.query(Resource).get_or_404(resource_id)
    db.session.delete(resource)
    db.session.commit()
    return 200


def get_resource_impacts(resource_id: int) -> Any:
    resource = db.session.query(Resource).get_or_404(resource_id)
    environmental_impact = resource.get_impact()
    schema = ImpactSourceImpactSchema()
    return schema.dump(environmental_impact)
