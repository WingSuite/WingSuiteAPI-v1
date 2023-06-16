# Imports
from flask_jwt_extended import decode_token
from utils.dict_parse import DictParse
from .base import DataAccessBase
from typing import Union, Any
from utils.hash import sha256
from models.user import User
import uuid


class UserAccess(DataAccessBase):
    """Class that handles user information"""

    @staticmethod
    @DataAccessBase.dict_wrap
    def register_user(
        first_name: str,
        last_name: str,
        email: str,
        phone_number: str,
        password: str,
        **kwargs: Any
    ) -> DictParse:
        """Method that handles registering a user to the system"""

        # Add user to the list and return success if the given
        # information is not the system
        query = {"email": email}
        if (
            DataAccessBase.USER_COL.find_one(query) is None
            and DataAccessBase.REGISTER_COL.find_one(query) is None
        ):
            # Prep data to be inserted
            data = {
                k: v
                for k, v in locals().items()
                if k not in ["kwargs", "args"]
            }
            data.update(locals()["kwargs"])
            data["_id"] = uuid.uuid4().hex
            data["permissions"] = []

            # Hash and save the given password
            password = sha256(password, DataAccessBase.CONFIG.database.spicer)
            data["password"] = password

            # Insert user into the database and return success
            DataAccessBase.REGISTER_COL.insert_one(data)
            return DataAccessBase.sendSuccess("User is up for authorization")

        # Return false if the given information exists
        else:
            return DataAccessBase.sendError(
                "User has registered or is authorized"
            )

    @staticmethod
    @DataAccessBase.dict_wrap
    def add_user(id: str) -> DictParse:
        """Method that handles adding a user to the system"""

        # Add user to the list and return success if the given
        # information is not the system
        user = DataAccessBase.REGISTER_COL.find_one({"_id": id})
        if user is not None:
            # Insert user into the database, remove from REGISTER_COL and
            # return success
            DataAccessBase.USER_COL.insert_one(user)
            DataAccessBase.REGISTER_COL.delete_one({"_id": id})
            return DataAccessBase.sendSuccess("User added to system")
        # Return false if the given information exists
        else:
            return DataAccessBase.sendError("User did not register")

    @staticmethod
    @DataAccessBase.dict_wrap
    def update_user(id: str, **kwargs: Any) -> DictParse:
        """Update the specified user's information"""

        # Delete the id in the kwargs
        del kwargs["_id"]

        # Check if the unit based on its id does exist
        if DataAccessBase.USER_COL.find_one({"_id": id}) is None:
            return DataAccessBase.sendError("User does not exist")

        # Update the document and return a success message
        DataAccessBase.USER_COL.update_one({"_id": id}, {"$set": kwargs})
        return DataAccessBase.sendSuccess("User updated")

    @staticmethod
    @DataAccessBase.dict_wrap
    def get_user(id: str) -> DictParse:
        """Base method for get_user methods"""

        # Get the results from the query
        user = DataAccessBase.USER_COL.find_one({"_id": id})

        # Return if the given user is not in the database
        if user is None:
            return DataAccessBase.sendError("User not found")

        # Return results based on types of representation
        return DataAccessBase.sendSuccess(User(**user))

    @staticmethod
    @DataAccessBase.dict_wrap
    def login(email: str, password: str) -> Union[User, DictParse]:
        """
        Method that returns the user object based
        on the given user and pass
        """

        # Hash and save the given password to kwargs
        password = sha256(password, DataAccessBase.CONFIG.database.spicer)

        # Get the user's ID based on the given credentials
        query = {"email": email, "password": password}
        id = DataAccessBase.USER_COL.find_one(query)["_id"]

        # Return with an error if no id was found
        if id is None:
            return DataAccessBase.sendError("Incorrect email or password")

        # Return user content
        return UserAccess.get_user(id)

    @staticmethod
    @DataAccessBase.dict_wrap
    def handle_jwt_blacklisting(refresh: str, access: str) -> DictParse:
        """Handles the blacklisting of JWT tokens"""

        # Get the JTI from the tokens
        refresh_jti = decode_token(refresh)["jti"]
        access_jti = decode_token(access)["jti"]

        # Place tokens to blacklist collection
        DataAccessBase.BLACKLIST_COL.insert_one(
            {
                "refresh": refresh,
                "access": access,
                "refresh_jti": refresh_jti,
                "access_jti": access_jti,
            }
        )

        # Return message
        return DataAccessBase.sendSuccess("Signed Out")
