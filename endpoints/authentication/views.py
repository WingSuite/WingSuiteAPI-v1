# Import the test blueprint
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
)
from . import (
    register,
    login,
    get_register_requests,
    refresh,
    authorize,
    signout,
    reject,
    kick_user,
)
from endpoints.base import (
    is_root,
    permissions_required,
    param_check,
    error_handler,
    ARGS,
)
from utils.communications.email import send_email
from utils.html import read_html_file
from database.user import UserAccess
from config.config import config
from flask import request

#
#   CREATE OPERATIONS
#   region
#


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


#   endregion

#
#   READ OPERATIONS
#   region
#


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


@get_register_requests.route("/get_register_requests/", methods=["GET"])
@permissions_required(["auth.get_register_requests"])
@error_handler
def get_register_requests_endpoint(**kwargs):
    """Get list of requests"""

    # Get the list of register information
    result = UserAccess.get_register_list()

    # If the response data results in an error, return 400
    # and error message
    if result.status != "success":
        return result, 400

    # Return success
    return result, 200


#   endregion

#
#   UPDATE OPERATIONS
#   region
#


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


@authorize.route("/authorize_user/", methods=["POST"])
@is_root
@permissions_required(["auth.authorize_user"])
@param_check(ARGS.authentication.authorize_user)
@error_handler
def authorize_user_endpoint(**kwargs):
    """Log In Handling"""

    # Parse information from the call's body
    data = request.get_json()

    # Get the user's instance based on the given information
    result = UserAccess.add_user(data["id"])

    # Notify user of the new feedback
    if result.status == "success":
        # Extract user info
        user = result.user_info

        # Calculate the recipient's and sender's appropriate name
        to_user_name = (
            user.rank + " " + user.full_name
            if "rank" in user
            else user.first_name
        )

        # Get feedback HTML content
        content = read_html_file(
            "authorized",
            to_user=to_user_name,
            detachment_name=config.organization_name,
            wingsuite_link=f"{config.wingsuite_link}/homepage"
        )

        # Send an email with the HTML content
        send_email(
            receiver=user.email,
            subject="Access Granted",
            content=content,
            emoji=config.message_emoji.authentication.accepted,
        )

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


#   endregion

#
#   DELETE OPERATIONS
#   region
#


@reject.route("/reject_user/", methods=["POST"])
@is_root
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


@kick_user.route("/kick_user/", methods=["POST"])
@is_root
@permissions_required(["auth.kick_user"])
@param_check(ARGS.authentication.kick_user)
@error_handler
def kick_user_endpoint(**kwargs):
    """Endpoint to kick a user"""

    # Parse information from the call's body
    data = request.get_json()

    # Get the target user's object
    user = UserAccess.get_user(data["id"])

    # If content is not in result of getting the user, return the
    # error message
    if user.status == "error":
        return user, 400

    # Get the content from the user fetch
    user = user.message.info

    # Kick the user out
    result = UserAccess.kick_user(user._id)

    # Notify user of the new feedback
    if result.status == "success":
        # Calculate the recipient's and sender's appropriate name
        to_user_name = (
            user.rank + " " + user.full_name
            if "rank" in user
            else user.first_name
        )

        # Get feedback HTML content
        content = read_html_file(
            "kicked",
            to_user=to_user_name,
            detachment_name=config.organization_name,
        )

        # Send an email with the HTML content
        send_email(
            receiver=user.email,
            subject="You Have Been Kicked Out",
            content=content,
            emoji=config.message_emoji.authentication.rejected,
        )

    # Return response data
    return result, (200 if result.status == "success" else 400)


#   endregion
