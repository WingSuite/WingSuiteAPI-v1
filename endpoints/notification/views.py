# Import the test blueprint
from endpoints.base import (
    client_error_response,
    is_root,
    permissions_required,
    param_check,
    error_handler,
    ARGS,
)
from . import (
    create_notification,
    get_notification_info,
    update_notification,
    delete_notification,
)
from utils.communications.email import send_email_by_units
from utils.permissions import isOfficerFromAbove
from database.notification import NotificationAccess
from database.unit import UnitAccess
from database.user import UserAccess
from config.config import config
from flask import request

#
#   CREATE OPERATIONS
#   region
#


@create_notification.route("/create_notification/", methods=["POST"])
@is_root
@permissions_required(["notification.create_notification"])
@param_check(ARGS.notification.create_notification)
@error_handler
def create_notification_endpoint(**kwargs):
    """Method to handle the creation of a new notification"""

    # Parse information from the call's body
    data = request.get_json()

    # Get the unit object of the target unit and return if error
    unit = UnitAccess.get_unit(data["unit"])
    if unit.status == "error":
        return unit, 400
    unit = unit.message.info

    # Get the sender's user info
    from_user = UserAccess.get_user(kwargs["id"]).message.info
    from_user_name = (
        from_user.rank + " " + from_user.full_name
        if "rank" in from_user
        else from_user.first_name
    )

    # Check if the user is an officer of a superior unit
    is_above = isOfficerFromAbove(data["unit"], kwargs["id"])

    # Check if the user is rooted or is officer of the unit
    if kwargs["isRoot"] or kwargs["id"] in unit.officers or is_above:
        # Add the notification to the database
        result = NotificationAccess.create_notification(
            **data, author=kwargs["id"]
        )

        # Check if the user wants to notify the people under this unit
        if result.status == "success" and data["notify"]:
            # Prep the contents of the message
            msg_content = {
                "template": "notification",
                "from_user": from_user_name,
                "message": data["notification"],
                "target_unit": unit.name,
                "notification_link": f"{config.wingsuite_dashboard_link}"
                + "/notifications",
            }

            # Send emails
            send_email_by_units(
                unit=unit._id,
                msg_content=msg_content,
                subject="New Notification",
                emoji=config.message_emoji.notification,
            )

        # Return response data
        return result, (200 if result.status == "success" else 400)

    # Return error if not
    return client_error_response("You don't have access to this feature")


#   endregion

#
#   READ OPERATIONS
#   region
#


@get_notification_info.route("/get_notification_info/", methods=["GET"])
@permissions_required(["notification.get_notification_info"])
@param_check(ARGS.notification.get_notification_info)
@error_handler
def get_notification_info_endpoint(**kwargs):
    """Method to get the info of a notification"""

    # Parse information from the call's body
    data = request.get_json()

    # Get the id of the target notification
    id = data.pop("id")

    # Get the notification's information from the database
    result = NotificationAccess.get_notification(id)

    # Return error if no notification was provided
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


@update_notification.route("/update_notification/", methods=["POST"])
@is_root
@permissions_required(["notification.update_notification"])
@param_check(ARGS.notification.update_notification)
@error_handler
def update_notification_endpoint(**kwargs):
    """Method to handle the update of a notification"""

    # Parse information from the call's body
    data = request.get_json()

    # Get the id of the target notification
    id = data.pop("id")

    # Get the notification
    notification = NotificationAccess.get_notification(id)

    # Check if the unit exists
    if notification.status == "error":
        return notification

    # Extract unit from notification
    notification = notification.message.info
    unit = UnitAccess.get_unit(notification.unit).message.info

    # Check if the user is an officer of a superior unit
    is_above = isOfficerFromAbove(unit._id, kwargs["id"])

    # Check if the user is rooted or is officer of the unit
    if kwargs["isRoot"] or kwargs["id"] in unit.officers or is_above:
        # Add the notification to the database
        result = NotificationAccess.update_notification(id, **data)

        # Return response data
        return result, (200 if result.status == "success" else 400)

    # Return error if not
    return client_error_response("You don't have access to this feature")


#   endregion

#
#   DELETE OPERATIONS
#   region
#


@delete_notification.route("/delete_notification/", methods=["POST"])
@is_root
@permissions_required(["notification.delete_notification"])
@param_check(ARGS.notification.delete_notification)
@error_handler
def delete_notification_endpoint(**kwargs):
    """Method to handle the deletion of a notification"""

    # Parse information from the call's body
    data = request.get_json()

    # Get the notification
    notification = NotificationAccess.get_notification(**data)

    # Check if the unit exists
    if notification.status == "error":
        return notification

    # Get the unit object of the target unit
    unit = UnitAccess.get_unit(notification.message.info.unit)
    if unit.status == "error":
        return unit, 400
    unit = unit.message.info

    # Check if the user is an officer of a superior unit
    is_above = isOfficerFromAbove(unit._id, kwargs["id"])

    # Check if the user is rooted or is officer of the unit
    if kwargs["isRoot"] or kwargs["id"] in unit.officers or is_above:
        # Add the event to the database
        result = NotificationAccess.delete_notification(**data)

        # Return response data
        return result, (200 if result.status == "success" else 400)


#   endregion
