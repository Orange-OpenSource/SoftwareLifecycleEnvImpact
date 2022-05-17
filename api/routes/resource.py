from typing import Any

import jsonpatch
from flask import abort, request

from api.data_model import db, Resource, ResourceSchema
from impacts_model.computation import get_resource_environmental_impact
from impacts_model.impacts import EnvironmentalImpactSchema


def get_resources() -> Any:
    """
    GET /resources/
    :return: all Resource in the database
    """
    resources = Resource.query.all()

    resource_schema = ResourceSchema(many=True)
    return resource_schema.dump(resources)

def get_resource(resource_id: int) -> Any:
    """
    GET /resources/<resource_id>
    :param resource_id: Id of the resource to get
    :return: Resource if it exists with id, 404 else
    """
    resource = Resource.query.filter(Resource.id == resource_id).one_or_none()

    if resource is not None:
        resource_schema = ResourceSchema()
        return resource_schema.dump(resource)
    else:
        return abort(
            404,
            "No resource found for Id: {resource_id}".format(resource_id=resource_id),
        )

def update_resource(resource_id: int) -> Any:
    """
    PATCH /resources/<resource_id>
    Update the resource with the A JSONPatch as defined by RFC 6902 in the body
    :param resource_id: the id of the resource to update
    :return: The updated resource if it exists with id, 403 if the JSONPatch format is incorrect, 404 else
    """
    resource = Resource.query.filter(Resource.id == resource_id).one_or_none()

    if resource is not None:
        try:
            resource_schema = ResourceSchema()
            data = resource_schema.dump(resource)

            patch = jsonpatch.JsonPatch(request.json)
            data = patch.apply(data)

            updated_resource = resource_schema.load(data)
            db.session.commit()

            return resource_schema.dump(updated_resource)
        except jsonpatch.JsonPatchConflict:
            return abort(403, "Patch format is incorrect")
    else:
        return abort(
            404,
            "No resource found for Id: {resource_id}".format(resource_id=resource_id),
        )

def get_resource_impacts(resource_id: int):
    resource = Resource.query.filter(Resource.id == resource_id).one_or_none()

    if resource is not None:
        environmental_impact = get_resource_environmental_impact(resource)
        schema = EnvironmentalImpactSchema()
        return schema.dump(environmental_impact)
    else:
        return abort(
            404,
            "No resource found for Id: {resource_id}".format(resource_id=resource_id),
        )