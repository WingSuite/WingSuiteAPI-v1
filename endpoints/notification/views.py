# Import the test blueprint
from endpoints.base import (
    permissions_required,
    param_check,
    serverErrorResponse,
    clientErrorResponse,
    ARGS,
)
from . import (
    create_notification,
    update_notification,
    get_notification_info,
    delete_notification,
)
from flask import request
from database.notification import NotificationAccess
from database.unit import UnitAccess


@create_notification.route("/create_notification/", methods=["POST"])
@permissions_required(["notification.create_notification"])
@param_check(ARGS.notification.create_notification)
def create_notification_endpoint(**kwargs):
    """Method to handle the creation of a new notification"""

    # Try to parse information
    try:
        # Parse information from the call's body
        data = request.get_json()

        # Get the unit object of the target unit
        unit = UnitAccess.get_unit(data["unit"])

        # Check if the unit exists
        if unit.status == "error":
            return unit

        # Extract unit information
        unit = unit.message.info

        # Check if the user is rooted or is officer of the unit
        if kwargs["isRoot"] or kwargs["id"] in unit.officers:
            # Add the notification to the database
            result = NotificationAccess.create_notification(
                **data, author=kwargs["id"]
            )

            # Return response data
            return result, (200 if result.status == "success" else 400)

        # Return error if not
        return clientErrorResponse("You don't have access to this feature")

    # Error handling
    except Exception as e:
        return serverErrorResponse(str(e))


@update_notification.route("/update_notification/", methods=["POST"])
@permissions_required(["notification.update_notification"])
@param_check(ARGS.notification.update_notification)
def update_notification_endpoint(**kwargs):
    """Method to handle the update of a notification"""

    # Try to parse information
    try:
        # Parse information from the call's body
        data = request.get_json()

        # Get the id of the target notification
        id = data.pop("id")

        # Get the notification
        notification = NotificationAccess.get_notification(id)

        # Check if the unit exists
        if notification.status == "error":
            return notification

        # Extract notification
        notification = notification.message.info

        # Get the unit from notification
        unit = UnitAccess.get_unit(notification.unit).message.info

        print(unit)

        # Check if the user is rooted or is officer of the unit
        if kwargs["isRoot"] or kwargs["id"] in unit.officers:
            # Add the notification to the database
            result = NotificationAccess.update_notification(id, **data)

            # Return response data
            return result, (200 if result.status == "success" else 400)

        # Return error if not
        return clientErrorResponse("You don't have access to this feature")

    # Error handling
    except Exception as e:
        return serverErrorResponse(str(e))


@get_notification_info.route("/get_notification_info/", methods=["GET"])
@permissions_required(["notification.get_notification_info"])
@param_check(ARGS.notification.get_notification_info)
def get_notification_info_endpoint(**kwargs):
    """Method to get the info of a notification"""

    # Try to parse information
    try:
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

    # Error handling
    except Exception as e:
        return serverErrorResponse(str(e))


@delete_notification.route("/delete_notification/", methods=["POST"])
@permissions_required(["notification.delete_notification"])
@param_check(ARGS.notification.delete_notification)
def delete_notification_endpoint(**kwargs):
    """Method to handle the deletion of a notification"""

    # Try to parse information
    try:
        # Parse information from the call's body
        data = request.get_json()

        # Get the notification
        notification = NotificationAccess.get_notification(**data)

        # Check if the unit exists
        if notification.status == "error":
            return notification

        # Get the unit object of the target unit
        unit = UnitAccess.get_unit(notification.message.info.unit)

        # Check if the unit exists
        if unit.status == "error":
            return unit

        # Extract unit information
        unit = unit.message.info

        # Check if the user is rooted or is officer of the unit
        if kwargs["isRoot"] or kwargs["id"] in unit.officers:
            # Add the event to the database
            result = NotificationAccess.delete_notification(**data)

            # Return response data
            return result, (200 if result.status == "success" else 400)

    # Error handling
    except Exception as e:
        return serverErrorResponse(str(e))
