# Imports
from flask_jwt_extended import decode_token
from config.config import permissions
from .base import DataAccessBase
from utils.hash import sha256
from models.user import User
import uuid


class UserAccess(DataAccessBase):
    """Class that handles user information"""

    # Store the required arguments for this class
    ARGS = DataAccessBase.REQ_ARGS.users

    @staticmethod
    @DataAccessBase.dict_wrap
    def get_user(secure=False, obj=False, **kwargs):
        """Base method for get_user methods"""

        # Get the results from the query
        user_data = DataAccessBase.USER_COL.find_one(kwargs)

        # Return if the given user is not in the database
        if user_data is None:
            return {
                "status": "error",
                "message": "Check your inputted credentials",
            }

        # Get the content of the user based on wether
        # we want to get all or some data
        content = (
            User(**user_data).info
            if not secure
            else User(**user_data).get_generic_info(
                includeFullName=True, lastNameFirst=True
            )
        )

        # Return results based on types of representation
        return {
            "status": "success",
            "content": content if not obj else User(**user_data),
        }

    @staticmethod
    @DataAccessBase.dict_wrap
    @DataAccessBase.param_check(ARGS.set_user)
    def set_user(**kwargs):
        """Update the specified user's information"""
        DataAccessBase.USER_COL.update_one(
            {"_id": kwargs["_id"]}, {"$set": kwargs["value"]}
        )
        return {}

    @staticmethod
    @DataAccessBase.dict_wrap
    @DataAccessBase.param_check(ARGS.login)
    def login(**kwargs):
        """
        Method that returns the user object based
        on the given user and pass
        """

        # Hash and save the given password to kwargs
        kwargs["password"] = sha256(
            kwargs["password"], DataAccessBase.CONFIG.database.spicer
        )

        # Return user content
        return UserAccess.get_user(secure=True, **kwargs)

    @staticmethod
    @DataAccessBase.dict_wrap
    @DataAccessBase.param_check(ARGS.add_user)
    def add_user(**kwargs):
        """Method that handles adding a user to the system"""

        # Add user to the list and return success if the given
        # information is not the system
        user = DataAccessBase.REGISTER_COL.find_one({"_id": kwargs["_id"]})
        if user is not None:
            # Insert user into the database, remove from REGISTER_COL and
            # return success
            DataAccessBase.USER_COL.insert_one(user)
            DataAccessBase.REGISTER_COL.delete_one({"_id": kwargs["_id"]})
            return {"status": "success", "message": "User added to the system"}
        # Return false if the given information exists
        else:
            return {"status": "error", "message": "User did not register"}

    @staticmethod
    @DataAccessBase.dict_wrap
    @DataAccessBase.param_check(ARGS.register_user)
    def register_user(**kwargs):
        """Method that handles registering a user to the system"""

        # Add user to the list and return success if the given
        # information is not the system
        if (
            DataAccessBase.USER_COL.find_one({"email": kwargs["email"]})
            is None
            and DataAccessBase.REGISTER_COL.find_one(
                {"email": kwargs["email"]}
            )
            is None
        ):
            # Prep data to be inserted
            kwargs["_id"] = uuid.uuid4().hex
            kwargs["permissions"] = []

            # Hash and save the given password
            kwargs["password"] = sha256(
                kwargs["password"], DataAccessBase.CONFIG.database.spicer
            )

            # Insert user into the database and return success
            DataAccessBase.REGISTER_COL.insert_one(kwargs)
            return {
                "status": "success",
                "message": "User is up for authorization",
            }
        # Return false if the given information exists
        else:
            return {
                "status": "error",
                "message": "User has registered or is authorized",
            }

    @staticmethod
    @DataAccessBase.dict_wrap
    @DataAccessBase.param_check(ARGS.change_permissions)
    def change_permissions(operation, **kwargs):
        """Add permissions values based on the given id"""

        # Check if the permissions value is a list
        if not isinstance(kwargs["permissions"], list):
            return {
                "status": "error",
                "message": "Permissions value not in list format",
            }

        # Check if the operation value is one of the accepted options
        if operation not in ["add", "delete"]:
            return {
                "status": "error",
                "message": "Operation value is not an accepted value",
            }

        # Get user object
        user = UserAccess.get_user(obj=True, _id=kwargs["_id"])

        # If content is not in result of getting the user, return the
        # error message
        if "content" not in user:
            return user

        # Get the content from the user fetch
        user = user.content

        # Add new permission(s) and track changes
        results = {}
        for permission in kwargs["permissions"]:
            # If the given permission is not part of the approved list of
            # permission track that is is not added with an explanation and
            # continue
            if permission not in permissions:
                results[permission] = "Not Added (Invalid Permission)"
                continue

            # Attempt add permission
            res = (
                user.add_permission(permission)
                if operation == "add"
                else user.delete_permission(permission)
            )

            # Track changes
            results[permission] = (
                ("Added" if operation == "add" else "Deleted")
                if res
                else "Not Added (Already "
                + (
                    "Added)"
                    if operation == "add"
                    else "Deleted or is Missing)"
                )
            )

        # Update database
        DataAccessBase.USER_COL.update_one(
            {"_id": user.info["_id"]},
            {"$set": {"permissions": user.info["permissions"]}},
        )

        # Return success message
        operation_type = "addition" if operation == "add" else "deletion"
        return {
            "status": "success",
            "message": f"Permission {operation_type} have been applied to"
            + f"{user.get_fullname(lastNameFirst=True)}. Refer to results"
            + "for what has been applied",
            "results": results,
        }

    @staticmethod
    @DataAccessBase.dict_wrap
    @DataAccessBase.param_check(ARGS.handle_jwt_blacklisting)
    def handle_jwt_blacklisting(**kwargs):
        """Handles the blacklisting of JWT tokens"""

        # Get the JTI from the tokens
        refresh_jti = decode_token(kwargs["refresh"])["jti"]
        access_jti = decode_token(kwargs["access"])["jti"]

        # Place tokens to blacklist collection
        DataAccessBase.BLACKLIST_COL.insert_one(
            {
                "refresh": kwargs["refresh"],
                "access": kwargs["access"],
                "refresh_jti": refresh_jti,
                "access_jti": access_jti,
            }
        )

        # Return message
        return {"status": "success", "message": "Signed Out"}
