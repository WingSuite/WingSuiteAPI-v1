# Flask Imports
from flask_jwt_extended import (
    JWTManager, 
    jwt_required, 
    create_access_token, 
    get_jwt_identity, 
    create_refresh_token
)
from flask_cors import CORS
from flask import Flask

# Endpoint Imports
from endpoints.authentication import *

# Miscellaneous Imports
from config.config import config
from datetime import timedelta

# Make app instance
app = Flask(__name__)

# Set CORS for the application
CORS(app, methods=["POST", "GET"])

# Initialize JWT functionalities
app.config["JWT_SECRET_KEY"] = config.JWT.secret 
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=config.JWT.accessExpiry)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(hours=config.JWT.refreshExpiry)
jwt = JWTManager(app)

# Register all blueprints
app.register_blueprint(home, url_prefix="/home/")
app.register_blueprint(login, url_prefix="/user/")
app.register_blueprint(register, url_prefix="/user/")
app.register_blueprint(authorize, url_prefix="/user/")
app.register_blueprint(add_permission, url_prefix="/user/")
app.register_blueprint(delete_permission, url_prefix="/user/")
app.register_blueprint(dashboard, url_prefix="/user/")
app.register_blueprint(signout, url_prefix="/user/")

# Main run thread
if __name__ == "__main__":
    app.run()