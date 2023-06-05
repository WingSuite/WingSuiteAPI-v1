# Import the test blueprint
from flask_jwt_extended import create_access_token, create_refresh_token
from endpoints.base import permissions_required
from database.users import UserAccess
from flask import jsonify, request
from models.user import User
from . import *

@login.route("/login/", methods=["POST"])
def login_endpoint():
    """Log In Handling"""
    
    # Try to parse information
    try:
        # Parse information from the call's body
        data = request.get_json()

        # Get the user's instance based on the given information
        response_data = UserAccess.login(**data)

        # If the response data results in an error, return 400 and error message
        if (response_data["status"] != "success"):
            return response_data, 400

        # Create refresh and access token
        identity = {
            "email": response_data["content"]["email"],
            "_id": response_data["content"]["_id"]
        }
        access_token = create_access_token(identity=identity)
        refresh_token = create_refresh_token(identity=identity)
        
        # Return response data except for the password
        return {"access_token": access_token, "refresh_token": refresh_token}, 200

    # Error handling
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@register.route("/register/", methods=["POST"])
def register_endpoint():
    """Log In Handling"""
    
    # Try to parse information
    try:
        # Parse information from the call's body
        data = request.get_json()

        # Get the user's instance based on the given information
        response_data = UserAccess.register_user(**data)

        # Return response data
        return response_data, (200 if response_data["status"] == "success" else 400)

    # Error handling
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@authorize.route("/authorize_user/", methods=["POST"])
@permissions_required(["user.authrize_user"])
def authorize_user_endpoint():
    """Log In Handling"""
    
    # Try to parse information
    try:
        # Parse information from the call's body
        data = request.get_json()

        # Get the user's instance based on the given information
        response_data = UserAccess.add_user(**data)

        # Return response data
        return response_data, (200 if response_data["status"] == "success" else 400)

    # Error handling
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@add_permission.route("/add_permission/", methods=["POST"])
@permissions_required(["user.add_permission"])
def add_permission_endpoint():
    """Method to handle the adding of new permissions to the user"""
    
    # Try to parse information
    try:
        # Parse information from the call's body
        data = request.get_json()

        # Add permission to the user's data
        response_data = UserAccess.change_permission("add", **data)

        # Return response data
        return response_data, (200 if response_data["status"] == "success" else 400)

    # Error handling
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@add_permission.route("/delete_permission/", methods=["POST"])
@permissions_required(["user.delete_permission"])
def delete_permission_endpoint():
    """Method to handle the adding of new permissions to the user"""
    
    # Try to parse information
    try:
        # Parse information from the call's body
        data = request.get_json()

        # Add permission to the user's data
        response_data = UserAccess.change_permission("delete", **data)

        # Return response data
        return response_data, (200 if response_data["status"] == "success" else 400)

    # Error handling
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@dashboard.route("/dashboard/")
def dashboard_endpoint():
    return User().info()

@signout.route("/signout/")
def signout_endpoint():
    return "Signout"