# Flask Imports
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask import Flask

# Data Import
from database.base import DataAccessBase

# Endpoint Imports
from endpoints.authentication import *
from endpoints.users import *

# Miscellaneous Imports
from config.config import config
from datetime import timedelta

import json

"""
FLASK APP CONFIGURATION
"""

# Make app instance
app = Flask(__name__)

# Set CORS for the application
CORS(app, methods=["POST", "GET"])

# Initialize JWT functionalities
app.config["JWT_SECRET_KEY"] = config.JWT.secret 
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=config.JWT.accessExpiry)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(hours=config.JWT.refreshExpiry)
jwt = JWTManager(app)

# Define the blacklist checker for JWT
@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
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
app.register_blueprint(add_permission, url_prefix="/user/")
app.register_blueprint(delete_permission, url_prefix="/user/")

"""
APP RUNTIME HANDLING
"""

# Main run thread
if __name__ == "__main__":
    app.run()