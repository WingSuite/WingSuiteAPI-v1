# Import the test blueprint
from endpoints.base import (
    is_root,
    success_response,
    client_error_response,
    permissions_required,
    param_check,
    error_handler,
    ARGS,
)
from . import (
    add_permissions,
    who_am_i,
    everyone,
    get_user,
    get_feedbacks,
    get_events,
    get_notifications,
    get_pfa_data,
    get_warrior_data,
    get_tasks,
    get_users_units,
    get_permissions_list,
    update_permissions,
    update_rank,
    delete_permissions,
)
from flask_jwt_extended import jwt_required, decode_token
from flask import request
from database.statistic.feedback import FeedbackAccess
from database.statistic.warrior import WarriorAccess
from database.statistic.task import TaskAccess
from database.statistic.pfa import PFAAccess
from database.notification import NotificationAccess
from database.event import EventAccess
from database.user import UserAccess
from database.unit import UnitAccess
from config.config import permissions, config
import json

#
#   CREATE OPERATIONS
#   region
#


@add_permissions.route("/add_permissions/", methods=["POST"])
@permissions_required(["user.add_permissions"])
@param_check(ARGS.user.add_permissions)
@error_handler
def add_permissions_endpoint(**kwargs):
    """Method to handle the adding of new permissions to the user"""

    # Parse information from the call's body
    data = request.get_json()

    # Get the target user's object
    user = UserAccess.get_user(data["id"])

    # If content is not in result of getting the user, return the
    # error message
    if user.status == "error":
        return user, 400

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
        results[permission] = "Added" if res else "Not Added (Already Added)"

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
    return success_response(message)


#   endregion

#
#   READ OPERATIONS
#   region
#


@who_am_i.route("/who_am_i/", methods=["GET"])
@jwt_required()
@error_handler
def who_am_i_endpoint(**kwargs):
    """Method to return the user's information"""

    # Get the access token
    token = request.headers.get("Authorization", None).split()[1]

    # Decode the JWT Token and get the ID of the user
    id = decode_token(token)["sub"]["_id"]

    # Get the user based on the ID
    result = UserAccess.get_user(id)
    content = result.message.get_generic_info()

    # Return the results of the database query
    return content, (200 if result.status == "success" else 400)


@everyone.route("/everyone/", methods=["POST"])
@is_root
@param_check(ARGS.user.everyone)
@jwt_required()
@error_handler
def everyone_endpoint(**kwargs):
    """Method to get every person in the user's database"""

    # Parse information from the call's body
    data = request.get_json()

    # Get the user and their permissions
    perms = UserAccess.get_user(id=kwargs["id"]).message.info.permissions

    # Create protections for the result
    protections = ["phone_number", "permissions"]

    # If the user has the right perms, remove the permissions protection
    if (
        kwargs["isRoot"]
        or "user.everyone.permission_view" in perms
        and "allow_permissions" in data
    ):
        del protections[1]
    if "allow_permissions" in data:
        del data["allow_permissions"]

    # If the user has the right perms, remove the phone protection
    if (
        kwargs["isRoot"]
        or "user.everyone.phone_number_view" in perms
        and "allow_phone_number" in data
    ):
        del protections[0]
    if "allow_phone_number" in data:
        del data["allow_phone_number"]

    # Get the content information based on the given page size and
    # page index
    results = UserAccess.get_all_users(**data)

    # If the resulting information is in error, respond with error
    if results.status == "error":
        return client_error_response(results.message)

    # Format message
    results.message = [
        item.get_generic_info(other_protections=protections)
        for item in results.message
    ]

    # Return the content of the information
    return results, 200


@get_user.route("/get_user/", methods=["POST"])
@param_check(ARGS.user.get_user)
@jwt_required()
@error_handler
def get_user_endpoint(**kwargs):
    """Endpoint to get the user's information"""

    # Parse information from the call's body
    data = request.get_json()

    # Get the id of the target unit
    id = data.pop("id")

    # Get the unit's information from the database
    result = UserAccess.get_user(id)

    # If the resulting information is in error, respond with error
    if result.status == "error":
        return client_error_response(result.message)

    result.message = result.message.get_generic_info(
        other_protections=["phone_number", "permissions"]
    )

    # Return response data
    return result, (200 if result.status == "success" else 400)


@get_feedbacks.route("/get_feedbacks/", methods=["POST"])
@param_check(ARGS.user.get_feedback)
@jwt_required()
@error_handler
def get_feedback_endpoint(**kwargs):
    """Method to get the feedback information for a user"""

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
        return client_error_response(results.message)

    # Return the content of the information
    return results, (200 if results.status == "success" else 400)


