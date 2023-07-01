# Import the test blueprint
from endpoints.base import (
    permissions_required,
    param_check,
    serverErrorResponse,
    ARGS,
)
from . import (
    create_pfa,
    update_pfa,
    get_pfa_info,
    delete_pfa,
)
from flask import request
from database.statistics.pfa import PFAAccess


@create_pfa.route("/create_pfa/", methods=["POST"])
@permissions_required(["statistic.pfa.create_pfa"])
@param_check(ARGS.statistic.pfa.create_pfa)
def create_pfa_endpoint(**kwargs):
    """Method to handle the creation of a new PFA"""

    # Try to parse information
    try:
        # Parse information from the call's body
        data = request.get_json()

        # Add the PFA to the database
        result = PFAAccess.create_pfa(**data, from_user=kwargs["id"])

        # Return response data
        return result, (200 if result.status == "success" else 400)

    # Error handling
    except Exception as e:
        return serverErrorResponse(str(e))


@update_pfa.route("/update_pfa/", methods=["POST"])
@permissions_required(["statistic.pfa.update_pfa"])
@param_check(ARGS.statistic.pfa.update_pfa)
def update_pfa_endpoint(**kwargs):
    """Method to handle the update of a PFA"""

    # Try to parse information
    try:
        # Parse information from the call's body
        data = request.get_json()

        # Get the id of the target PFA
        id = data.pop("id")

        # Add the PFA to the database
        result = PFAAccess.update_pfa(id, **data)

        # Return response data
        return result, (200 if result.status == "success" else 400)

    # Error handling
    except Exception as e:
        return serverErrorResponse(str(e))


@get_pfa_info.route("/get_pfa_info/", methods=["GET"])
@permissions_required(["statistic.pfa.get_pfa_info"])
@param_check(ARGS.statistic.pfa.get_pfa_info)
def get_pfa_info_endpoint(**kwargs):
    """Method to get the info of an PFA"""

    # Try to parse information
    try:
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

    # Error handling
    except Exception as e:
        return serverErrorResponse(str(e))


@delete_pfa.route("/delete_pfa/", methods=["POST"])
@permissions_required(["statistic.pfa.delete_pfa"])
@param_check(ARGS.statistic.pfa.delete_pfa)
def delete_pfa_endpoint(**kwargs):
    """Method to handle the deletion of a PFA"""

    # Try to parse information
    try:
        # Parse information from the call's body
        data = request.get_json()

        # Add the event to the database
        result = PFAAccess.delete_pfa(**data)

        # Return response data
        return result, (200 if result.status == "success" else 400)

    # Error handling
    except Exception as e:
        return serverErrorResponse(str(e))
