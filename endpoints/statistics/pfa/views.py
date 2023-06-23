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
from database.statistics.pfa import PfaAccess
from flask import request


@create_pfa.route("/create_pfa/", methods=["POST"])
@permissions_required(["statistic.pfa.create_pfa"])
@param_check(ARGS.pfa.create_pfa)
def create_pfa_endpoint():
    """Method to handle the creation of a new pfa"""

    # Try to parse information
    try:
        # Parse information from the call's body
        data = request.get_json()

        # Add the pfa to the database
        result = PfaAccess.create_pfa(**data)

        # Return response data
        return result, (200 if result.status == "success" else 400)

    # Error handling
    except Exception as e:
        return serverErrorResponse(str(e))


@update_pfa.route("/update_pfa/", methods=["POST"])
@permissions_required(["statistic.pfa.update_pfa"])
@param_check(ARGS.pfa.update_pfa)
def update_pfa_endpoint():
    """Method to handle the update of a pfa"""

    # Try to parse information
    try:
        # Parse information from the call's body
        data = request.get_json()

        # Get the id of the target pfa
        id = data.pop("id")

        # Add the pfa to the database
        result = PfaAccess.update_pfa(id, **data)

        # Return response data
        return result, (200 if result.status == "success" else 400)

    # Error handling
    except Exception as e:
        return serverErrorResponse(str(e))


@get_pfa_info.route("/get_pfa_info/", methods=["GET"])
@permissions_required(["statistic.pfa.get_pfa_info"])
@param_check(ARGS.pfa.get_pfa_info)
def get_pfa_info_endpoint():
    """Method to get the info of an pfa"""

    # Try to parse information
    try:
        # Parse information from the call's body
        data = request.get_json()

        # Get the id of the target pfa
        id = data.pop("id")

        # Get the pfa's information from the database
        result = PfaAccess.get_pfa(id)

        # Return error if no pfa was provided
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
@param_check(ARGS.pfa.delete_pfa)
def delete_pfa_endpoint():
    """Method to handle the deletion of a pfa"""

    # Try to parse information
    try:
        # Parse information from the call's body
        data = request.get_json()

        # Add the event to the database
        result = PfaAccess.delete_pfa(**data)

        # Return response data
        return result, (200 if result.status == "success" else 400)

    # Error handling
    except Exception as e:
        return serverErrorResponse(str(e))
