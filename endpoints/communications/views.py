# Import the test blueprint
from endpoints.base import (  # noqa
    is_root,  # noqa
    success_response,
    client_error_response,
    permissions_required,
    param_check,
    error_handler,
    ARGS,
)
from . import send_user_email_message, send_unit_discord_message
from utils.communications.discord import send_discord_message_to_channel
from utils.communications.email import send_email
from database.unit import UnitAccess
from database.user import UserAccess
from flask import request

#
#   CREATE OPERATIONS
#   region
#


@send_user_email_message.route("/send_user_email_message/", methods=["POST"])
@permissions_required(["communications.send_user_email_message"])
@param_check(ARGS.communications.send_user_email_message)
@error_handler
def send_user_email_message_endpoint(**kwargs):
    """Send email to a user based on given title and message"""

    # Extract body data
    data = request.get_json()

    # Get the user's email
    user = UserAccess.get_user(data["id"])
    if user.status == "error":
        return user, 400
    email = user.message.info.email

    # Send email
    result = send_email(
        receiver=email, subject=data["title"], content=data["message"]
    )

    # Return response information
    return (
        success_response("Email sent")
        if result
        else client_error_response("Email was unable to be sent")
    )


@send_unit_discord_message.route(
    "/send_unit_discord_message/", methods=["POST"]
)
@permissions_required(["communications.send_unit_discord_message"])
@param_check(ARGS.communications.send_unit_discord_message)
@error_handler
def send_unit_discord_message_endpoint(**kwargs):
    """Send discord message based on given title and message"""

    # Extract body data
    data = request.get_json()

    # Get unit's object representation
    unit = UnitAccess.get_unit(data["id"])
    if unit.status == "error":
        return unit, 400
    unit = unit.message.info

    # Get unit's url link
    if "discord" not in unit.communications:
        return client_error_response(
            "Unit does not have a discord channel setup for notifications"
        )
    if not unit.communications.discord.channel:
        return client_error_response(
            "Unit does not have a discord channel setup for notifications"
        )
    url = unit.communications.discord.channel

    # Send message
    result = send_discord_message_to_channel(
        url=url, title=data["title"], message=data["message"]
    )

    # Return response information
    return (
        success_response("Message sent")
        if result
        else client_error_response("Message was unable to be sent")
    )


# endregion

#
#   READ OPERATIONS
#   region
#


# endregion

#
#   UPDATE OPERATIONS
#   region
#


# endregion

#
#   DELETE OPERATIONS
#   region
#


# endregion
