# Import the test blueprint
from endpoints.base import (
    is_root,
    permissions_required,
    param_check,
    error_handler,
    ARGS,
)
from . import (
    create_feedback,
    get_feedback_info,
    update_feedback,
    delete_feedback,
)
from flask import request
from database.statistics.feedback import FeedbackAccess


#
#   CREATE OPERATIONS
#   region
#


@create_feedback.route("/create_feedback/", methods=["POST"])
@is_root
@permissions_required(["statistic.feedback.create_feedback"])
@param_check(ARGS.statistic.feedback.create_feedback)
@error_handler
def create_feedback_endpoint(**kwargs):
    """Method to handle the creation of a new feedback"""

    # Parse information from the call's body
    data = request.get_json()

    # Add the feedback to the database
    result = FeedbackAccess.create_feedback(**data, from_user=kwargs["id"])

    # Return response data
    return result, (200 if result.status == "success" else 400)


#   endregion

#
#   READ OPERATIONS
#   region
#


@get_feedback_info.route("/get_feedback_info/", methods=["GET"])
@permissions_required(["statistic.feedback.get_feedback_info"])
@param_check(ARGS.statistic.feedback.get_feedback_info)
@error_handler
def get_feedback_info_endpoint(**kwargs):
    """Method to get the info of an feedback"""

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


#   endregion

#
#   UPDATE OPERATIONS
#   region
#


@update_feedback.route("/update_feedback/", methods=["POST"])
@permissions_required(["statistic.feedback.update_feedback"])
@param_check(ARGS.statistic.feedback.update_feedback)
@error_handler
def update_feedback_endpoint(**kwargs):
    """Method to handle the update of a feedback"""

    # Parse information from the call's body
    data = request.get_json()

    # Get the id of the target feedback
    id = data.pop("id")

    # Add the feedback to the database
    result = FeedbackAccess.update_feedback(id, **data)

    # Return response data
    return result, (200 if result.status == "success" else 400)


#   endregion

#
#   DELETE OPERATIONS
#   region
#


@delete_feedback.route("/delete_feedback/", methods=["POST"])
@permissions_required(["statistic.feedback.delete_feedback"])
@param_check(ARGS.statistic.feedback.delete_feedback)
@error_handler
def delete_feedback_endpoint(**kwargs):
    """Method to handle the deletion of an feedback"""

    # Parse information from the call's body
    data = request.get_json()

    # Add the event to the database
    result = FeedbackAccess.delete_feedback(**data)

    # Return response data
    return result, (200 if result.status == "success" else 400)


#   endregion
