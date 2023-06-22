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
    get_feedback,
)
from flask_jwt_extended import jwt_required, decode_token
from flask import request
from database.statistics.feedback import FeedbackAccess
from database.user import UserAccess
from config.config import permissions


@add_permissions.route("/add_permissions/", methods=["POST"])
@permissions_required(["user.add_permissions"])
@param_check(ARGS.user.add_permissions)
def add_permissions_endpoint():
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
def delete_permissions_endpoint():
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
def who_am_i_endpoint():
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
def everyone_endpoint():
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

        # Return the content of the information
        return results, 200

    # Error handling
    except Exception as e:
        return serverErrorResponse(str(e))


@get_feedback.route("/get_feedback/", methods=["POST"])
@param_check(ARGS.user.get_feedback)
@jwt_required()
def get_feedback_endpoint():
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

        # If the resulting information is in error, respond with error
        if results.status == "error":
            return clientErrorResponse(results.message)

        # Return the content of the information
        return results, (200 if results.status == "success" else 400)

    # Error handling
    except Exception as e:
        return serverErrorResponse(str(e))
