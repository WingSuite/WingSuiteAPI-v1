# Imports
from email.message import EmailMessage
from config.config import config
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
