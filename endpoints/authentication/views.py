# Import the test blueprint
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
)
from . import (
    login,
    refresh,
    register,
    authorize,
    reject,
    signout,
)
from endpoints.base import (
    permissions_required,
    param_check,
    error_handler,
    ARGS,
)
from database.user import UserAccess
from flask import request


@login.route("/login/", methods=["POST"])
@param_check(ARGS.authentication.login)
@error_handler
def login_endpoint(**kwargs):
    """Log In Handling"""

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


@refresh.route("/refresh/", methods=["POST"])
@jwt_required(refresh=True)
@error_handler
def refresh_endpoint(**kwargs):
    """Method to refresh user's access token"""

    # Get the identity from the refresh token
    current_user = get_jwt_identity()

    # Create a new access token
    new_token = create_access_token(identity=current_user)

    # Return the new token
    return {"access_token": new_token}, 200


@register.route("/register/", methods=["POST"])
@param_check(ARGS.authentication.register)
@error_handler
def register_endpoint(**kwargs):
    """Log In Handling"""

    # Parse information from the call's body
    data = request.get_json()

    # Get the user's instance based on the given information
    result = UserAccess.register_user(**data)

    # Return response data
    return result, (200 if result.status == "success" else 400)


@authorize.route("/authorize_user/", methods=["POST"])
@permissions_required(["auth.authorize_user"])
@param_check(ARGS.authentication.authorize_user)
@error_handler
def authorize_user_endpoint(**kwargs):
    """Log In Handling"""

    # Parse information from the call's body
    data = request.get_json()

    # Get the user's instance based on the given information
    result = UserAccess.add_user(data["id"])

    # Return response data
    return result, (200 if result.status == "success" else 400)


@reject.route("/reject_user/", methods=["POST"])
@permissions_required(["auth.reject_user"])
@param_check(ARGS.authentication.reject_user)
@error_handler
def reject_user_endpoint(**kwargs):
    """Log In Handling"""

    # Parse information from the call's body
    data = request.get_json()

    # Get the user's instance based on the given information
    result = UserAccess.reject_user(data["id"])

    # Return response data
    return result, (200 if result.status == "success" else 400)


@signout.route("/signout/", methods=["POST"])
@param_check(ARGS.authentication.signout)
@jwt_required()
@error_handler
def signout_endpoint(**kwargs):
    """Sign Out Handling"""

    # Parse information from the call's body
    access = request.get_json()["access"]
    refresh = request.get_json()["refresh"]

    # Get the user's instance based on the given information
    result = UserAccess.handle_jwt_blacklisting(access, refresh)

    # Return response data
    return result, (200 if result.status == "success" else 400)
