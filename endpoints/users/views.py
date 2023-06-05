# Import the test blueprint
from flask_jwt_extended import jwt_required, decode_token
from endpoints.base import permissions_required
from database.users import UserAccess
from flask import jsonify, request
from models.user import User
from . import *
import json


@add_permissions.route("/add_permissions/", methods=["POST"])
@permissions_required(["user.add_permissions"])
def add_permissions_endpoint():
    """Method to handle the adding of new permissions to the user"""
    
    # Try to parse information
    try:
        # Parse information from the call's body
        data = request.get_json()

        # Add permission to the user's data
        result = UserAccess.change_permissions("add", **data)

        # Return response data
        return result, (200 if result["status"] == "success" else 400)

    # Error handling
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@delete_permissions.route("/delete_permissions/", methods=["POST"])
@permissions_required(["user.delete_permissions"])
def delete_permissions_endpoint():
    """Method to handle the adding of new permissions to the user"""
    
    # Try to parse information
    try:
        # Parse information from the call's body
        data = request.get_json()

        # Add permission to the user's data
        result = UserAccess.change_permissions("delete", **data)

        # Return response data
        return result, (200 if result["status"] == "success" else 400)

    # Error handling
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@who_am_i.route("/who_am_i/", methods=["GET"])
@jwt_required()
def who_am_i():
    """Method to return the user's information"""
    
    # Try to parse information
    try:
        # Get the access token
        token = request.headers.get('Authorization', None).split()[1]
        
        # Decode the JWT Token and get the ID of the user
        id = decode_token(token)["sub"]["_id"]
        
        # Get the user based on the ID
        result = UserAccess.get_user(secure=True, _id=id)
        
        return result, (200 if result["status"] == "success" else 400)

    # Error handling
    except Exception as e:
        return jsonify({"error": str(e)}), 500