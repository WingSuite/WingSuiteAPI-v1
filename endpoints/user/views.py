# Import the test blueprint
from endpoints.base import (
    permissions_required,
    param_check,
    serverErrorResponse,
    clientErrorResponse,
    successResponse,
    ARGS,
)
from . import (
    add_permissions,
    delete_permissions,
    who_am_i,
    everyone,
    get_user,
    get_feedbacks,
    get_events,
    get_notifications,
    get_users_units,
)
from flask_jwt_extended import jwt_required, decode_token
from flask import request
from database.statistics.feedback import FeedbackAccess
from database.notification import NotificationAccess
from database.event import EventAccess
from database.user import UserAccess
from database.unit import UnitAccess
from config.config import permissions, config


@add_permissions.route("/add_permissions/", methods=["POST"])
@permissions_required(["user.add_permissions"])
@param_check(ARGS.user.add_permissions)
def add_permissions_endpoint(**kwargs):
    """Method to handle the adding of new permissions to the user"""

    # Try to parse information
    try:
        # Parse information from the call's body
        data = request.get_json()

        # Get the target user's object
        user = UserAccess.get_user(data["id"])

        # If content is not in result of getting the user, return the
        # error message
        if user.status == "error":
            return user

        # Get the content from the user fetch
        user = user.message

        # Add new permission(s) and track changes
        results = {}
        for permission in data["permissions"]:
            # If the iterated item is not part of the approved list of
            # permission, track that it's not added and continue
            if permission not in permissions:
                results[permission] = "Not Added (Invalid Permission)"
                continue

            # Attempt add permission and track change
            res = user.add_permission(permission)
            results[permission] = (
                "Added" if res else "Not Added (Already Added)"
            )

        # Push changes to collection
        UserAccess.update_user(data["id"], **user.info)

        # Make response dictionary
        message = {
            "status": "success",
            "message": "Permission addition have been applied to "
            + f"{user.get_fullname(lastNameFirst=True)}. Refer to results "
            + "for what has been applied",
            "results": results,
        }

        # Return response data
        return successResponse(message)

    # Error handling
    except Exception as e:
        return serverErrorResponse(str(e))


@delete_permissions.route("/delete_permissions/", methods=["POST"])
@permissions_required(["user.delete_permissions"])
@param_check(ARGS.user.delete_permissions)
def delete_permissions_endpoint(**kwargs):
    """Method to handle the adding of new permissions to the user"""

    # Try to parse information
    try:
        # Parse information from the call's body
        data = request.get_json()

        # Get the target user's object
        user = UserAccess.get_user(data["id"])

        # If content is not in result of getting the user, return the
        # error message
        if user.status == "error":
            return user

        # Get the content from the user fetch
        user = user.message

        # Add new permission(s) and track changes
        results = {}
        for permission in data["permissions"]:
            # If the iterated item is not part of the approved list of
            # permission, track that it's not added and continue
            if permission not in permissions:
                results[permission] = "Not Added (Invalid Permission)"
                continue

            # Attempt add permission and track change
            res = user.delete_permission(permission)
            results[permission] = (
                "Deleted" if res else "Not Deleted (Permission Missing)"
            )

        # Push changes to collection
        UserAccess.update_user(data["id"], **user.info)

        # Make response dictionary
        message = {
            "status": "success",
            "message": "Permission deletion have been applied to "
            + f"{user.get_fullname(lastNameFirst=True)}. Refer to results "
            + "for what has been applied",
            "results": results,
        }

        # Return response data
        return successResponse(message)

    # Error handling
    except Exception as e:
        return serverErrorResponse(str(e))


@who_am_i.route("/who_am_i/", methods=["GET"])
@jwt_required()
def who_am_i_endpoint(**kwargs):
    """Method to return the user's information"""

    # Try to parse information
    try:
        # Get the access token
        token = request.headers.get("Authorization", None).split()[1]

        # Decode the JWT Token and get the ID of the user
        id = decode_token(token)["sub"]["_id"]

        # Get the user based on the ID
        result = UserAccess.get_user(id)
        content = result.message.get_generic_info()

        # Return the results of the database query
        return content, (200 if result.status == "success" else 400)

    # Error handling
    except Exception as e:
        return serverErrorResponse(str(e))


@everyone.route("/everyone/", methods=["POST"])
@param_check(ARGS.user.everyone)
@jwt_required()
def everyone_endpoint(**kwargs):
    """Method to get every person in the user's database"""

    # Try to parse information
    try:
        # Parse information from the call's body
        data = request.get_json()

        # Get the content information based on the given page size and
        # page index
        results = UserAccess.get_users(**data)

        # If the resulting information is in error, respond with error
        if results.status == "error":
            return clientErrorResponse(results.message)

        # Format message
        results.message = [
            item.get_generic_info(
                other_protections=["phone_number", "permissions"]
            )
            for item in results.message
        ]

        # Return the content of the information
        return results, 200

    # Error handling
    except Exception as e:
        return serverErrorResponse(str(e))


@get_user.route("/get_user/", methods=["POST"])
@param_check(ARGS.user.get_user)
@jwt_required()
def get_user_endpoint(**kwargs):
    """Endpoint to get the user's information"""

    # Try to parse information
    try:
        # Parse information from the call's body
        data = request.get_json()

        # Get the id of the target unit
        id = data.pop("id")

        # Get the unit's information from the database
        result = UserAccess.get_user(id)

        # If the resulting information is in error, respond with error
        if result.status == "error":
            return clientErrorResponse(result.message)

        result.message = result.message.get_generic_info(
            other_protections=["phone_number", "permissions"]
        )

        # Return response data
        return result, (200 if result.status == "success" else 400)

    # Error handling
    except Exception as e:
        return serverErrorResponse(str(e))


