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
    create_pfa,
    get_pfa_info,
    get_user_pfa_info,
    get_pfa_format_info,
    get_test_pfa_score,
    update_pfa,
    delete_pfa,
)
from utils.permissions import isOfficerFromAbove
from flask_jwt_extended import jwt_required
from flask import request
from database.statistics.pfa import PFAAccess
from database.user import UserAccess
from models.statistics.pfa import PFA


#
#   CREATE OPERATIONS
#   region
#


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


#   endregion


#
#   READ OPERATIONS
#   region
#


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


@get_pfa_format_info.route("/get_pfa_format_info/", methods=["GET"])
@jwt_required()
@error_handler
def get_pfa_format_info_endpoint(**kwargs):
    """Endpoint to get the PFA format structure"""

    # Develop message
    message = {
        "scoring_ids": PFA.get_scoring_ids(),
        "scoring_type": PFA.get_scoring_type(),
        "scoring_options": PFA.get_scoring_options(),
        "scoring_formatted": PFA.get_scoring_formatted(),
        "info_ids": PFA.get_info_ids(),
        "info_type": PFA.get_info_type(),
        "info_options": PFA.get_info_options(),
        "info_formatted": PFA.get_info_formatted(),
    }

    # Return message
    return success_response(message)


@get_test_pfa_score.route("/get_test_pfa_score/", methods=["POST"])
@jwt_required()
@param_check(ARGS.statistic.pfa.get_test_pfa_score)
@error_handler
def get_test_pfa_score_endpoint(**kwargs):
    """Return a test result of a set of given inputs"""

    # Parse information from the call's body
    data = request.get_json()

    # Calculate the PFA scoring
    result = PFAAccess.get_test_pfa(**data)

    # Return response data
    return result, (200 if result.status == "success" else 400)


#   endregion


#
#   UPDATE OPERATIONS
#   region
#


@update_pfa.route("/update_pfa/", methods=["POST"])
@is_root
@permissions_required(["statistic.pfa.update_pfa"])
@param_check(ARGS.statistic.pfa.update_pfa)
@error_handler
def update_pfa_endpoint(**kwargs):
    """Method to handle the update of a PFA"""

    # Parse information from the call's body
    data = request.get_json()

    # Check if the pfa is legit
    pfa = PFAAccess.get_pfa(data["id"])
    if pfa.status == "error":
        return client_error_response(pfa.message)
    pfa = pfa.message.info

    # Get to user's info
    user = UserAccess.get_user(pfa.to_user).message.info

    # Check if the user is an officer of a superior unit
    is_superior_officer = isOfficerFromAbove(user.units, kwargs["id"])

    # If the user is not rooted nor is officer of the unit, return error
    if not (kwargs["isRoot"] or is_superior_officer):
        # Return error if not
        return client_error_response(
            "You don't have access to this information"
        )

    # Check if subscores is in the body contents and ensure it is OK
    types = PFA.get_scoring_type()[1:]
    if "subscores" in data:
        for idx, i in enumerate(PFA.get_scoring_ids()[1:]):
            if i in data["subscores"]:
                if types[idx] == "number":
                    pfa.subscores[i] = float(data["subscores"][i])
                elif types[idx] == "time":
                    pfa.subscores[i] = str(data["subscores"][i])

    # Check if info is in the body contents and ensure it is OK
    types = PFA.get_info_type()[1:]
    if "info" in data:
        for idx, i in enumerate(PFA.get_info()[1:]):
            if i in data["info"]:
                if types[idx] == "number":
                    pfa.info[i] = float(data["info"][i])
                elif types[idx] == "string":
                    pfa.info[i] = str(data["info"][i])

    # Regenerate the pfa object and update PFA
    pfa = PFA(**pfa)
    result = PFAAccess.update_pfa(data["id"], **pfa.info)

    # Return response data
    return result, (200 if result.status == "success" else 400)


#   endregion


#
#   DELETE OPERATIONS
#   region
#


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


#   endregion
