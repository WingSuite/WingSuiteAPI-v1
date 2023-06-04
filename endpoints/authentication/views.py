# Import the test blueprint
from database.users import UserAccess
from flask import jsonify, request
from models.user import User
from . import *

@login.route('/login/', methods=['POST'])
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
        
        # Return response data except for the password
        return response_data, 200

    # Error handling
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@register.route('/register/', methods=['POST'])
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
        return jsonify({'error': str(e)}), 500

@authorize.route('/authorize_user/', methods=['POST'])
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
        return jsonify({'error': str(e)}), 500

@dashboard.route('/dashboard/')
def dashboard_endpoint():
    return User().info()

@signout.route('/signout/')
def signout_endpoint():
    return "Signout"