# Import the test blueprint
from endpoints.base import (
    client_error_response,
    is_root,
    permissions_required,
    param_check,
    error_handler,
    ARGS,
)
from . import create_event, get_event_info, update_event, delete_event
from utils.permissions import isOfficerFromAbove
from database.unit import UnitAccess
from database.event import EventAccess
from flask import request

#
#   CREATE OPERATIONS
#   region
#


@create_event.route("/create_event/", methods=["POST"])
@is_root
@permissions_required(["event.create_event"])
@param_check(ARGS.event.create_event)
@error_handler
def create_event_endpoint(**kwargs):
    """Method to handle the creation of a new event"""

    # Parse information from the call's body
    data = request.get_json()

    # Get the unit object of the target unit and return if error
    unit = UnitAccess.get_unit(data["unit"])
    if unit.status == "error":
        return unit
    unit = unit.message.info

    # Check if the user is an officer of a superior unit
    is_above = isOfficerFromAbove(data["unit"], kwargs["id"])

    # Check if the user is rooted or is officer of the unit
    if kwargs["isRoot"] or kwargs["id"] in unit.officers or is_above:
        # Add the event to the database
        result = EventAccess.create_event(**data)

        # Return response data
        return result, (200 if result.status == "success" else 400)

    # Return error if not
    return client_error_response("You don't have access to this feature")


#   endregion

#
#   READ OPERATIONS
#   region
#


@get_event_info.route("/get_event_info/", methods=["GET"])
@permissions_required(["event.get_event_info"])
@param_check(ARGS.event.get_event_info)
@error_handler
def get_event_info_endpoint(**kwargs):
    """Method to get the info of an event"""

    # Parse information from the call's body
    data = request.get_json()

    # Get the id of the target event
    id = data.pop("id")

    # Get the event's information from the database
    result = EventAccess.get_event_by_id(id)

    # Return error if no feedback was provided
    if result.status == "error":
        return result, 200

    # Format message
    result.message = result.message.info

    # Return response data
    return result, (200 if result.status == "success" else 400)


#   endregion

#
#   UPDATE OPERATIONS
#   region
#


@update_event.route("/update_event/", methods=["POST"])
@is_root
@permissions_required(["event.update_event"])
@param_check(ARGS.event.update_event)
@error_handler
def update_event_endpoint(**kwargs):
    """Method to handle the update of an event"""

    # Parse information from the call's body
    data = request.get_json()

    # Get the id of the target event
    id = data.pop("id")

    # Get the event
    event = EventAccess.get_event_by_id(id)

    # Check if the event exists
    if event.status == "error":
        return event

    # Extract unit from event
    event = event.message.info
    unit = UnitAccess.get_unit(event.unit).message.info

    # Check if the user is an officer of a superior unit
    is_above = isOfficerFromAbove(unit._id, kwargs["id"])

    # Check if the user is rooted or is officer of the unit
    if kwargs["isRoot"] or kwargs["id"] in unit.officers or is_above:
        # Add the event to the database
        result = EventAccess.update_event(id, **data)

        # Return response data
        return result, (200 if result.status == "success" else 400)

    # Return error if not
    return client_error_response("You don't have access to this feature")


#   endregion

#
#   DELETE OPERATIONS
#   region
#


@delete_event.route("/delete_event/", methods=["POST"])
@is_root
@permissions_required(["event.delete_event"])
@param_check(ARGS.event.delete_event)
@error_handler
def delete_event_endpoint(**kwargs):
    """Method to handle the deletion of an event"""

    # Parse information from the call's body
    data = request.get_json()

    # Get the event
    event = EventAccess.get_event_by_id(**data)

    # Check if the unit exists
    if event.status == "error":
        return event

    # Get the unit object of the target unit
    unit = UnitAccess.get_unit(event.message.info.unit)
    if unit.status == "error":
        return unit
    unit = unit.message.info

    # Check if the user is an officer of a superior unit
    is_above = isOfficerFromAbove(unit._id, kwargs["id"])

    # Check if the user is rooted or is officer of the unit
    if kwargs["isRoot"] or kwargs["id"] in unit.officers or is_above:
        # Add the event to the database
        result = EventAccess.delete_event(**data)

        # Return response data
        return result, (200 if result.status == "success" else 400)

    # Return error if not
    return client_error_response("You don't have access to this feature")


#   endregion