@get_events.route("/get_events/", methods=["POST"])
@param_check(ARGS.user.get_events)
@jwt_required()
@error_handler
def get_events_endpoint(**kwargs):
    """Method to get the events based on the user's units"""

    # Parse information from the call's body
    data = request.get_json()

    # Get the access token
    token = request.headers.get("Authorization", None).split()[1]

    # Decode the JWT Token and get the ID of the user
    id = decode_token(token)["sub"]["_id"]

    # Get the user's information from the database
    result = UserAccess.get_user(id)

    # Extract user info
    result = result.message.info

    # Check if the user is admin
    isAdmin = config.root_permission_string in result.permissions

    # If the user is an admin, get all of the unit IDs
    units = result.units
    if isAdmin:
        units = UnitAccess.get_all_units(page_size=2000, page_index=0).message
        units = [item.info._id for item in units]

    # Setup information for iteration
    user_events = {}
    iterable_units = []
    units_above = UnitAccess.get_units_above(units).message
    for i in units_above:
        # Check if the user is an officer for the iterated unit
        if id in i.officers:
            # Get the units below
            temp_below = UnitAccess.get_units_below([i._id]).message

            # Append to iterable_units
            iterable_units += temp_below
    iterable_units += units_above

    # Iterate through the user's units and get their event information
    for i in iterable_units:
        # Get event info
        events = EventAccess.get_event_by_unit_id(
            i._id, data["start_datetime"], data["end_datetime"]
        )

        # If the queried event(s) is not None add em
        if events.status == "success":
            for event in events.message:
                user_events[event.info._id] = event.info

    # Turn user_events into a list of content
    user_events = [user_events[item] for item in user_events]

    # Sort the user events by start datetime
    user_events = sorted(user_events, key=lambda x: x["start_datetime"])

    # Return response data
    return success_response(user_events)


@get_notifications.route("/get_notifications/", methods=["POST"])
@param_check(ARGS.user.get_notifications)
@jwt_required()
@error_handler
def get_notifications_endpoint(**kwargs):
    """Method to get notifications based on the user's units"""

    # Parse information from the call's body
    data = request.get_json()

    # Get the access token
    token = request.headers.get("Authorization", None).split()[1]

    # Decode the JWT Token and get the ID of the user
    id = decode_token(token)["sub"]["_id"]

    # Get the user's information from the database
    result = UserAccess.get_user(id)

    # Extract user info
    result = result.message.info

    # Check if the user is admin
    isAdmin = config.root_permission_string in result.permissions

    # If the user is an admin, get all of the unit IDs
    units = result.units
    if isAdmin:
        units = UnitAccess.get_all_units(page_size=2000, page_index=0).message
        units = [item.info._id for item in units]

    # Setup information for iteration
    user_notifications = {}
    iterable_units = []
    units_above = UnitAccess.get_units_above(units).message
    for i in units_above:
        # Check if the user is an officer for the iterated unit
        if id in i.officers:
            # Get the units below
            temp_below = UnitAccess.get_units_below([i._id]).message

            # Append to iterable_units
            iterable_units += temp_below
    iterable_units += units_above

    # Iterate through the user's units and get their event information
    for i in iterable_units:
        # Get event info
        notifications = NotificationAccess.get_notification_by_unit_id(
            i._id, data["start_datetime"], data["end_datetime"]
        )

        # If the queried event(s) is not None add em
        if notifications.status == "success":
            for notification in notifications.message:
                user_notifications[notification.info._id] = notification.info

    # Turn user_events into a list of content
    user_notifications = [
        user_notifications[item] for item in user_notifications
    ]

    # Sort the user events by start datetime
    # TODO: Have sorting be handled by user's end
    user_notifications = sorted(
        user_notifications,
        key=lambda x: x["created_datetime"],
        reverse=True,
    )

    # Return response data
    return success_response(user_notifications)


@get_pfa_data.route("/get_pfa_data/", methods=["POST"])
@param_check(ARGS.user.get_pfa_data)
@jwt_required()
@error_handler
def get_pfa_data_endpoint(**kwargs):
    """Endpoint to get user's PFA information"""

    # Parse information from the call's body
    data = request.get_json()

    # Get the access token
    token = request.headers.get("Authorization", None).split()[1]

    # Decode the JWT Token and get the ID of the user
    id = decode_token(token)["sub"]["_id"]

    # Get PFA information based on the user's id
    result = PFAAccess.get_user_pfa(id=id, **data)

    # Sort the user events by start datetime
    result.message = sorted(
        result.message,
        key=lambda x: x["datetime_taken"],
        reverse=True,
    )

    # Return the information
    return result, 200


@get_warrior_data.route("/get_warrior_data/", methods=["POST"])
@param_check(ARGS.user.get_warrior_data)
@jwt_required()
@error_handler
def get_warrior_data_endpoint(**kwargs):
    """Endpoint to get user's warrior knowledge information"""

    # Parse information from the call's body
    data = request.get_json()

    # Get the access token
    token = request.headers.get("Authorization", None).split()[1]

    # Decode the JWT Token and get the ID of the user
    id = decode_token(token)["sub"]["_id"]

    # Get warrior knowledge information based on the user's id
    result = WarriorAccess.get_user_warrior(id=id, **data)

    # Sort the user events by start datetime
    result.message = sorted(
        result.message,
        key=lambda x: x["datetime_taken"],
        reverse=True,
    )

    # Return the information
    return result, 200


