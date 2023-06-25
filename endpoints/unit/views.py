# Imports
from endpoints.base import (
    permissions_required,
    param_check,
    clientErrorResponse,
    serverErrorResponse,
    successResponse,
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
def create_unit_endpoint():
    """Method to handle the creation of a new unit"""

    # Try to parse information
    try:
        # Parse information from the call's body
        data = request.get_json()

        # Add the unit to the database
        result = UnitAccess.create_unit(**data)

        # Return response data
        return result, (200 if result.status == "success" else 400)

    # Error handling
    except Exception as e:
        return serverErrorResponse(str(e))


@update_unit.route("/update_unit/", methods=["POST"])
@permissions_required(["unit.update_unit"])
@param_check(ARGS.unit.update_unit)
def update_unit_endpoint():
    """Method to handle the update of a unit"""

    # Try to parse information
    try:
        # Parse information from the call's body
        data = request.get_json()

        # Get the id of the target unit
        id = data.pop("id")

        # Add the unit to the database
        result = UnitAccess.update_unit(id, **data)

        # Return response data
        return result, (200 if result.status == "success" else 400)

    # Error handling
    except Exception as e:
        return serverErrorResponse(str(e))


@get_unit_info.route("/get_unit_info/", methods=["POST"])
@param_check(ARGS.unit.get_unit_info)
def get_unit_info_endpoint():
    """Method to get the info of a unit"""

    # Try to parse information
    try:
        # Parse information from the call's body
        data = request.get_json()

        # Get the id of the target unit
        id = data.pop("id")

        # Get the unit's information from the database
        result = UnitAccess.get_unit(id)
        result.message = result.message.info

        # Return response data
        return result, (200 if result.status == "success" else 400)

    # Error handling
    except Exception as e:
        return serverErrorResponse(str(e))


@get_all_units.route("/get_all_units/", methods=["POST"])
@param_check(ARGS.unit.get_all_units)
@jwt_required()
def get_all_units_endpoint():
    """Method to get all unit IDs"""

    # Try to parse information
    try:
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
            key=lambda x: (config.unitTypes.index(x["unit_type"]), x["name"])
        )

        # Return the content of the information
        return results, 200

    # Error handling
    except Exception as e:
        return serverErrorResponse(str(e))


@delete_unit.route("/delete_unit/", methods=["POST"])
@permissions_required(["user.delete_unit"])
@param_check(ARGS.unit.delete_unit)
def delete_unit_endpoint():
    """Method to handle the deletion of a unit"""

    # Try to parse information
    try:
        # Parse information from the call's body
        data = request.get_json()

        # Add the unit to the database
        result = UnitAccess.delete_unit(**data)

        # Return response data
        return result, (200 if result.status == "success" else 400)

    # Error handling
    except Exception as e:
        return serverErrorResponse(str(e))


@add_members.route("/add_members/", methods=["POST"])
@permissions_required(["user.add_members"])
@param_check(ARGS.unit.add_members)
def add_members_endpoint():
    """Method to add a new members to the unit"""

    # Try to parse information
    try:
        # Parse information from the call's body
        data = request.get_json()

        # Return response data
        return _update_personnel_helper(
            **data, operation="add", participation="member"
        )

    # Error handling
    except Exception as e:
        return serverErrorResponse(str(e))


@delete_members.route("/delete_members/", methods=["POST"])
@permissions_required(["user.delete_members"])
@param_check(ARGS.unit.delete_members)
def delete_members_endpoint():
    """Method to delete members to the unit"""

    # Try to parse information
    try:
        # Parse information from the call's body
        data = request.get_json()

        # Return response data
        return _update_personnel_helper(
            **data, operation="delete", participation="member"
        )

    # Error handling
    except Exception as e:
        return serverErrorResponse(str(e))


@add_officers.route("/add_officers/", methods=["POST"])
@permissions_required(["user.add_officers"])
@param_check(ARGS.unit.add_officers)
def add_officers_endpoint():
    """Method to add a new officers to the unit"""

    # Try to parse information
    try:
        # Parse information from the call's body
        data = request.get_json()

        # Return response data
        return _update_personnel_helper(
            **data, operation="add", participation="officer"
        )

    # Error handling
    except Exception as e:
        return serverErrorResponse(str(e))


@delete_officers.route("/delete_officers/", methods=["POST"])
@permissions_required(["user.delete_officers"])
@param_check(ARGS.unit.delete_officers)
def delete_officers_endpoint():
    """Method to delete officers to the unit"""

    # Try to parse information
    try:
        # Parse information from the call's body
        data = request.get_json()

        # Return response data
        return _update_personnel_helper(
            **data, operation="delete", participation="officer"
        )

    # Error handling
    except Exception as e:
        return serverErrorResponse(str(e))
