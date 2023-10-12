# Import the test blueprint
from endpoints.base import (
    is_root,
    permissions_required,
    param_check,
    error_handler,
    ARGS,
)
from . import (
    create_task
)
from flask import request
from utils.communications.email import send_email
from utils.html import read_html_file
from database.statistic.task import TaskAccess
from database.user import UserAccess
from config.config import config

#
#   CREATE OPERATIONS
#   region
#


@create_task.route("/create_task/", methods=["POST"])
@is_root
@permissions_required(["statistic.task.create_task"])
@param_check(ARGS.statistic.task.create_task)
@error_handler
def create_task_endpoint(**kwargs):
    """Method to handle the creation of a new task"""

    # Parse information from the call's body
    data = request.get_json()

    # Get an object instance of the users in the list
    to_users = UserAccess.get_users(data["to_users"]).message

    # Get the sender's user info
    from_user = UserAccess.get_user(kwargs["id"]).message

    # Add task to the database
    result = TaskAccess.create_task(**data, from_user=kwargs["id"])

    # Send an email to each recipient if success in creating task
    if result.status == "success" and data["notify_email"]:
        for i in to_users:
            # Get feedback HTML content
            content = read_html_file(
                "statistic.feedback",
                to_user=i.get_fullname(with_rank=True),
                from_user=from_user.get_fullname(with_rank=True),
                message=data["description"],
                feedback_link=f"{config.wingsuite_dashboard_link}/feedback",
            )

            # Send an email with the HTML content
            send_email(
                receiver=i.info.email,
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


#   endregion

#
#   UPDATE OPERATIONS
#   region
#


#   endregion


#
#   DELETE OPERATIONS
#   region
#


#   endregion
