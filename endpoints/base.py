# Imports
from flask_jwt_extended import jwt_required, get_jwt_identity
from config.config import config, arguments
from database.user import UserAccess
from functools import wraps
from flask import request


def successResponse(message: str) -> dict:
    """Returns a message with a success status"""
    return {"status": "success", "message": message}, 200


def clientErrorResponse(message: str) -> dict:
    """Returns a message with a client error status"""
    return {"status": "error", "message": message}, 400


def serverErrorResponse(message: str) -> dict:
    """Returns a message with a server error status"""
    return {"status": "error", "message": message}, 500


def permissions_required(required_permissions):
    """Function to decorate endpoints with needed permissions"""

    # Modify required_permission so that the root permission key is included
    required_permissions.insert(0, config.rootPermissionString)

    def decorator(fn):
        """Decorator definition for this functionality"""

        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            """Wrapper that checks if the user has the correct permissions"""

            # Get user's permissions based on the user's given ID
            id = get_jwt_identity()["_id"]
            user = UserAccess.get_user(id)
            user_permissions = set(user.message.info.permissions)

            # IF the user does not have sufficient permissions, deny the user
            if not user_permissions.intersection(required_permissions):
                clientErrorResponse("You do not have access to this feature")

            # If so, continue on with the function that is being decorated
            else:
                return fn(*args, **kwargs)

        # Return the functionality of the wrapper
        return wrapper

    # Return the functionality of the decorator
    return decorator


def param_check(required_params):
    """Method that checks for minimum parameters"""

    def decorator(func):
        """Decorator definition"""

        @wraps(func)
        def wrapper(*args, **kwargs):
            """Wrapping definition"""

            # Get the JSON body
            data = request.get_json()

            # Return error if the body was empty
            if data is None:
                return clientErrorResponse("JSON body is empty")

            # Check if the given arguments has the minimum arguments
            for arg in data.keys():
                if arg not in required_params:
                    return clientErrorResponse(
                        "Call needs the following arguments: "
                        + ", ".join(required_params)
                    )

            # Return normally if all else is good
            return func(*args, **kwargs)

        # End of wrapper definition
        return wrapper

    # End of decorator definition
    return decorator


# Export an arguments config variable
ARGS = arguments.endpoints
