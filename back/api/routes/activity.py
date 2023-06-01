from typing import Any

import jsonpatch
from flask import abort, request

from impacts_model.data_model import (
    db,
    Model,
    Resource,
    Activity,
    ActivitySchema,
)
from impacts_model.impacts import (
    ActivityImpactSchema,
)
from typing import Optional


def get_activities() -> Any:
    """
    GET /activities/
    :return: all activities in the database
    """
    activities = Activity.query.all()

    activity_schema = ActivitySchema(many=True)
    return activity_schema.dump(activities)


def get_activity(activity_id: int) -> Any:
    """
    GET /activities/<activity_id>
    :return: activity if it exists with id, 404 else
    """
    activity = db.session.query(Activity).get_or_404(activity_id)
    activity_schema = ActivitySchema()
    return activity_schema.dump(activity)


def update_activity(activity_id: int) -> Any:
    """
    PATCH /activities/<activity_id>
    Update the activity with the A JSONPatch as defined by RFC 6902 in the body
    :param activity_id: the id of the activity to update
    :return: The updated activity if it exists with id, 403 if the JSONPatch format is incorrect, 404 else
    """
    activity = db.session.query(Activity).get_or_404(activity_id)
    old_parent = (
        activity.parent_activity_id
    )  # Parent activity a to be saved before patch

    try:
        activity_schema = ActivitySchema()
        data = activity_schema.dump(activity)

        patch = jsonpatch.JsonPatch(request.json)
        data = patch.apply(data)
        activity = activity_schema.load(data)

        for operation in patch:
            if operation["path"] == "/parent_activity_id":
                _exchange_parent(int(operation["value"]), activity, old_parent)
        db.session.commit()

        return activity_schema.dump(activity)
    except jsonpatch.JsonPatchConflict:
        return abort(403, "Patch format is incorrect")


def _exchange_parent(
    parent_id_to_set: int, activity: Activity, old_parent_id: int
) -> None:
    # Check when changing the parent of a activity, if its by one of its subactivities
    # If it is, it will set the subactivity parent as this of the activity
    # For a tree 1 -> 2 -> 3 and activity 2 goes under 3, 3 parent will be set as 1
    # Recursive to check for all subactivities

    # Iterate through subactivities
    for i in range(len(activity.subactivities)):
        # Recursive call for each subactivity
        _exchange_parent(
            parent_id_to_set, activity.subactivities[i], activity.parent_activity_id
        )

        # If subactivity id is the one we want to set as parent
        if activity.subactivities[i].id == parent_id_to_set:
            # Replace subactivity id by this of the activity parent
            activity.subactivities[i].parent_activity_id = old_parent_id


def get_activity_impacts(activity_id: int) -> Any:
    """
    GET /activities/<activity_id>/impacts
    Get a activity environmental impact
    :param activity_id: the id of the activity to get the impact
    :return: ActivityImpact if activity exist, 404 else
    """
    activity: Activity = db.session.query(Activity).get_or_404(activity_id)
    activity_impact = activity.get_impact()
    schema = ActivityImpactSchema()
    return schema.dump(activity_impact)


def delete_activity(activity_id: int) -> Any:
    """
    DELETE /activities/<activity_id>
    :param activity_id: the id of the activity to delete
    :return: 200 if the activity exists and is deleted, 404 else
    """
    activity = db.session.query(Activity).get_or_404(activity_id)

    model = Model.query.filter(Model.root_activity_id == activity.id).one_or_none()
    if model != None:
        return abort(
            403,
            "Cannot delete activity {activity_id} as it is the root of model {model}".format(
                activity_id=activity_id, model=model.root_activity_id
            ),
        )
    db.session.delete(activity)
    db.session.commit()
    return 200


def create_activity(activity: dict[str, Any]) -> Any:
    """
    POST /activities/

    :param activity: activity to add
    :return: the activity inserted with its id
    """
    name = activity.get("name")
    parent_activity_id = activity.get("parent_activity_id")

    existing_activity = (
        Activity.query.filter(Activity.name == name)
        .filter(Activity.parent_activity_id == parent_activity_id)
        .one_or_none()
    )

    if existing_activity is None:
        schema = ActivitySchema()
        new_activity = schema.load(activity)
        db.session.add(new_activity)
        db.session.commit()
        data = schema.dump(new_activity)
        return data, 201
    else:
        return abort(
            409,
            "Activity {activity} exists already".format(activity=activity),
        )
