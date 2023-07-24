# Import the test blueprint
from endpoints.base import (
    is_root,
    permissions_required,
    param_check,
    error_handler,
    ARGS,
)
from . import (
    create_pfa,
    update_pfa,
    delete_pfa,
    get_pfa_info,
    get_user_pfa_info,
)
from flask import request
from database.statistics.pfa import PFAAccess
from database.user import UserAccess


@create_pfa.route("/create_pfa/", methods=["POST"])
@is_root
@permissions_required(["statistic.pfa.create_pfa"])
@param_check(ARGS.statistic.pfa.create_pfa)
@error_handler
def create_pfa_endpoint(**kwargs):
    """Method to handle the creation of a new PFA"""

    # Parse information from the call's body
    data = request.get_json()

    # Add the PFA to the database
    result = PFAAccess.create_pfa(**data, from_user=kwargs["id"])

    # Return response data
    return result, (200 if result.status == "success" else 400)


@update_pfa.route("/update_pfa/", methods=["POST"])
@permissions_required(["statistic.pfa.update_pfa"])
@param_check(ARGS.statistic.pfa.update_pfa)
@error_handler
def update_pfa_endpoint(**kwargs):
    """Method to handle the update of a PFA"""

    # Parse information from the call's body
    data = request.get_json()

    # Get the id of the target PFA
    id = data.pop("id")

    # Add the PFA to the database
    result = PFAAccess.update_pfa(id, **data)

    # Return response data
    return result, (200 if result.status == "success" else 400)


@delete_pfa.route("/delete_pfa/", methods=["POST"])
@permissions_required(["statistic.pfa.delete_pfa"])
@param_check(ARGS.statistic.pfa.delete_pfa)
@error_handler
def delete_pfa_endpoint(**kwargs):
    """Method to handle the deletion of a PFA"""

    # Parse information from the call's body
    data = request.get_json()

    # Add the event to the database
    result = PFAAccess.delete_pfa(**data)

    # Return response data
    return result, (200 if result.status == "success" else 400)


@get_pfa_info.route("/get_pfa_info/", methods=["GET"])
@permissions_required(["statistic.pfa.get_pfa_info"])
@param_check(ARGS.statistic.pfa.get_pfa_info)
@error_handler
def get_pfa_info_endpoint(**kwargs):
    """Method to get the info of an PFA"""

    # Parse information from the call's body
    data = request.get_json()

    # Get the id of the target PFA
    id = data.pop("id")

    # Get the PFA's information from the database
    result = PFAAccess.get_pfa(id)

    # Return error if no PFA was provided
    if result.status == "error":
        return result, 200

    # Format message
    result.message = result.message.info

    # Return response data
    return result, (200 if result.status == "success" else 400)


@get_user_pfa_info.route("/get_user_pfa_info/", methods=["POST"])
@permissions_required(["statistic.pfa.get_user_pfa_info"])
@param_check(ARGS.statistic.pfa.get_user_pfa_info)
@error_handler
def get_user_pfa_info_endpoint(**kwargs):
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
    result = PFAAccess.get_user_pfa(id=id, **data)

    # Sort the user events by start datetime
    result.message = sorted(
        result.message,
        key=lambda x: x["datetime_taken"],
        reverse=True,
    )

    # Return the information
    return result, 200
