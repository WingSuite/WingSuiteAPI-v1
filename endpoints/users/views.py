# Import the test blueprint
from . import add_permissions, delete_permissions, who_am_i
from flask_jwt_extended import jwt_required, decode_token
from endpoints.base import permissions_required
from database.user import UserAccess
from flask import jsonify, request


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
        return result, (200 if result.status == "success" else 400)

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
        return result, (200 if result.status == "success" else 400)

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
        token = request.headers.get("Authorization", None).split()[1]

        # Decode the JWT Token and get the ID of the user
        id = decode_token(token)["sub"]["_id"]

        # Get the user based on the ID
        result = UserAccess.get_user(secure=True, _id=id)

        # Return the results of the database query
        return result, (200 if result.status == "success" else 400)

    # Error handling
    except Exception as e:
        return jsonify({"error": str(e)}), 500
