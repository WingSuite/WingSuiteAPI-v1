# Flask Imports
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask import Flask

# Data Import
from database.base import DataAccessBase

# Endpoint Imports
from endpoints.authentication import (
    register,
    login,
    get_register_requests,
    refresh,
    authorize,
    signout,
    reject,
    kick_user,
)
from endpoints.communications import (
    send_user_email_message,
    send_unit_discord_message,
)
from endpoints.user import (
    add_permissions,
    who_am_i,
    everyone,
    get_user,
    get_feedbacks,
    get_events,
    get_notifications,
    get_pfa_data,
    get_warrior_data,
    get_users_units,
    get_permissions_list,
    update_permissions,
    update_rank,
    delete_permissions,
)
from endpoints.unit import (
    create_unit,
    add_members,
    add_officers,
    update_unit,
    update_frontpage,
    get_unit_info,
    get_unit_types,
    get_all_units,
    get_all_officers,
    get_all_members,
    is_superior_officer,
    get_all_five_point_data,
    get_all_pfa_data,
    get_all_warrior_data,
    delete_unit,
    delete_members,
    delete_officers,
)
from endpoints.event.views import event_dispatch
from endpoints.event import (
    create_event,
    get_event_info,
    update_event,
    delete_event,
)
from endpoints.notification import (
    create_notification,
    get_notification_info,
    update_notification,
    delete_notification,
)
from endpoints.statistic.feedback import (
    create_feedback,
    get_feedback_info,
    update_feedback,
    delete_feedback,
)
from endpoints.statistic.five_point import (
    create_five_point,
    get_five_point_info,
    get_user_five_point_info,
    get_five_point_format_info,
    get_test_five_point_score,
    update_five_point,
    delete_five_point,
)
from endpoints.statistic.pfa import (
    create_pfa,
    get_pfa_info,
    get_user_pfa_info,
    get_pfa_format_info,
    get_test_pfa_score,
    update_pfa,
    delete_pfa,
)
from endpoints.statistic.warrior import (
    create_warrior,
    get_warrior_info,
    get_user_warrior_info,
    get_warrior_format_info,
    get_test_warrior_score,
    update_warrior,
    delete_warrior,
)

# Scheduler Imports
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

# Miscellaneous Imports
from config.config import config
from datetime import timedelta
import atexit
import os

"""
FLASK APP CONFIGURATION
"""

# Make app instance
app = Flask(__name__)

# Set CORS for the application
CORS(app, methods=["POST", "GET"])

# Initialize JWT functionalities
app.config["JWT_SECRET_KEY"] = config.JWT.secret
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(
    hours=config.JWT.access_expiry
)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(
    hours=config.JWT.refresh_expiry
)
jwt = JWTManager(app)


# Define the blacklist checker for JWT
@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    """Function to test if the user's token is blacklisted"""

    # Get the JWT token information
    jti = jwt_payload["jti"]

    # Check if the token is blacklisted
    query = DataAccessBase.BLACKLIST_COL.find_one({"access_jti": jti})

    # Return true if it is, false if not
    return query is not None


# Customize expired token message
@jwt.expired_token_loader
def my_expired_token_callback(*kwargs):
    """Function to customize the expired token message"""

    # Return a custom error message
    return {
        "status": "expired",
        "message": "Your access is expired",
    }, 401


# Dry landing page
@app.route("/")
def home():
    """Dry landing page"""
    return """<!doctype html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <title>DET 025 API</title>
    </head>
    <body>
        <h1 style="font-size: 50px; text-align: center;">
            Detachment 025 WingSuite API Server
        </h1>
        <p style="text-align: center;">
            For any issues, please contact Benjamin Herrera via email at
            b10@asu.edu
        </p>
    </body>
    </html>"""


"""
ROUTE HANDLING
"""

# Authentication routes
# region
app.register_blueprint(register, url_prefix="/auth/")
app.register_blueprint(login, url_prefix="/auth/")
app.register_blueprint(get_register_requests, url_prefix="/auth/")
app.register_blueprint(refresh, url_prefix="/auth/")
app.register_blueprint(authorize, url_prefix="/auth/")
app.register_blueprint(signout, url_prefix="/auth/")
app.register_blueprint(reject, url_prefix="/auth/")
app.register_blueprint(kick_user, url_prefix="/auth/")
# endregion

# Communication routes
# region
app.register_blueprint(send_user_email_message, url_prefix="/communications/")
app.register_blueprint(
    send_unit_discord_message, url_prefix="/communications/"
)
# endregion

# User routes
# region
app.register_blueprint(add_permissions, url_prefix="/user/")
app.register_blueprint(who_am_i, url_prefix="/user/")
app.register_blueprint(everyone, url_prefix="/user/")
app.register_blueprint(get_user, url_prefix="/user/")
app.register_blueprint(get_feedbacks, url_prefix="/user/")
app.register_blueprint(get_events, url_prefix="/user/")
app.register_blueprint(get_notifications, url_prefix="/user/")
app.register_blueprint(get_pfa_data, url_prefix="/user/")
app.register_blueprint(get_warrior_data, url_prefix="/user/")
app.register_blueprint(get_users_units, url_prefix="/user/")
app.register_blueprint(get_permissions_list, url_prefix="/user/")
app.register_blueprint(update_permissions, url_prefix="/user/")
app.register_blueprint(update_rank, url_prefix="/user/")
app.register_blueprint(delete_permissions, url_prefix="/user/")
# endregion

