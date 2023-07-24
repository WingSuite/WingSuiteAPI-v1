# Flask Imports
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask import Flask

# Data Import
from database.base import DataAccessBase

# Endpoint Imports
from endpoints.authentication import (
    login,
    refresh,
    register,
    authorize,
    reject,
    signout,
)
from endpoints.user import (
    add_permissions,
    delete_permissions,
    who_am_i,
    everyone,
    get_user,
    get_feedbacks,
    get_events,
    get_notifications,
    get_pfa_data,
    get_warrior_data,
    get_users_units
)
from endpoints.unit import (
    create_unit,
    update_unit,
    update_frontpage,
    get_unit_info,
    get_all_units,
    get_all_officers,
    delete_unit,
    add_members,
    delete_members,
    add_officers,
    delete_officers,
    get_all_members,
    is_superior_officer
)
from endpoints.event import (
    create_event,
    update_event,
    get_event_info,
    delete_event,
)
from endpoints.notification import (
    create_notification,
    update_notification,
    get_notification_info,
    delete_notification,
)
from endpoints.statistics.feedback import (
    create_feedback,
    update_feedback,
    get_feedback_info,
    delete_feedback,
)
from endpoints.statistics.pfa import (
    create_pfa,
    update_pfa,
    delete_pfa,
    get_pfa_info,
    get_user_pfa_info
)
from endpoints.statistics.warrior import (
    create_warrior,
    update_warrior,
    get_warrior_info,
    delete_warrior,
)

# Miscellaneous Imports
from config.config import config
from datetime import timedelta

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
    hours=config.JWT.accessExpiry
)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(
    hours=config.JWT.refreshExpiry
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


"""
ROUTE HANDLING
"""

# Authentication routes
app.register_blueprint(login, url_prefix="/auth/")
app.register_blueprint(refresh, url_prefix="/auth/")
app.register_blueprint(register, url_prefix="/auth/")
app.register_blueprint(authorize, url_prefix="/auth/")
app.register_blueprint(reject, url_prefix="/auth/")
app.register_blueprint(signout, url_prefix="/auth/")

# User routes
app.register_blueprint(add_permissions, url_prefix="/user/")
app.register_blueprint(delete_permissions, url_prefix="/user/")
app.register_blueprint(who_am_i, url_prefix="/user/")
app.register_blueprint(everyone, url_prefix="/user/")
app.register_blueprint(get_user, url_prefix="/user/")
app.register_blueprint(get_feedbacks, url_prefix="/user/")
app.register_blueprint(get_events, url_prefix="/user/")
app.register_blueprint(get_notifications, url_prefix="/user/")
app.register_blueprint(get_pfa_data, url_prefix="/user/")
app.register_blueprint(get_warrior_data, url_prefix="/user/")
app.register_blueprint(get_users_units, url_prefix="/user/")

# Unit routes
app.register_blueprint(create_unit, url_prefix="/unit/")
app.register_blueprint(update_unit, url_prefix="/unit/")
app.register_blueprint(update_frontpage, url_prefix="/unit/")
app.register_blueprint(get_unit_info, url_prefix="/unit/")
app.register_blueprint(get_all_units, url_prefix="/unit/")
app.register_blueprint(get_all_officers, url_prefix="/unit/")
app.register_blueprint(get_all_members, url_prefix="/unit/")
app.register_blueprint(add_members, url_prefix="/unit/")
app.register_blueprint(add_officers, url_prefix="/unit/")
app.register_blueprint(delete_unit, url_prefix="/unit/")
app.register_blueprint(delete_members, url_prefix="/unit/")
app.register_blueprint(delete_officers, url_prefix="/unit/")
app.register_blueprint(is_superior_officer, url_prefix="/unit/")

# Event routes
app.register_blueprint(create_event, url_prefix="/event/")
app.register_blueprint(update_event, url_prefix="/event/")
app.register_blueprint(get_event_info, url_prefix="/event/")
app.register_blueprint(delete_event, url_prefix="/event/")

# Notification routes
app.register_blueprint(create_notification, url_prefix="/notification/")
app.register_blueprint(update_notification, url_prefix="/notification/")
app.register_blueprint(get_notification_info, url_prefix="/notification/")
app.register_blueprint(delete_notification, url_prefix="/notification/")

# Statistic Feedback routes
app.register_blueprint(create_feedback, url_prefix="/statistic/feedback/")
app.register_blueprint(update_feedback, url_prefix="/statistic/feedback/")
app.register_blueprint(get_feedback_info, url_prefix="/statistic/feedback/")
app.register_blueprint(delete_feedback, url_prefix="/statistic/feedback/")

# Statistic PFA routes
app.register_blueprint(create_pfa, url_prefix="/statistic/pfa/")
app.register_blueprint(update_pfa, url_prefix="/statistic/pfa/")
app.register_blueprint(get_pfa_info, url_prefix="/statistic/pfa/")
app.register_blueprint(delete_pfa, url_prefix="/statistic/pfa/")
app.register_blueprint(get_user_pfa_info, url_prefix="/statistic/pfa/")

# Statistic Warrior routes
app.register_blueprint(create_warrior, url_prefix="/statistic/warrior/")
app.register_blueprint(update_warrior, url_prefix="/statistic/warrior/")
app.register_blueprint(get_warrior_info, url_prefix="/statistic/warrior/")
app.register_blueprint(delete_warrior, url_prefix="/statistic/warrior/")

"""
APP RUNTIME HANDLING
"""

# Main run thread
if __name__ == "__main__":
    app.run()
