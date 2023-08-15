# Import
from flask import Blueprint

# Blueprint initialization
send_user_email_message = Blueprint("send_user_email_message", __name__)
send_unit_discord_message = Blueprint("send_unit_discord_message", __name__)

# Import views
from . import views   # noqa