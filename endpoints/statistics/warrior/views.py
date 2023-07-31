# Import the test blueprint
from endpoints.base import (
    success_response,
    client_error_response,
    is_root,
    permissions_required,
    param_check,
    error_handler,
    ARGS,
)
from . import (
    create_warrior,
    get_warrior_info,
    get_user_warrior_info,
    get_warrior_format_info,
    update_warrior,
    delete_warrior,
)
from utils.permissions import isOfficerFromAbove
from flask import request
from database.statistics.warrior import WarriorAccess
from database.user import UserAccess
from models.statistics.warrior import Warrior

#
#   CREATE OPERATIONS
#   region
#


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


#   endregion

#
#   READ OPERATIONS
#   region
#


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


@get_user_warrior_info.route("/get_user_warrior_info/", methods=["POST"])
@permissions_required(["statistic.pfa.get_user_warrior_info"])
@param_check(ARGS.statistic.warrior.get_user_warrior_info)
@error_handler
def get_user_warrior_info_endpoint(**kwargs):
    """Method to get the info of an PFA"""

    # Parse information from the call's body
    data = request.get_json()

    # Get the id of the target PFA
    id = data.pop("id")

    # Get the user's information from the database
    user = UserAccess.get_user(id)

    # Return error if the given ID is not found
    if user.status == "error":
        return user, 200

    # Extract user info
    user = user.message.info

    # Get PFA information based on the user's id
    result = WarriorAccess.get_user_warrior(id=id, **data)

    # Sort the user events by start datetime
    result.message = sorted(
        result.message,
        key=lambda x: x["datetime_taken"],
        reverse=True,
    )

    # Return the information
    return result, 200


@get_warrior_format_info.route("/get_warrior_format_info/", methods=["GET"])
@permissions_required(["statistic.warrior.get_warrior_format_info"])
@error_handler
def get_pfa_format_info_endpoint(**kwargs):
    """Endpoint to get the warrior format structure"""

    # Develop message
    message = {
        "scoring_ids": Warrior.get_scoring_ids(),
        "scoring_type": Warrior.get_scoring_type(),
        "scoring_options": Warrior.get_scoring_options(),
        "scoring_formatted": Warrior.get_scoring_formatted(),
        "info_ids": Warrior.get_info_ids(),
        "info_type": Warrior.get_info_type(),
        "info_options": Warrior.get_info_options(),
        "info_formatted": Warrior.get_info_formatted(),
    }

    # Return message
    return success_response(message)


#   endregion

#
#   UPDATE OPERATIONS
#   region
#


@update_warrior.route("/update_warrior/", methods=["POST"])
@is_root
@permissions_required(["statistic.warrior.update_warrior"])
@param_check(ARGS.statistic.warrior.update_warrior)
@error_handler
def update_warrior_endpoint(**kwargs):
    """Method to handle the update of a warrior"""

    # Parse information from the call's body
    data = request.get_json()

    # Check if the pfa is legit
    warrior = WarriorAccess.get_warrior(data["id"])
    if warrior.status == "error":
        return client_error_response(warrior.message)
    warrior = warrior.message.info

    # Get to user's info
    user = UserAccess.get_user(warrior.to_user).message.info

    # Check if the user is an officer of a superior unit
    is_superior_officer = isOfficerFromAbove(user.units, kwargs["id"])

    # If the user is not rooted nor is officer of the unit, return error
    if not (kwargs["isRoot"] or is_superior_officer):
        # Return error if not
        return client_error_response(
            "You don't have access to this information"
        )

    # If composite score is provided, change it
    if "composite_score" in data:
        warrior.composite_score = data["composite_score"]

    # Regenerate the warrior object and update warrior knowledge
    warrior = Warrior(**warrior)
    result = WarriorAccess.update_warrior(data["id"], **warrior.info)

    # Return response data
    return result, (200 if result.status == "success" else 400)


#   endregion

#
#   DELETE OPERATIONS
#   region
#


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


#   endregion
