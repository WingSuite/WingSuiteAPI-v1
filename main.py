# Flask Imports
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask import Flask

# Data Import
from database.base import DataAccessBase

# Endpoint Imports
from endpoints.authentication import (
    login,
    register,
    authorize,
    signout
)
from endpoints.user import (
    add_permissions,
    delete_permissions,
    who_am_i
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
    jti = jwt_payload["jti"]
    query = DataAccessBase.BLACKLIST_COL.find_one({"access_jti": jti})
    return query is not None


"""
ROUTE HANDLING
"""

# Authentication routes
app.register_blueprint(login, url_prefix="/auth/")
app.register_blueprint(register, url_prefix="/auth/")
app.register_blueprint(authorize, url_prefix="/auth/")
app.register_blueprint(signout, url_prefix="/auth/")

# User routes
app.register_blueprint(add_permissions, url_prefix="/user/")
app.register_blueprint(delete_permissions, url_prefix="/user/")
app.register_blueprint(who_am_i, url_prefix="/user/")

"""
APP RUNTIME HANDLING
"""

# Main run thread
if __name__ == "__main__":
    app.run()
