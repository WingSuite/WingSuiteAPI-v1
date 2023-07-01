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
from flask_jwt_extended import jwt_required, decode_token
from flask import request
from database.statistics.warrior import WarriorAccess


@create_warrior.route("/create_warrior/", methods=["POST"])
@permissions_required(["statistic.warrior.create_warrior"])
@param_check(ARGS.statistic.warrior.create_warrior)
@jwt_required()
def create_warrior_endpoint(**kwargs):
    """Method to handle the creation of a new warrior"""

    # Try to parse information
    try:
        # Get the access token
        token = request.headers.get("Authorization", None).split()[1]

        # Decode the JWT Token and get the ID of the user
        id = decode_token(token)["sub"]["_id"]

        # Parse information from the call's body
        data = request.get_json()

        # Add the warrior to the database
        result = WarriorAccess.create_warrior(**data, from_user=id)

        # Return response data
        return result, (200 if result.status == "success" else 400)

    # Error handling
    except Exception as e:
        return serverErrorResponse(str(e))


@update_warrior.route("/update_warrior/", methods=["POST"])
@permissions_required(["statistic.warrior.update_warrior"])
@param_check(ARGS.statistic.warrior.update_warrior)
def update_warrior_endpoint(**kwargs):
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
@param_check(ARGS.statistic.warrior.get_warrior_info)
def get_warrior_info_endpoint(**kwargs):
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
@param_check(ARGS.statistic.warrior.delete_warrior)
def delete_warrior_endpoint(**kwargs):
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
