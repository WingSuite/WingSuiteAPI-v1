# Imports
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.user import UserAccess
from config.config import config
from functools import wraps
from flask import jsonify


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
            user_permissions = UserAccess.get_user(get_jwt_identity()["_id"])
            user_permissions = set(user_permissions["content"]["permissions"])

            # IF the user does not have sufficient permissions, deny the user
            if not user_permissions.intersection(required_permissions):
                return (
                    jsonify(
                        {
                            "status": "error",
                            "message": "You do not have access to this feature"
                        }
                    ),
                    403,
                )

            # If so, continue on with the function that is being decorated
            else:
                return fn(*args, **kwargs)

        # Return the functionality of the wrapper
        return wrapper

    # Return the functionality of the decorator
    return decorator
