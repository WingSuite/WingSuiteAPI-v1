# Imports
from email.message import EmailMessage
from config.config import config
import smtplib

# Boot up connection
SERVER = smtplib.SMTP_SSL(config.email.smtp_server, config.email.smtp_port)
SERVER.login(config.email.sender_email, config.email.password)


def send_email(receiver: str, subject: str, content: str) -> bool:
    """Helper function to send an email to a user"""

    # Try
    try:
        # Create the message
        message = EmailMessage()
        message["Subject"] = subject
        message[
            "From"
        ] = f"WingSuite Messaging System <{config.email.sender_email}>"
        message["To"] = receiver
        message.set_content(content)

        # Send message
        SERVER.send_message(message)

        # Return true
        return True

    # Return false on error
    except Exception:
        return False
