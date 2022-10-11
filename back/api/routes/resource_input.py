from typing import Any
from impacts_model.data_model import db, ResourceInput, ResourceInputSchema
import jsonpatch
from flask import abort, request


def get_resource_input(resource_input_id: int) -> Any:
    """
    GET /resourceinputs/<resource_input_id>
    :param resource_input_id: Id of the resource input to get
    :return: ResourceInput if it exists with id, 404 else
    """
    resource_input = ResourceInput.query.filter(
        ResourceInput.id == resource_input_id
    ).one_or_none()

    if resource_input is not None:
        resource_input_schema = ResourceInputSchema()
        return resource_input_schema.dump(resource_input)
    else:
        return abort(
            404,
            "No resource input found for Id: {resource_input_id}".format(
                resource_input_id=resource_input_id
            ),
        )


def update_resource_input(resource_input_id: int) -> Any:
    """
    PATCH /resourceinputs/<resource_input_id>
    Update the resource input with the A JSONPatch as defined by RFC 6902 in the body
    :param resource_input_id: the id of the resource input to update
    :return: The updated resource input if it exists with id, 403 if the JSONPatch format is incorrect, 404 else
    """
    resource_input = ResourceInput.query.filter(
        ResourceInput.id == resource_input_id
    ).one_or_none()

    if resource_input is not None:
        try:
            resource_input_schema = ResourceInputSchema()
            data = resource_input_schema.dump(resource_input)

            patch = jsonpatch.JsonPatch(request.json)
            data = patch.apply(data)

            updated_resource = resource_input_schema.load(data)
            db.session.commit()

            return resource_input_schema.dump(updated_resource)
        except jsonpatch.JsonPatchConflict:
            return abort(403, "Patch format is incorrect")
    else:
        return abort(
            404,
            "No resource input found for Id: {resource_input_id}".format(
                resource_input_id=resource_input_id
            ),
        )