# Unit routes
# region
app.register_blueprint(create_unit, url_prefix="/unit/")
app.register_blueprint(add_members, url_prefix="/unit/")
app.register_blueprint(add_officers, url_prefix="/unit/")
app.register_blueprint(get_unit_info, url_prefix="/unit/")
app.register_blueprint(get_unit_types, url_prefix="/unit/")
app.register_blueprint(get_all_units, url_prefix="/unit/")
app.register_blueprint(get_all_officers, url_prefix="/unit/")
app.register_blueprint(get_all_members, url_prefix="/unit/")
app.register_blueprint(is_superior_officer, url_prefix="/unit/")
app.register_blueprint(get_all_five_point_data, url_prefix="/unit/")
app.register_blueprint(get_all_pfa_data, url_prefix="/unit/")
app.register_blueprint(get_all_warrior_data, url_prefix="/unit/")
app.register_blueprint(update_unit, url_prefix="/unit/")
app.register_blueprint(update_frontpage, url_prefix="/unit/")
app.register_blueprint(delete_unit, url_prefix="/unit/")
app.register_blueprint(delete_members, url_prefix="/unit/")
app.register_blueprint(delete_officers, url_prefix="/unit/")
# endregion

# Event routes
# region
app.register_blueprint(create_event, url_prefix="/event/")
app.register_blueprint(get_event_info, url_prefix="/event/")
app.register_blueprint(update_event, url_prefix="/event/")
app.register_blueprint(delete_event, url_prefix="/event/")
# endregion

# Notification routes
# region
app.register_blueprint(create_notification, url_prefix="/notification/")
app.register_blueprint(get_notification_info, url_prefix="/notification/")
app.register_blueprint(update_notification, url_prefix="/notification/")
app.register_blueprint(delete_notification, url_prefix="/notification/")
# endregion

# Statistic Feedback routes
# region
app.register_blueprint(create_feedback, url_prefix="/statistic/feedback/")
app.register_blueprint(get_feedback_info, url_prefix="/statistic/feedback/")
app.register_blueprint(update_feedback, url_prefix="/statistic/feedback/")
app.register_blueprint(delete_feedback, url_prefix="/statistic/feedback/")
# endregion

# Statistic Five Point Evaluation routes
# region
app.register_blueprint(create_five_point, url_prefix="/statistic/five_point/")
app.register_blueprint(
    get_five_point_info, url_prefix="/statistic/five_point/"
)
app.register_blueprint(
    get_user_five_point_info, url_prefix="/statistic/five_point/"
)
app.register_blueprint(
    get_five_point_format_info, url_prefix="/statistic/five_point/"
)
app.register_blueprint(
    get_test_five_point_score, url_prefix="/statistic/five_point/"
)
app.register_blueprint(update_five_point, url_prefix="/statistic/five_point/")
app.register_blueprint(delete_five_point, url_prefix="/statistic/five_point/")
# endregion

# Statistic PFA routes
# region
app.register_blueprint(create_pfa, url_prefix="/statistic/pfa/")
app.register_blueprint(get_pfa_info, url_prefix="/statistic/pfa/")
app.register_blueprint(get_user_pfa_info, url_prefix="/statistic/pfa/")
app.register_blueprint(get_pfa_format_info, url_prefix="/statistic/pfa/")
app.register_blueprint(get_test_pfa_score, url_prefix="/statistic/pfa/")
app.register_blueprint(update_pfa, url_prefix="/statistic/pfa/")
app.register_blueprint(delete_pfa, url_prefix="/statistic/pfa/")
# endregion

# Statistic Warrior routes
# region
app.register_blueprint(create_warrior, url_prefix="/statistic/warrior/")
app.register_blueprint(get_warrior_info, url_prefix="/statistic/warrior/")
app.register_blueprint(get_user_warrior_info, url_prefix="/statistic/warrior/")
app.register_blueprint(
    get_warrior_format_info, url_prefix="/statistic/warrior/"
)
app.register_blueprint(
    get_test_warrior_score, url_prefix="/statistic/warrior/"
)
app.register_blueprint(update_warrior, url_prefix="/statistic/warrior/")
app.register_blueprint(delete_warrior, url_prefix="/statistic/warrior/")
# endregion

"""
APP RUNTIME HANDLING
"""

# Scheduler functionalities
if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    # Initialize scheduler functionalities
    print("Starting background scheduler...")
    scheduler = BackgroundScheduler()
    scheduler.start()

    # Schedule the event update function to run every minute
    trigger = IntervalTrigger(minutes=1)
    scheduler.add_job(
        func=event_dispatch,
        trigger=trigger,
        id="check_events_job",
        replace_existing=True,
    )

    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())
    print("Background scheduler created!") 

# Main run thread
if __name__ == "__main__":
    # Import waitress
    from waitress import serve

    # Check if the server is in development mode
    mode_type = int(os.environ.get("RUN_MODE"))
    if mode_type == 0:
        print("Running API Server in DEVELOPMENT MODE")
        app.run(host="0.0.0.0", port=5000)
    # Check if the server is in production mode
    elif mode_type == 1:
        print("Running API Server in PRODUCTION MODE")
        serve(app, host="0.0.0.0", port=5000)
    # If the mode value was not provided, exit with a message
    else:
        print("Invalid mode specification. Exiting...")
        exit()
