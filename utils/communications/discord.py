# Imports
import requests


def send_discord_message_to_channel(
    url: str, title: str, message: str, emoji: str = "🔔"
) -> bool:
    """Sends a Discord embedded message with org name and icon"""

    # Try
    try:
        # Define image url
        image = "https://avatars.githubusercontent.com/u/134102646?s=200&v=4"

        # Define bot name
        emoji = emoji + ' ' if emoji else ''

        # Define the content of the embedded message
        embed = {
            "title": title,
            "description": message,
            "color": 0x54C0FF,
        }

        # Set a custom username and avatar for the webhook
        data = {
            "username": f"{emoji}WingSuite",
            "avatar_url": image,
            "embeds": [embed],
        }

        # Send the message with the defined content
        requests.post(url, json=data)

        # Return
        return True

    # Return false on error
    except Exception:
        return False
