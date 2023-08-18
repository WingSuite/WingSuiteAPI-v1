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
    password_reset_request,
    refresh,
    authorize,
    signout,
    reset_password,
    reject,
    kick_user,
)
from endpoints.base import (
    success_response,
    client_error_response,
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
import datetime
import uuid

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


@password_reset_request.route("/password_reset_request/", methods=["POST"])
@param_check(ARGS.authentication.password_reset_request)
@error_handler
def password_reset_request_endpoint(**kwargs):
    """Method to request password reset"""

    # Parse information from the call's body
    data = request.get_json()

    # Get the user's email
    user = UserAccess.get_user(id="_email", email=data["email"])
    if user.status == "error":
        return user, 400
    user = user.message.info

    # Generate a reset token and update the user's info
    token = str(uuid.uuid4())
    UserAccess.update_user(
        id=user._id,
        reset_token=token,
        token_expiry=datetime.datetime.now()
        + datetime.timedelta(minutes=config.JWT.password_reset_expiry),
    )

    # Get the user's proper name
    to_user_name = (
        user.rank + " " + user.full_name if "rank" in user else user.first_name
    )

    # Get password reset HTML content
    content = read_html_file(
        "auth.reset_request",
        to_user=to_user_name,
        reset_link=f"{config.wingsuite_link}/reset?token={token}",
    )

    # Send message to the user
    send_email(
        receiver=data["email"],
        subject="Password Reset",
        content=content,
        emoji=config.message_emoji.authentication.reset,
    )

    # Send success message
    return success_response(
        "Your password reset link has been sent to your email. You have 5 "
        + "minutes to reset it, before the link expires."
    )


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
            "auth.authorized",
            to_user=to_user_name,
            wingsuite_link=f"{config.wingsuite_dashboard_link}/homepage",
        )

        # Send an email with the HTML content
        send_email(
            receiver=user.email,
            subject="Access Granted",
            content=content,
            emoji=config.message_emoji.authentication.accepted,
        )

    # Return response data
    return {"message": result.message, "status": result.status}, (
        200 if result.status == "success" else 400
    )


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


@reset_password.route("/reset_password/", methods=["POST"])
@param_check(ARGS.authentication.reset_password)
@error_handler
def password_reset_endpoint(**kwargs):
    """Endpoint to reset password"""

    # Extract the body information
    token = request.json["token"]
    new_password = request.json["new_password"]

    # Get the user with the token
    user = UserAccess.get_user_with_reset_token(token)

    # Return error message if the nothing is found
    if not user:
        return client_error_response(
            "Invalid or expired token. Request a new link."
        )

    # Update the user's password
    result = UserAccess.update_user_password(user._id, new_password)

    # Return success
    return success_response(result.message)


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
        # Calculate the recipient's appropriate name
        to_user_name = (
            user.rank + " " + user.full_name
            if "rank" in user
            else user.first_name
        )

        # Get feedback HTML content
        content = read_html_file(
            "auth.kicked",
            to_user=to_user_name,
        )

        # Send an email with the HTML content
        send_email(
            receiver=user.email,
            subject="You Have Been Kicked Out",
            content=content,
            emoji=config.message_emoji.authentication.kicked,
        )

    # Return response data
    return result, (200 if result.status == "success" else 400)


#   endregion
