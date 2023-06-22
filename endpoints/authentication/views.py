# Import the test blueprint
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
)
from . import (
    login,
    register,
    authorize,
    reject,
    signout,
)
from endpoints.base import (
    permissions_required,
    param_check,
    serverErrorResponse,
    ARGS,
)
from database.user import UserAccess
from flask import request


@login.route("/login/", methods=["GET"])
@param_check(ARGS.authentication.login)
def login_endpoint():
    """Log In Handling"""

    # Try to parse information
    try:
        # Parse information from the call's body
        data = request.get_json()

        # Get the user's instance based on the given information
        result = UserAccess.login(**data)

        # If the response data results in an error, return 400
        # and error message
        if result.status != "success":
            return result, 400

        # Create refresh and access token
        identity = {
            "email": result.message.info.email,
            "_id": result.message.info._id,
        }
        access_token = create_access_token(identity=identity)
        refresh_token = create_refresh_token(identity=identity)

        # Return response data except for the password
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }, 200

    # Error handling
    except Exception as e:
        return serverErrorResponse(str(e))


@register.route("/register/", methods=["POST"])
@param_check(ARGS.authentication.register)
def register_endpoint():
    """Log In Handling"""

    # Try to parse information
    try:
        # Parse information from the call's body
        data = request.get_json()

        # Get the user's instance based on the given information
        result = UserAccess.register_user(**data)

        # Return response data
        return result, (200 if result.status == "success" else 400)

    # Error handling
    except Exception as e:
        return serverErrorResponse(str(e))


@authorize.route("/authorize_user/", methods=["POST"])
@permissions_required(["auth.authorize_user"])
@param_check(ARGS.authentication.authorize_user)
def authorize_user_endpoint():
    """Log In Handling"""

    # Try to parse information
    try:
        # Parse information from the call's body
        data = request.get_json()

        # Get the user's instance based on the given information
        result = UserAccess.add_user(data["id"])

        # Return response data
        return result, (200 if result.status == "success" else 400)

    # Error handling
    except Exception as e:
        return serverErrorResponse(str(e))


@reject.route("/reject_user/", methods=["POST"])
@permissions_required(["auth.reject_user"])
@param_check(ARGS.authentication.reject_user)
def reject_user_endpoint():
    """Log In Handling"""

    # Try to parse information
    try:
        # Parse information from the call's body
        data = request.get_json()

        # Get the user's instance based on the given information
        result = UserAccess.reject_user(data["id"])

        # Return response data
        return result, (200 if result.status == "success" else 400)

    # Error handling
    except Exception as e:
        return serverErrorResponse(str(e))


@signout.route("/signout/", methods=["POST"])
@param_check(ARGS.authentication.signout)
@jwt_required()
def signout_endpoint():
    """Sign Out Handling"""

    # Try to parse information
    try:
        # Parse information from the call's body
        access = request.get_json()["access"]
        refresh = request.get_json()["refresh"]

        # Get the user's instance based on the given information
        result = UserAccess.handle_jwt_blacklisting(access, refresh)

        # Return response data
        return result, (200 if result.status == "success" else 400)

    # Error handling
    except Exception as e:
        return serverErrorResponse(str(e))
