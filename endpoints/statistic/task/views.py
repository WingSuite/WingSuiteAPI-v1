# Import the test blueprint
from endpoints.base import (
    is_root,
    client_error_response,
    permissions_required,
    param_check,
    error_handler,
    ARGS,
)
from . import (
    create_task,
    get_task_info,
    get_dispatched_tasks,
    update_task,
    request_completion,
    change_status,
    delete_task,
)
from flask import request
from utils.communications.email import send_email
from utils.html import read_html_file
from database.statistic.task import TaskAccess
from database.user import UserAccess
from config.config import config
from datetime import datetime
from threading import Thread

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
    data["incomplete"] = {i: "" for i in data["users"]}
    del data["users"]
    result = TaskAccess.create_task(**data, from_user=kwargs["id"])

    # Send an email to each recipient if success in creating task
    if result.status == "success" and data["notify_email"]:
        for i in to_users:
            # Get task HTML content
            content = read_html_file(
                "statistic.task.create",
                to_user=i.get_fullname(with_rank=True),
                from_user=from_user.get_fullname(with_rank=True),
                name=data["name"],
                suspense=datetime.fromtimestamp(data["suspense"]).strftime(
                    "%d %b %Y, %H:%M"
                ),
                description=data["description"],
                task_link=f"{config.wingsuite_dashboard_link}/tasks",
            )

            # Send an email with the HTML content
            thread = Thread(
                target=send_email,
                args=(
                    i.info.email,
                    "New Task",
                    content,
                    config.message_emoji.statistic.task,
                ),
            )
            thread.start()

    # Return response data
    return result, (200 if result.status == "success" else 400)


#   endregion

#
#   READ OPERATIONS
#   region
#


@get_task_info.route("/get_task_info/", methods=["POST"])
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


@get_dispatched_tasks.route("/get_dispatched_tasks/", methods=["POST"])
@is_root
@permissions_required(["statistic.task.get_dispatched_tasks"])
@param_check(ARGS.statistic.task.get_dispatched_tasks)
@error_handler
def get_dispatched_tasks_endpoint(**kwargs):
    """Endpoint to get dispatched tasks made by the user"""

    # Parse information from the call's body
    data = request.get_json()

    # Get warrior knowledge information based on the user's id
    result = TaskAccess.get_dispatched_tasks(id=kwargs["id"], **data)

    # If the resulting information is in error, respond with error
    if result.status == "error":
        return client_error_response(result.message)

    # Return the content of the information
    return result, (200 if result.status == "success" else 400)


def task_dispatch(**kwargs):
    """Function to dispatch task notifications"""

    # Get tasks that have reminders
    tasks = TaskAccess.get_upcoming_tasks().message

    # Print debug
    print(f"Found {len(tasks)} tasks to dispatch")

    # Iterate through each event]
    memoize = {}
    for i in tasks:
        # Get suspense time for the iterate task
        suspense_str = datetime.fromtimestamp(i.info.suspense).strftime(
            "%d %b %Y, %H:%M"
        )
        # Iterate through the people in the incomplete stage
        for user in i.info.incomplete:
            # If the iterated user is not in the memoized list, add them
            if user not in memoize:
                # If the iterate user is no longer a user, continue
                user_info = UserAccess.get_user(user)
                if user_info.status == "error":
                    continue

                # Add user to the memoization
                memoize[user] = user_info.message

            # Extract the user's email and name
            email = memoize[user].info.email
            name = memoize[user].get_fullname(with_rank=True)
            print(f"{config.wingsuite_dashboard_link}/tasks")

            # Prep the contents of the message
            msg_content = {
                "to_user": name,
                "template": "statistic.task.notify",
                "name": i.info.name,
                "time_to_completion": i.info.formatted_time_remain,
                "suspense": suspense_str,
                "description": i.info.description,
                "task_link": f"{config.wingsuite_dashboard_link}/tasks",
            }

            # Send emails
            thread = Thread(
                target=send_email,
                args=(
                    email,
                    "Task Reminder",
                    read_html_file(**msg_content),
                    config.message_emoji.statistic.task,
                ),
            )
            thread.start()


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
@param_check(ARGS.statistic.task.request_completion)
@error_handler
def request_completion_endpoint(**kwargs):
    """Method to handling users' completion request"""

    # Parse information from the call's body
    data = request.get_json()

    # Get the id of the target feedback and user
    task_id = data.pop("id")
    user_id = kwargs["id"]
    message = data["message"]

    # Update the task
    result = TaskAccess.request_completion(task_id, user_id, message)

    # Return response data
    return result, (200 if result.status == "success" else 400)


@change_status.route("/change_status/", methods=["POST"])
@is_root
@permissions_required(["statistic.task.change_status"])
@param_check(ARGS.statistic.task.change_status)
@error_handler
def change_status_endpoint(**kwargs):
    """Method to handle users' completion status, rejection"""

    # Parse information from the call's body
    data = request.get_json()

    # Get the id of the target feedback and user
    task_id = data.pop("task_id")
    user_id = data.pop("user_id")
    message = data.pop("message")
    action = data.pop("action")

    # Reject the target user
    result = TaskAccess.change_status(task_id, user_id, message, action)

    # Return response data
    return result, (200 if result.status == "success" else 400)


#   endregion


#
#   DELETE OPERATIONS
#   region
#


@delete_task.route("/delete_task/", methods=["POST"])
@permissions_required(["statistic.task.delete_task"])
@param_check(ARGS.statistic.task.delete_task)
@error_handler
def delete_task_endpoint(**kwargs):
    """Method to handle the deletion of an task"""

    # Parse information from the call's body
    data = request.get_json()

    # Add the event to the database
    result = TaskAccess.delete_task(**data)

    # Return response data
    return result, (200 if result.status == "success" else 400)


#   endregion