@get_tasks.route("/get_tasks/", methods=["POST"])
@param_check(ARGS.user.get_tasks)
@jwt_required()
@error_handler
def get_tasks_endpoint(**kwargs):
    """Endpoint to get user's task information"""

    # Parse information from the call's body
    data = request.get_json()

    # Get the access token
    token = request.headers.get("Authorization", None).split()[1]

    # Decode the JWT Token and get the ID of the user
    id = decode_token(token)["sub"]["_id"]

    # Get warrior knowledge information based on the user's id
    result = TaskAccess.get_own_task(id=id, **data)

    # If the resulting information is in error, respond with error
    if result.status == "error":
        return client_error_response(result.message)

    # Return the content of the information
    return result, (200 if result.status == "success" else 400)


@get_users_units.route("/get_users_units/", methods=["GET"])
@jwt_required()
@error_handler
def get_users_units_endpoint(**kwargs):
    """Endpoint to the user's available units"""

    # Get the access token
    token = request.headers.get("Authorization", None).split()[1]

    # Decode the JWT Token and get the ID of the user
    id = decode_token(token)["sub"]["_id"]

    # Get the user's information from the database
    user = UserAccess.get_user(id).message.info

    # Check if the user is a root user
    if config.root_permission_string in user.permissions:
        # Get all of the units
        results = UnitAccess.get_all_units(page_size=3000, page_index=0)

        # If the resulting information is in error, respond with error
        if results.status == "error":
            return client_error_response(results.message)

        # Sort and Format message
        results = [item.info for item in results.message]
        results = sorted(
            results,
            key=lambda x: (
                config.unit_types.index(x["unit_type"]),
                x["name"],
            ),
        )

        # Return results
        return success_response(results)

    # Iterate through the units that the user is in
    units = []
    for i in user.units:
        # If the user is an officer in the unit, get all units beneath
        if id in UnitAccess.get_unit(i).message.info.officers:
            # Get the units below
            units_below = UnitAccess.get_units_below([i]).message

            # Iterate through every unit and add a tag for superiority
            for idx, j in enumerate(units_below):
                # Tag the unit
                j.is_superior = True

                # Apply changes
                units_below[idx] = j

            # Update units list
            units += units_below
        # If not, just add the unit iterated
        else:
            # Get the unit
            unit = UnitAccess.get_unit(i).message.info

            # Update unit's information
            unit.is_superior = False

            # Update units list
            units.append(unit)

    # Filter data
    temp = set()
    filtered = []
    for i in units:
        # Add unit ID to set if not in the set and track the unit
        if i._id not in temp:
            temp.add(i._id)
            filtered.append(i)
        # If not, continue
        else:
            continue

    # Sort and Format message
    results = sorted(
        list(filtered),
        key=lambda x: (
            config.unit_types.index(x["unit_type"]),
            x["name"],
        ),
    )

    # Return results
    return success_response(results)


@get_permissions_list.route("/get_permissions_list/", methods=["GET"])
@permissions_required(["user.get_permissions_list"])
@error_handler
def get_permissions_list_endpoint(**kwargs):
    """Returns the full list of permissions"""

    # Get the permissions list
    return success_response(json.load(open("./config/permissions.json")))


#   endregion

#
#   UPDATE OPERATIONS
#   region
#


@update_permissions.route("/update_permissions/", methods=["POST"])
@permissions_required(["user.update_permissions"])
@param_check(ARGS.user.update_permissions)
@error_handler
def update_permissions_endpoint(**kwargs):
    """Method to handle the updating of permissions to the user"""

    # Parse information from the call's body
    data = request.get_json()

    # Get the target user's object
    user = UserAccess.get_user(data["id"])

    # If content is not in result of getting the user, return the
    # error message
    if user.status == "error":
        return user, 400

    # Get the content from the user fetch
    user = user.message

    # Overwrite permission list
    user.info.permissions = data["permissions"]

    # Push changes to collection
    result = UserAccess.update_user(data["id"], **user.info)

    # Return result
    return result, (200 if result.status == "success" else 400)


@update_rank.route("/update_rank/", methods=["POST"])
@permissions_required(["user.update_rank"])
@param_check(ARGS.user.update_rank)
@error_handler
def update_rank_endpoint(**kwargs):
    """Update a selected user's rank"""

    # Parse information from the call's body
    data = request.get_json()

    # Get the target user's object
    user = UserAccess.get_user(data["id"])

    # If content is not in result of getting the user, return the
    # error message
    if user.status == "error":
        return user, 400

    # Get the content from the user fetch
    user = user.message

    # Update the user's info
    result = UserAccess.update_user(id=data["id"], rank=data["rank"])

    # Return result
    return result, (200 if result.status == "success" else 400)


#   endregion

#
#   DELETE OPERATIONS
#   region


@delete_permissions.route("/delete_permissions/", methods=["POST"])
@permissions_required(["user.delete_permissions"])
@param_check(ARGS.user.delete_permissions)
@error_handler
def delete_permissions_endpoint(**kwargs):
    """Method to handle the adding of new permissions to the user"""

    # Parse information from the call's body
    data = request.get_json()

    # Get the target user's object
    user = UserAccess.get_user(data["id"])

    # If content is not in result of getting the user, return the
    # error message
    if user.status == "error":
        return user, 400

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
    return success_response(message)


#   endregion
