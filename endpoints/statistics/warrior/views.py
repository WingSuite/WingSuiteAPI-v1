# Import the test blueprint
from endpoints.base import (
    permissions_required,
    param_check,
    serverErrorResponse,
    ARGS,
)
from . import (
    create_warrior,
    update_warrior,
    get_warrior_info,
    delete_warrior,
)
from database.statistics.warrior import WarriorAccess
from flask import request


@create_warrior.route("/create_warrior/", methods=["POST"])
@permissions_required(["statistic.warrior.create_warrior"])
@param_check(ARGS.warrior.create_warrior)
def create_warrior_endpoint():
    """Method to handle the creation of a new warrior"""

    # Try to parse information
    try:
        # Parse information from the call's body
        data = request.get_json()

        # Add the warrior to the database
        result = WarriorAccess.create_warrior(**data)

        # Return response data
        return result, (200 if result.status == "success" else 400)

    # Error handling
    except Exception as e:
        return serverErrorResponse(str(e))


@update_warrior.route("/update_warrior/", methods=["POST"])
@permissions_required(["statistic.warrior.update_warrior"])
@param_check(ARGS.warrior.update_warrior)
def update_warrior_endpoint():
    """Method to handle the update of a warrior"""

    # Try to parse information
    try:
        # Parse information from the call's body
        data = request.get_json()

        # Get the id of the target warrior
        id = data.pop("id")

        # Add the warrior to the database
        result = WarriorAccess.update_warrior(id, **data)

        # Return response data
        return result, (200 if result.status == "success" else 400)

    # Error handling
    except Exception as e:
        return serverErrorResponse(str(e))


@get_warrior_info.route("/get_warrior_info/", methods=["GET"])
@permissions_required(["statistic.warrior.get_warrior_info"])
@param_check(ARGS.warrior.get_warrior_info)
def get_warrior_info_endpoint():
    """Method to get the info of an warrior"""

    # Try to parse information
    try:
        # Parse information from the call's body
        data = request.get_json()

        # Get the id of the target warrior
        id = data.pop("id")

        # Get the warrior's information from the database
        result = WarriorAccess.get_warrior(id)

        # Return error if no warrior was provided
        if result.status == "error":
            return result, 200

        # Format message
        result.message = result.message.info

        # Return response data
        return result, (200 if result.status == "success" else 400)

    # Error handling
    except Exception as e:
        return serverErrorResponse(str(e))


@delete_warrior.route("/delete_warrior/", methods=["POST"])
@permissions_required(["statistic.warrior.delete_warrior"])
@param_check(ARGS.warrior.delete_warrior)
def delete_warrior_endpoint():
    """Method to handle the deletion of a warrior"""

    # Try to parse information
    try:
        # Parse information from the call's body
        data = request.get_json()

        # Add the event to the database
        result = WarriorAccess.delete_warrior(**data)

        # Return response data
        return result, (200 if result.status == "success" else 400)

    # Error handling
    except Exception as e:
        return serverErrorResponse(str(e))
