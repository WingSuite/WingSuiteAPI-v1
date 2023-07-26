# Imports
from flask_jwt_extended import jwt_required, get_jwt_identity
from config.config import config, arguments
from database.user import UserAccess
from typing import List, Any
from functools import wraps
from flask import request
import traceback


def success_response(message: str, **kwargs: Any) -> dict:
    """Returns a message with a success status"""

    # Prep the message
    message = {"status": "success", "message": message}
    message.update(kwargs)

    # Return response
    return message, 200


def client_error_response(message: str, **kwargs: Any) -> dict:
    """Returns a message with a client error status"""

    # Prep the message
    message = {"status": "error", "message": message}
    message.update(kwargs)

    # Return response
    return message, 400


def server_error_response(message: str, **kwargs: Any) -> dict:
    """Returns a message with a server error status"""
    # Prep the message
    message = {"status": "error", "message": message}
    message.update(kwargs)

    # Return response
    return message, 500


def is_root(func: object) -> object:
    """Wrapper to determine if the user is an admin"""

    @wraps(func)
    @jwt_required()
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        """Wrapper that checks if the user has the correct permissions"""

        # Get user's permissions based on the user's given ID
        id = get_jwt_identity()["_id"]
        user = UserAccess.get_user(id)
        user_permissions = set(user.message.info.permissions)

        # Check if the user has root key
        root = config.rootPermissionString in user_permissions

        # Return the function with information provided
        return func(*args, **kwargs, isRoot=root, id=id)

    # Return the functionality of the wrapper
    return wrapper


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
                return client_error_response(
                    "You don't have access to this feature"
                )

            # If so, continue on with the function that is being decorated
            else:
                # Return the function with information provided
                return func(*args, **kwargs)

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
                return client_error_response("JSON body is empty")

            # Check if the given arguments has the minimum arguments
            for arg in required_params:
                if arg not in data.keys():
                    return client_error_response(
                        "Call needs the following arguments: "
                        + ", ".join(required_params)
                    )

            # Return normally if all else is good
            return func(*args, **kwargs)

        # End of wrapper definition
        return wrapper

    # End of decorator definition
    return decorator


def error_handler(func: object) -> object:
    """Decorator to handle errors inside function endpoints"""

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        """Wrapping definition"""

        # Try to execute the function
        try:
            return func(*args, **kwargs)

        # If the exception occurs, print the error to the console and
        # return a server error response
        except Exception:
            print(f"Caught an exception in {func.__name__}():")
            traceback.print_exc()
            return server_error_response("A server error occurred")

    # Return the wrapper
    return wrapper


# Export an arguments config variable
ARGS = arguments.endpoints
