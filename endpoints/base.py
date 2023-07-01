# Imports
from flask_jwt_extended import jwt_required, get_jwt_identity
from config.config import config, arguments
from database.user import UserAccess
from typing import List, Any
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


def permissions_required(required_permissions: List[str]) -> object:
    """Function to decorate endpoints with needed permissions"""

    # Modify required_permission so that the root permission key is included
    required_permissions.insert(0, config.rootPermissionString)

    def decorator(func: object) -> object:
        """Decorator definition for this functionality"""

        @wraps(func)
        @jwt_required()
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """Wrapper that checks if the user has the correct permissions"""

            # Get user's permissions based on the user's given ID
            id = get_jwt_identity()["_id"]
            user = UserAccess.get_user(id)
            user_permissions = set(user.message.info.permissions)

            # IF the user does not have sufficient permissions, deny the user
            if not user_permissions.intersection(required_permissions):
                return clientErrorResponse(
                    "You do not have access to this feature"
                )

            # If so, continue on with the function that is being decorated
            else:
                # Check if the user has root key
                root = config.rootPermissionString in user_permissions

                # Return the function with information provided
                return func(*args, **kwargs, isRoot=root, id=id)

        # Return the functionality of the wrapper
        return wrapper

    # Return the functionality of the decorator
    return decorator


def param_check(required_params: List[str]) -> object:
    """Method that checks for minimum parameters"""

    def decorator(func: object) -> object:
        """Decorator definition"""

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """Wrapping definition"""

            # Get the JSON body
            data = request.get_json()

            # Return error if the body was empty
            if data is None:
                return clientErrorResponse("JSON body is empty")

            # Check if the given arguments has the minimum arguments
            for arg in required_params:
                if arg not in data.keys():
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
