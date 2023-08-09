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
    create_five_point,
    get_five_point_info,
    get_user_five_point_info,
    get_five_point_format_info,
    get_test_five_point_score,
    update_five_point,
    delete_five_point,
)
from utils.permissions import isOfficerFromAbove
from flask_jwt_extended import jwt_required
from flask import request
from database.statistics.five_point import FivePointAccess
from database.user import UserAccess
from models.statistics.five_point import FivePoint


#
#   CREATE OPERATIONS
#   region
#


@create_five_point.route("/create_five_point/", methods=["POST"])
@is_root
@permissions_required(["statistic.five_point.create_five_point"])
@param_check(ARGS.statistic.five_point.create_five_point)
@error_handler
def create_five_point_endpoint(**kwargs):
    """Method to handle the creation of a new five point evaluation"""

    # Parse information from the call's body
    data = request.get_json()

    # Add the five_point to the database
    result = FivePointAccess.create_five_point(**data, from_user=kwargs["id"])

    # Return response data
    return result, (200 if result.status == "success" else 400)


#   endregion


#
#   READ OPERATIONS
#   region
#


@get_five_point_info.route("/get_five_point_info/", methods=["GET"])
@permissions_required(["statistic.five_point.get_five_point_info"])
@param_check(ARGS.statistic.five_point.get_five_point_info)
@error_handler
def get_five_point_info_endpoint(**kwargs):
    """Method to get the info of an five point evaluation"""

    # Parse information from the call's body
    data = request.get_json()

    # Get the id of the target five point
    id = data.pop("id")

    # Get the five point evaluation's information from the database
    result = FivePointAccess.get_five_point(id)

    # Return error if no five point was provided
    if result.status == "error":
        return result, 200

    # Format message
    result.message = result.message.info

    # Return response data
    return result, (200 if result.status == "success" else 400)


@get_user_five_point_info.route("/get_user_five_point_info/", methods=["POST"])
@permissions_required(["statistic.five_point.get_user_five_point_info"])
@param_check(ARGS.statistic.five_point.get_user_five_point_info)
@error_handler
def get_user_five_point_info_endpoint(**kwargs):
    """Method to get the info of a five point"""

    # Parse information from the call's body
    data = request.get_json()

    # Get the id of the target five point
    id = data.pop("id")

    # Get the user's information from the database
    user = UserAccess.get_user(id)

    # Return error if the given ID is not found
    if user.status == "error":
        return user, 200

    # Extract user info
    user = user.message.info

    # Get five point information based on the user's id
    result = FivePointAccess.get_user_five_point(id=id, **data)

    # Sort the user events by start datetime
    result.message = sorted(
        result.message,
        key=lambda x: x["datetime_taken"],
        reverse=True,
    )

    # Return the information
    return result, 200


@get_five_point_format_info.route(
    "/get_five_point_format_info/", methods=["GET"]
)
@jwt_required()
@error_handler
def get_five_point_format_info_endpoint(**kwargs):
    """Endpoint to get the five point format structure"""

    # Develop message
    message = {
        "scoring_ids": FivePoint.get_scoring_ids(),
        "scoring_type": FivePoint.get_scoring_type(),
        "scoring_options": FivePoint.get_scoring_options(),
        "scoring_formatted": FivePoint.get_scoring_formatted(),
        "info_ids": FivePoint.get_info_ids(),
        "info_type": FivePoint.get_info_type(),
        "info_options": FivePoint.get_info_options(),
        "info_formatted": FivePoint.get_info_formatted(),
    }

    # Return message
    return success_response(message)


@get_test_five_point_score.route(
    "/get_test_five_point_score/", methods=["POST"]
)
@jwt_required()
@param_check(ARGS.statistic.five_point.get_test_five_point_score)
@error_handler
def get_test_five_point_score_endpoint(**kwargs):
    """Return a test result of a set of given inputs"""

    # Parse information from the call's body
    data = request.get_json()

    # Calculate the five point scoring
    result = FivePointAccess.get_test_five_point(**data)

    # Return response data
    return result, (200 if result.status == "success" else 400)


#   endregion


#
#   UPDATE OPERATIONS
#   region
#


@update_five_point.route("/update_five_point/", methods=["POST"])
@is_root
@permissions_required(["statistic.five_point.update_five_point"])
@param_check(ARGS.statistic.five_point.update_five_point)
@error_handler
def update_five_point_endpoint(**kwargs):
    """Method to handle the update of a five point"""

    # Parse information from the call's body
    data = request.get_json()

    # Check if the five point is legit
    five_point = FivePointAccess.get_five_point(data["id"])
    if five_point.status == "error":
        return client_error_response(five_point.message)
    five_point = five_point.message.info

    # Get to user's info
    user = UserAccess.get_user(five_point.to_user).message.info

    # Check if the user is an officer of a superior unit
    is_superior_officer = isOfficerFromAbove(user.units, kwargs["id"])

    # If the user is not rooted nor is officer of the unit, return error
    if not (kwargs["isRoot"] or is_superior_officer):
        # Return error if not
        return client_error_response(
            "You don't have access to this information"
        )

    # Check if subscores is in the body contents and ensure it is OK
    types = FivePoint.get_scoring_type()[1:]
    if "subscores" in data:
        for idx, i in enumerate(FivePoint.get_scoring_ids()[1:]):
            if i in data["subscores"]:
                if types[idx] == "number":
                    five_point.subscores[i] = float(data["subscores"][i])
                elif types[idx] == "selection":
                    five_point.subscores[i] = data["subscores"][i]
                elif types[idx] == "time":
                    five_point.subscores[i] = str(data["subscores"][i])

    # Check if info is in the body contents and ensure it is OK
    types = FivePoint.get_info_type()[1:]
    if "info" in data:
        for idx, i in enumerate(FivePoint.get_info()[1:]):
            if i in data["info"]:
                if types[idx] == "number":
                    five_point.info[i] = float(data["info"][i])
                elif types[idx] == "string":
                    five_point.info[i] = str(data["info"][i])

    # Regenerate the five point object and update five point
    five_point = FivePoint(**five_point)
    result = FivePointAccess.update_five_point(data["id"], **five_point.info)

    # Return response data
    return result, (200 if result.status == "success" else 400)


#   endregion


#
#   DELETE OPERATIONS
#   region
#


@delete_five_point.route("/delete_five_point/", methods=["POST"])
@permissions_required(["statistic.five_point.delete_five_point"])
@param_check(ARGS.statistic.five_point.delete_five_point)
@error_handler
def delete_five_point_endpoint(**kwargs):
    """Method to handle the deletion of a five point"""

    # Parse information from the call's body
    data = request.get_json()

    # Add the event to the database
    result = FivePointAccess.delete_five_point(**data)

    # Return response data
    return result, (200 if result.status == "success" else 400)


#   endregion
