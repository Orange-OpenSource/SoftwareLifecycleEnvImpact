from typing import Any

import jsonpatch
from flask import abort, request

from impacts_model.data_model import db, Resource, ResourceSchema, Task
from impacts_model.impacts import EnvironmentalImpactSchema


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
    name = resource.get("name")
    task_id = resource.get("task_id")
    impact_source_id = resource.get("impact_source_id") # TODO this should use the resourceSchema directly
    input = resource.get("input")

    existing_resource = (
        Resource.query.filter(Resource.name == name)
        .filter(Resource.task_id == task_id)
        .one_or_none()
    )
    existing_task = Task.query.filter(Task.id == task_id).one_or_none()

    if existing_resource is None and existing_task is not None:

        resource = Resource(
            name=name,
            task_id=task_id,
            impact_source_id=impact_source_id, # TODO this should use the resourceSchema
            input=input,
        )
        db.session.add(resource)
        db.session.commit()

        schema = ResourceSchema()
        data = schema.dump(resource)
        return data, 201
    else:
        return abort(
            409,
            "Resource {resource} exists already".format(resource=name),
        )


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


def delete_resource(resource_id: int) -> Any:
    """
    DELETE /resources/<resource_id>
    :param resource_id: the id of the resource to delete
    :return: 200 if the resource exists and is deleted, 404 else
    """
    resource = Resource.query.filter(Resource.id == resource_id).one_or_none()

    if resource is not None:
        db.session.delete(resource)
        db.session.commit()
        return 200
    else:
        return abort(
            404,
            "No resource found for Id: {resource_id}".format(resource_id=resource_id),
        )


def get_resource_impacts(resource_id: int):
    resource = Resource.query.filter(Resource.id == resource_id).one_or_none()

    if resource is not None:
        environmental_impact = resource.get_environmental_impact()
        schema = EnvironmentalImpactSchema()
        return schema.dump(environmental_impact)
    else:
        return abort(
            404,
            "No resource found for Id: {resource_id}".format(resource_id=resource_id),
        )
