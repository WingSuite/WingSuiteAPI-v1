# Imports
from utils.html import read_html_file
from database.unit import UnitAccess
from database.user import UserAccess
from email.message import EmailMessage
from config.config import config
from typing import Any, Union
import smtplib


def send_email(
    receiver: Union[str, list], subject: str, content: str, emoji: str = "🔔"
) -> bool:
    """Helper function to send an email to a user"""

    # Convert receivers to a list if it is a single string
    if isinstance(receiver, str):
        receiver = [receiver]

    # Create a new SMTP connection
    with smtplib.SMTP_SSL(
        config.email.smtp_server, config.email.smtp_port
    ) as server:
        # Try
        try:
            # Login to the SMTP server
            server.login(config.email.sender_email, config.email.password)

            # Create the message
            emoji = emoji + " " if emoji else ""
            message = EmailMessage()
            message["Subject"] = "NOTIFICATION // " + subject
            message[
                "From"
            ] = f"{emoji}‎ WingSuite <{config.email.sender_email}>"
            message["BCC"] = receiver
            message.set_content(content)

            # Add the HTML content as an alternative to plain text content
            message.add_alternative(content, subtype="html")

            # Send message
            server.send_message(message)

            # Return true
            print("Email sent -", receiver)
            return True

        # Return false on error
        except Exception:
            print("Error occurred")
            return False


def send_email_by_units(
    unit: str, msg_content: dict, subject: str, emoji: str, **kwargs: Any
) -> bool:
    """Helper function to send email by units"""

    # Try
    try:
        # Get units below the current unit
        units = UnitAccess.get_units_below([unit]).message

        # Iterate through the units and add the members and officers into
        # a set for message dispatch
        personnel = set()
        for i in units:
            personnel = personnel.union(i.members)
            personnel = personnel.union(i.officers)
        personnel = [UserAccess.get_user(i).message.info for i in personnel]
        personnel = [i.email for i in personnel]

        # Get feedback HTML content
        content = read_html_file(**msg_content)

        # Send an email with the HTML content
        send_email(
            receiver=personnel,
            subject=subject,
            content=content,
            emoji=emoji,
        )

        # Return true
        return True

    # Return false on error
    except Exception:
        return False
