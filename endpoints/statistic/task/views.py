# Import the test blueprint
from endpoints.base import (
    is_root,
    permissions_required,
    param_check,
    error_handler,
    ARGS,
)
from . import create_task, get_task_info, update_task, request_completion
from flask import request
from utils.communications.email import send_email
from utils.html import read_html_file
from database.statistic.task import TaskAccess
from database.user import UserAccess
from config.config import config
from datetime import datetime

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
    to_users = UserAccess.get_users(data["users"]).message

    # Get the sender's user info
    from_user = UserAccess.get_user(kwargs["id"]).message

    # Add task to the database
    data["incomplete"] = data["users"]
    del data["users"]
    result = TaskAccess.create_task(**data, from_user=kwargs["id"])

    # Send an email to each recipient if success in creating task
    if result.status == "success" and data["notify_email"]:
        for i in to_users:
            # Get task HTML content
            content = read_html_file(
                "statistic.task",
                to_user=i.get_fullname(with_rank=True),
                from_user=from_user.get_fullname(with_rank=True),
                name=data["name"],
                suspense=datetime.fromtimestamp(data["suspense"]).strftime(
                    "%d %b %Y, %H:%M"
                ),
                description=data["description"],
                task_link=f"{config.wingsuite_dashboard_link}/task",
            )

            # Send an email with the HTML content
            send_email(
                receiver=i.info.email,
                subject="New Task",
                content=content,
                emoji=config.message_emoji.statistic.task,
            )

    # Return response data
    return result, (200 if result.status == "success" else 400)


#   endregion

#
#   READ OPERATIONS
#   region
#


@get_task_info.route("get_task_info", methods=["POST"])
@permissions_required(["statistic.task.get_task_info"])
@param_check(ARGS.statistic.task.get_task_info)
@error_handler
def get_task_info_endpoint(**kwargs):
    """Method to get the info of a task"""

    # Parse information from the call's body
    data = request.get_json()

    # Get the id of the target task
    id = data.pop("id")

    # Get the task's information from the database
    result = TaskAccess.get_task(id)

    # Return error if no task was provided
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


@update_task.route("/update_task/", methods=["POST"])
@permissions_required(["statistic.task.update_task"])
@param_check(ARGS.statistic.task.update_task)
@error_handler
def update_task_endpoint(**kwargs):
    """Method to handle the update of a task"""

    # Parse information from the call's body
    data = request.get_json()

    # Get the id of the target feedback
    id = data.pop("id")

    # Add the feedback to the database
    result = TaskAccess.update_task(id, **data)

    # Return response data
    return result, (200 if result.status == "success" else 400)


@request_completion.route("/request_completion/", methods=["POST"])
@is_root
@param_check(ARGS.statistic.task.update_task)
@error_handler
# TODO: FIX ISSUES WITH PENDING AND COMPLETE BEING OBJECTS
def request_completion_endpoint(**kwargs):
    """Method to handling users' completion request"""

    # Parse information from the call's body
    data = request.get_json()

    # Get the id of the target feedback and user
    task_id = data.pop("id")
    user_id = kwargs["id"]

    # Update the task
    result = TaskAccess.request_completion(task_id, user_id)

    # Return response data
    return result, (200 if result.status == "success" else 400)


#   endregion


#
#   DELETE OPERATIONS
#   region
#


#   endregion