@get_feedbacks.route("/get_feedbacks/", methods=["POST"])
@param_check(ARGS.user.get_feedback)
@jwt_required()
def get_feedback_endpoint(**kwargs):
    """Method to get the feedback information for a user"""

    # Try to process the endpoint
    try:
        # Parse information from the call's body
        data = request.get_json()

        # Get the access token
        token = request.headers.get("Authorization", None).split()[1]

        # Decode the JWT Token and get the ID of the user
        id = decode_token(token)["sub"]["_id"]

        # Get feedbacks from database
        results = FeedbackAccess.get_own_feedback(id, **data)

        # Reverse feedback order
        results.message = results.message[::-1]

        # If the resulting information is in error, respond with error
        if results.status == "error":
            return clientErrorResponse(results.message)

        # Return the content of the information
        return results, (200 if results.status == "success" else 400)

    # Error handling
    except Exception as e:
        return serverErrorResponse(str(e))


@get_events.route("/get_events/", methods=["POST"])
@param_check(ARGS.user.get_events)
@jwt_required()
def get_events_endpoint(**kwargs):
    """Method to get the events based on the user's units"""

    # Try to parse information
    try:
        # Parse information from the call's body
        data = request.get_json()

        # Get the access token
        token = request.headers.get("Authorization", None).split()[1]

        # Decode the JWT Token and get the ID of the user
        id = decode_token(token)["sub"]["_id"]

        # Get the user's information from the database
        result = UserAccess.get_user(id)

        # Iterate through the user's units and get their event information
        user_events = {}
        for i in result.message.info.units:
            # Set ptr on start of given ID
            ptr = UnitAccess.get_unit(i)

            # Iterate until the very root of the unit's tree
            while ptr.status == "success":
                # Get the unit object
                unit = ptr.message.info

                # Get event info
                events = EventAccess.get_event_by_unit_id(
                    unit._id, data["start_datetime"], data["end_datetime"]
                )

                # If the queried event(s) is not None add em
                if events.status == "success":
                    for event in events.message:
                        user_events[event.info._id] = event.info

                ptr = UnitAccess.get_unit(unit.parent)

        # Turn user_events into a list of content
        user_events = [user_events[item] for item in user_events]

        # Sort the user events by start datetime
        user_events = sorted(user_events, key=lambda x: x["start_datetime"])

        # Return response data
        return successResponse(user_events)

    # Error handling
    except Exception as e:
        return serverErrorResponse(str(e))


@get_notifications.route("/get_notifications/", methods=["POST"])
@param_check(ARGS.user.get_notifications)
@jwt_required()
def get_notifications_endpoint(**kwargs):
    """Method to get notifications based on the user's units"""

    # Try to parse information
    try:
        # Parse information from the call's body
        data = request.get_json()

        # Get the access token
        token = request.headers.get("Authorization", None).split()[1]

        # Decode the JWT Token and get the ID of the user
        id = decode_token(token)["sub"]["_id"]

        # Get the user's information from the database
        result = UserAccess.get_user(id)

        # Iterate through the user's units and get their event information
        user_notifications = {}
        for i in result.message.info.units:
            # Set ptr on start of given ID
            ptr = UnitAccess.get_unit(i)

            # Iterate until the very root of the unit's tree
            while ptr.status == "success":
                # Get the unit object
                unit = ptr.message.info

                # Get event info
                notifications = NotificationAccess.get_notification_by_unit_id(
                    unit._id, data["start_datetime"], data["end_datetime"]
                )

                # If the queried event(s) is not None add em
                if notifications.status == "success":
                    for notification in notifications.message:
                        user_notifications[
                            notification.info._id
                        ] = notification.info

                ptr = UnitAccess.get_unit(unit.parent)

        # Turn user_events into a list of content
        user_notifications = [
            user_notifications[item] for item in user_notifications
        ]

        # Sort the user events by start datetime
        user_notifications = sorted(
            user_notifications,
            key=lambda x: x["created_datetime"],
            reverse=True,
        )

        # Return response data
        return successResponse(user_notifications)

    # Error handling
    except Exception as e:
        return serverErrorResponse(str(e))


@get_users_units.route("/get_users_units/", methods=["GET"])
@jwt_required()
def get_users_units_endpoint(**kwargs):
    """Endpoint to the user's available units"""

    # Try to parse information
    try:
        # Get the access token
        token = request.headers.get("Authorization", None).split()[1]

        # Decode the JWT Token and get the ID of the user
        id = decode_token(token)["sub"]["_id"]

        # Get the user's information from the database
        user = UserAccess.get_user(id).message.info

        # Check if the user is a root user
        if config.rootPermissionString in user.permissions:
            # Get all of the units
            results = UnitAccess.get_units(page_size=3000, page_index=0)

            # If the resulting information is in error, respond with error
            if results.status == "error":
                return clientErrorResponse(results.message)

            # Sort and Format message
            results = [item.info for item in results.message]
            results = sorted(
                results,
                key=lambda x: (
                    config.unitTypes.index(x["unit_type"]),
                    x["name"],
                ),
            )

            # Return results
            return successResponse(results)

        # Create a tracker
        results = []

        # If not, return the content of the user's information
        for item in user.units:
            # Get the unit information
            results.append(UnitAccess.get_unit(item).message.info)

            # Sort and Format message
            results = sorted(
                results,
                key=lambda x: (
                    config.unitTypes.index(x["unit_type"]),
                    x["name"],
                ),
            )

            return successResponse(results)

    # Error handling
    except Exception as e:
        return serverErrorResponse(str(e))
