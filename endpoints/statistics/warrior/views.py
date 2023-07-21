# Import the test blueprint
from endpoints.base import (
    is_root,
    permissions_required,
    param_check,
    error_handler,
    ARGS,
)
from . import (
    create_warrior,
    update_warrior,
    get_warrior_info,
    delete_warrior,
)
from flask import request
from database.statistics.warrior import WarriorAccess


@create_warrior.route("/create_warrior/", methods=["POST"])
@is_root
@permissions_required(["statistic.warrior.create_warrior"])
@param_check(ARGS.statistic.warrior.create_warrior)
@error_handler
def create_warrior_endpoint(**kwargs):
    """Method to handle the creation of a new warrior"""

    # Parse information from the call's body
    data = request.get_json()

    # Add the warrior to the database
    result = WarriorAccess.create_warrior(**data, from_user=kwargs["id"])

    # Return response data
    return result, (200 if result.status == "success" else 400)


@update_warrior.route("/update_warrior/", methods=["POST"])
@permissions_required(["statistic.warrior.update_warrior"])
@param_check(ARGS.statistic.warrior.update_warrior)
@error_handler
def update_warrior_endpoint(**kwargs):
    """Method to handle the update of a warrior"""

    # Parse information from the call's body
    data = request.get_json()

    # Get the id of the target warrior
    id = data.pop("id")

    # Add the warrior to the database
    result = WarriorAccess.update_warrior(id, **data)

    # Return response data
    return result, (200 if result.status == "success" else 400)


@get_warrior_info.route("/get_warrior_info/", methods=["GET"])
@permissions_required(["statistic.warrior.get_warrior_info"])
@param_check(ARGS.statistic.warrior.get_warrior_info)
@error_handler
def get_warrior_info_endpoint(**kwargs):
    """Method to get the info of an warrior"""

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


@delete_warrior.route("/delete_warrior/", methods=["POST"])
@permissions_required(["statistic.warrior.delete_warrior"])
@param_check(ARGS.statistic.warrior.delete_warrior)
@error_handler
def delete_warrior_endpoint(**kwargs):
    """Method to handle the deletion of a warrior"""

    # Parse information from the call's body
    data = request.get_json()

    # Add the event to the database
    result = WarriorAccess.delete_warrior(**data)

    # Return response data
    return result, (200 if result.status == "success" else 400)
