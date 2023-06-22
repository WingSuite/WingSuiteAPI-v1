# Import the test blueprint
from endpoints.base import (
    permissions_required,
    param_check,
    serverErrorResponse,
    ARGS,
)
from . import (
    create_feedback,
    update_feedback,
    get_feedback_info,
    delete_feedback,
)
from database.statistics.feedback import FeedbackAccess
from flask import request


@create_feedback.route("/create_feedback/", methods=["POST"])
@permissions_required(["statistic.feedback.create_feedback"])
@param_check(ARGS.feedback.create_feedback)
def create_feedback_endpoint():
    """Method to handle the creation of a new feedback"""

    # Try to parse information
    try:
        # Parse information from the call's body
        data = request.get_json()

        # Add the feedback to the database
        result = FeedbackAccess.create_feedback(**data)

        # Return response data
        return result, (200 if result.status == "success" else 400)

    # Error handling
    except Exception as e:
        return serverErrorResponse(str(e))


@update_feedback.route("/update_feedback/", methods=["POST"])
@permissions_required(["statistic.feedback.update_feedback"])
@param_check(ARGS.feedback.update_feedback)
def update_feedback_endpoint():
    """Method to handle the update of a feedback"""

    # Try to parse information
    try:
        # Parse information from the call's body
        data = request.get_json()

        # Get the id of the target feedback
        id = data.pop("id")

        # Add the feedback to the database
        result = FeedbackAccess.update_feedback(id, **data)

        # Return response data
        return result, (200 if result.status == "success" else 400)

    # Error handling
    except Exception as e:
        return serverErrorResponse(str(e))


@get_feedback_info.route("/get_feedback_info/", methods=["GET"])
@permissions_required(["statistic.feedback.get_feedback_info"])
@param_check(ARGS.feedback.get_feedback_info)
def get_feedback_info_endpoint():
    """Method to get the info of an feedback"""

    # Try to parse information
    try:
        # Parse information from the call's body
        data = request.get_json()

        # Get the id of the target feedback
        id = data.pop("id")

        # Get the feedback's information from the database
        result = FeedbackAccess.get_feedback(id)

        # Return error if no feedback was provided
        if result.status == "error":
            return result, 200

        # Format message
        result.message = result.message.info

        # Return response data
        return result, (200 if result.status == "success" else 400)

    # Error handling
    except Exception as e:
        return serverErrorResponse(str(e))


@delete_feedback.route("/delete_feedback/", methods=["POST"])
@permissions_required(["statistic.feedback.delete_feedback"])
@param_check(ARGS.feedback.delete_feedback)
def delete_feedback_endpoint():
    """Method to handle the deletion of an feedback"""

    # Try to parse information
    try:
        # Parse information from the call's body
        data = request.get_json()

        # Add the event to the database
        result = FeedbackAccess.delete_feedback(**data)

        # Return response data
        return result, (200 if result.status == "success" else 400)

    # Error handling
    except Exception as e:
        return serverErrorResponse(str(e))
