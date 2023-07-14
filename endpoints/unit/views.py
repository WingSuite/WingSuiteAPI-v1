# Imports
from endpoints.base import (
    successResponse,
    clientErrorResponse,
    permissions_required,
    param_check,
    error_handler,
    ARGS,
)
from . import (
    create_unit,
    update_unit,
    get_unit_info,
    get_all_units,
    delete_unit,
    add_members,
    delete_members,
    add_officers,
    delete_officers,
    get_all_members,
)
from config.config import config
from flask_jwt_extended import jwt_required
from flask import request
from database.unit import UnitAccess
from database.user import UserAccess


def _update_personnel_helper(id, users, operation, participation):
    """Helper function to update personnel for a unit"""

    # Get the vocab based on the operation
    past_tense = "added" if operation == "add" else "deleted"
    ion_word = "addition" if operation == "add" else "deletion"

    # Get the unit object
    unit = UnitAccess.get_unit(id)

    # If content is not in result of getting the unit, return the
    # error message
    if unit.status == "error":
        return unit

    # Get the content from the unit fetch
    unit = unit.message

    # Iterate through the list of members
    results = {}
    for user in users:
        # Get the user object of the iterated person
        user_obj = UserAccess.get_user(user)

        # If the user object query results an error, track it and continue
        if user_obj.status == "error":
            results[user] = "User not found"
            continue

        # Extract user object
        user_obj = user_obj.message

        # Do an add operation if operation is "add"
        if operation == "add":
            res = user_obj.add_unit(id)
            if res:
                if participation == "member":
                    unit.add_member(user)
                elif participation == "officer":
                    unit.add_officer(user)

        # Do a delete operation if operation is "delete"
        elif operation == "delete":
            res = None
            if participation == "member":
                res = unit.delete_member(user)
            elif participation == "officer":
                res = unit.delete_officer(user)
            if res:
                user_obj.delete_unit(id)

        # Update user
        UserAccess.update_user(user_obj.info._id, **user_obj.info)

        # Track result
        results[user] = (
            f"User {past_tense}"
            if res
            else f"User already {past_tense} as a {participation}"
        )

    # Push unit changes
    UnitAccess.update_unit(id, **unit.info)

    # Make the message
    message = {
        "status": "success",
        "message": f"{participation.capitalize()} {ion_word} have been applied"
        + f" to {unit.info.name}. Refer to results for what has been "
        + "applied",
        "results": results,
    }

    # Return
    return successResponse(message)


@create_unit.route("/create_unit/", methods=["POST"])
@permissions_required(["unit.create_unit"])
@param_check(ARGS.unit.create_unit)
@error_handler
def create_unit_endpoint(**kwargs):
    """Method to handle the creation of a new unit"""

    # Parse information from the call's body
    data = request.get_json()

    # Add the unit to the database
    result = UnitAccess.create_unit(**data)

    # Return response data
    return result, (200 if result.status == "success" else 400)


@update_unit.route("/update_unit/", methods=["POST"])
@permissions_required(["unit.update_unit"])
@param_check(ARGS.unit.update_unit)
@error_handler
def update_unit_endpoint(**kwargs):
    """Method to handle the update of a unit"""

    # Parse information from the call's body
    data = request.get_json()

    # Get the id of the target unit
    id = data.pop("id")

    # Add the unit to the database
    result = UnitAccess.update_unit(id, **data)

    # Return response data
    return result, (200 if result.status == "success" else 400)


@get_unit_info.route("/get_unit_info/", methods=["POST"])
@param_check(ARGS.unit.get_unit_info)
@error_handler
def get_unit_info_endpoint(**kwargs):
    """Method to get the info of a unit"""

    # Parse information from the call's body
    data = request.get_json()

    # Get the id of the target unit
    id = data.pop("id")

    # Get the unit's information from the database
    result = UnitAccess.get_unit(id)
    result.message = result.message.info

    # Return response data
    return result, (200 if result.status == "success" else 400)


@get_all_units.route("/get_all_units/", methods=["POST"])
@param_check(ARGS.unit.get_all_units)
@jwt_required()
@error_handler
def get_all_units_endpoint(**kwargs):
    """Method to get all unit IDs"""

    # Parse information from the call's body
    data = request.get_json()

    # Get the content information based on the given page size and
    # page index
    results = UnitAccess.get_units(**data)

    # If the resulting information is in error, respond with error
    if results.status == "error":
        return clientErrorResponse(results.message)

    # Sort and Format message
    results.message = [item.info for item in results.message]
    results.message = sorted(
        results.message,
        key=lambda x: (config.unitTypes.index(x["unit_type"]), x["name"]),
    )

    # Return the content of the information
    return results, 200


@delete_unit.route("/delete_unit/", methods=["POST"])
@permissions_required(["user.delete_unit"])
@param_check(ARGS.unit.delete_unit)
@error_handler
def delete_unit_endpoint(**kwargs):
    """Method to handle the deletion of a unit"""

    # Parse information from the call's body
    data = request.get_json()

    # Add the unit to the database
    result = UnitAccess.delete_unit(**data)

    # Return response data
    return result, (200 if result.status == "success" else 400)


@add_members.route("/add_members/", methods=["POST"])
@permissions_required(["user.add_members"])
@param_check(ARGS.unit.add_members)
@error_handler
def add_members_endpoint(**kwargs):
    """Method to add a new members to the unit"""

    # Parse information from the call's body
    data = request.get_json()

    # Return response data
    return _update_personnel_helper(
        **data, operation="add", participation="member"
    )


@delete_members.route("/delete_members/", methods=["POST"])
@permissions_required(["user.delete_members"])
@param_check(ARGS.unit.delete_members)
@error_handler
def delete_members_endpoint(**kwargs):
    """Method to delete members to the unit"""

    # Parse information from the call's body
    data = request.get_json()

    # Return response data
    return _update_personnel_helper(
        **data, operation="delete", participation="member"
    )


@add_officers.route("/add_officers/", methods=["POST"])
@permissions_required(["user.add_officers"])
@param_check(ARGS.unit.add_officers)
@error_handler
def add_officers_endpoint(**kwargs):
    """Method to add a new officers to the unit"""

    # Parse information from the call's body
    data = request.get_json()

    # Return response data
    return _update_personnel_helper(
        **data, operation="add", participation="officer"
    )


@delete_officers.route("/delete_officers/", methods=["POST"])
@permissions_required(["user.delete_officers"])
@param_check(ARGS.unit.delete_officers)
@error_handler
def delete_officers_endpoint(**kwargs):
    """Method to delete officers to the unit"""

    # Parse information from the call's body
    data = request.get_json()

    # Return response data
    return _update_personnel_helper(
        **data, operation="delete", participation="officer"
    )


@get_all_members.route("/get_all_members/", methods=["POST"])
@param_check(ARGS.unit.get_all_members)
@error_handler
def get_all_members_endpoint(**kwargs):
    """Function to handle getting all the members of a unit"""

    return {}, 200
