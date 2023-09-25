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
from utils.communications.email import send_email
from utils.html import read_html_file
from database.statistic.feedback import FeedbackAccess
from database.user import UserAccess
from config.config import config


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

    # Check if the user is an actual user and get their email
    to_user = UserAccess.get_user(data["to_user"])
    if to_user.status == "error":
        return to_user, 400
    to_user = to_user.message.info

    # Get the sender's user info
    from_user = UserAccess.get_user(kwargs["id"]).message.info

    # Calculate the recipient's and sender's appropriate name
    to_user_name = (
        to_user.rank + " " + to_user.full_name
        if "rank" in to_user
        else to_user.first_name
    )
    from_user_name = (
        from_user.rank + " " + from_user.full_name
        if "rank" in from_user
        else from_user.first_name
    )

    # Add the feedback to the database
    result = FeedbackAccess.create_feedback(**data, from_user=kwargs["id"])

    # Notify user of the new feedback
    if result.status == "success" and data["notify_email"]:
        # Get feedback HTML content
        content = read_html_file(
            "statistic.feedback",
            to_user=to_user_name,
            from_user=from_user_name,
            message=data["feedback"],
            feedback_link=f"{config.wingsuite_dashboard_link}/feedback",
        )

        # Send an email with the HTML content
        send_email(
            receiver=to_user.email,
            subject="New Feedback",
            content=content,
            emoji=config.message_emoji.statistic.feedback,
        )

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
