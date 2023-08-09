# Import
from flask import Blueprint

# Blueprint initialization
send_email = Blueprint("send_email", __name__)
send_unit_discord_message = Blueprint("send_unit_discord_message", __name__)

# Import views
from . import views   # noqa