# Import the test blueprint
from flask_jwt_extended import create_access_token, create_refresh_token
from endpoints.base import permissions_required
from database.users import UserAccess
from flask import jsonify, request
from models.user import User
from . import *


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