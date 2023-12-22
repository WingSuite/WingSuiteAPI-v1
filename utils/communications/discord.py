# Imports
from database.unit import UnitAccess
from typing import List, Any
import requests


def send_discord_message(
    url: str,
    title: str,
    message: str,
    emoji: str = "🔔",
    at_everyone: bool = False,
    fields: List[dict] = {},
) -> bool:
    """Sends a Discord embedded message with org name and icon"""

    # Try
    try:
        # Define image url
        image = "https://avatars.githubusercontent.com/u/134102646?s=200&v=4"

        # Define bot name
        emoji = emoji + " " if emoji else ""

        # Define the content of the embedded message
        embed = {
            "title": title,
            "description": message,
            "color": 0x54C0FF,
            "fields": fields,
        }

        # Set a custom username and avatar for the webhook
        data = {
            "username": f"{emoji}WingSuite",
            "avatar_url": image,
            "embeds": [embed],
        }

        # Include @everyone if the at_everyone is provided
        if at_everyone:
            data["content"] = "@everyone"

        # Send the message with the defined content
        requests.post(url, json=data)

        # Return
        return True

    # Return false on error
    except Exception:
        return False


def send_discord_message_by_units(
    unit: str,
    message: dict,
    title: str,
    fields: List[dict] = {},
    **kwargs: Any,
) -> bool:
    """Helper function to send discord message by units"""

    # Try
    try:
        # Get units below the current unit
        units = UnitAccess.get_units_below([unit]).message

        # Iterate through the unit list and send discord messages if they
        # have a proper discord embed link
        for i in units:
            # If there is no communication field in the unit's info, continue
            if "communications" not in i:
                continue

            # If there is no proper discord link, continue
            if "discord" not in i.communications:
                continue

            # Send an email with the HTML content
            send_discord_message(
                url=i.communications.discord.channel,
                title=title,
                message=message,
                fields=fields,
                at_everyone=i.communications.discord.ping_everyone
            )

        # Return true
        return True

    # Return false on error
    except Exception:
        return False
