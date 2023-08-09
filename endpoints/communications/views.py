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
from . import send_email, send_unit_discord_message  # noqa
from utils.communications.discord import send_discord_message_to_channel
from database.unit import UnitAccess
from flask_jwt_extended import jwt_required, decode_token  # noqa
from flask import request
from config.config import permissions, config  # noqa

#
#   CREATE OPERATIONS
#   region
#


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
    if "update_channel" not in unit:
        return client_error_response(
            "Unit does not have their notifier channel setup"
        )
    url = unit.update_channel

    # Send message
    result = send_discord_message_to_channel(
        url=url, title=data["title"], message=data["message"]
    )

    # Return response information
    return (
        success_response("Message sent")
        if result
        else client_error_response("Message unable to be sent")
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
