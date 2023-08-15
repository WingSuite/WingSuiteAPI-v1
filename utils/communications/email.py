# Imports
from utils.dict_parse import DictParse
from utils.html import read_html_file
from database.unit import UnitAccess
from database.user import UserAccess
from email.message import EmailMessage
from config.config import config
from typing import Any
import smtplib

# Boot up connection
SERVER = smtplib.SMTP_SSL(config.email.smtp_server, config.email.smtp_port)
SERVER.login(config.email.sender_email, config.email.password)


def send_email(
    receiver: str, subject: str, content: str, emoji: str = "🔔"
) -> bool:
    """Helper function to send an email to a user"""

    # Try
    try:
        # Create the message
        emoji = emoji + " " if emoji else ""
        message = EmailMessage()
        message["Subject"] = "NOTIFICATION // " + subject
        message["From"] = (
            f"{emoji}‎ WingSuite" + f" <{config.email.sender_email}>"
        )
        message["To"] = receiver
        message.set_content(content)

        # Add the HTML content as an alternative to plain text content
        message.add_alternative(content, subtype="html")

        # Send message
        SERVER.send_message(message)

        # Return true
        return True

    # Return false on error
    except Exception:
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
        personnel = [
            DictParse(
                {
                    "email": i.email,
                    "full_name": (
                        i.rank + " " + i.full_name
                        if "rank" in i
                        else i.first_name
                    ),
                }
            )
            for i in personnel
        ]

        # Iterate through the email list and send the emails
        for i in personnel:
            # Add to msg_content
            msg_content["to_user"] = i.full_name

            # Get feedback HTML content
            content = read_html_file(**msg_content)

            # Send an email with the HTML content
            send_email(
                receiver=i.email,
                subject=subject,
                content=content,
                emoji=emoji,
            )

        # Return true
        return True

    # Return false on error
    except Exception:
        return False
