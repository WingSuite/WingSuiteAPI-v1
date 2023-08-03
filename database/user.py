# Imports
from flask_jwt_extended import decode_token
from utils.dict_parse import DictParse
from .base import DataAccessBase
from typing import Union, Any
from utils.hash import sha256
from models.user import User
import uuid
import math


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
            data["units"] = []
            del data["query"]

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
    def login(email: str, password: str) -> Union[User, DictParse]:
        """
        Method that returns the user object based
        on the given user and pass
        """

        # Hash and save the given password to kwargs
        password = sha256(password, DataAccessBase.CONFIG.database.spicer)

        # Get the user's information based on the given credentials
        query = {"email": email, "password": password}
        user = DataAccessBase.USER_COL.find_one(query)

        # Return with an error if no id was found
        if user is None:
            return DataAccessBase.sendError("Incorrect email or password")

        # Get the user's id
        id = user["_id"]

        # Return user content
        return UserAccess.get_user(id)

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
    def get_users(page_size: int, page_index: int) -> DictParse:
        """Get a list of users based on the page size and the index"""

        # Check if the page_size or page_index is negative
        if page_size <= 0 or page_index < 0:
            return DataAccessBase.sendError("Invalid pagination size or index")

        # Get the total amount of pages based on pagination size
        pages = math.ceil(
            DataAccessBase.USER_COL.count_documents({}) / page_size
        )

        # Check if the page_index is outside the page range
        if page_index >= pages:
            return DataAccessBase.sendError("Pagination index out of bounds")

        # Calculate skip value
        skips = page_size * (page_index)

        # Get the list of users based on the given page size and index
        results = DataAccessBase.USER_COL.find().skip(skips).limit(page_size)

        # Turn each document into a Unit object
        results = [User(**item) for item in list(results)]

        # Return the results and the page size
        return DataAccessBase.sendSuccess(results, pages=pages)

    @staticmethod
    @DataAccessBase.dict_wrap
    def get_register_list() -> DictParse:
        """Return a list of people requesting for organization access"""

        # Get the list of users
        results = DataAccessBase.REGISTER_COL.find({})

        # Return the results
        return DataAccessBase.sendSuccess(list(results))

    @staticmethod
    @DataAccessBase.dict_wrap
    def update_user(id: str, **kwargs: Any) -> DictParse:
        """Update the specified user's information"""

        # Delete the id in the kwargs
        if "_id" in kwargs:
            del kwargs["_id"]
        if "id" in kwargs:
            del kwargs["id"]

        # Check if the unit based on its id does exist
        if DataAccessBase.USER_COL.find_one({"_id": id}) is None:
            return DataAccessBase.sendError("User does not exist")

        # Update the document and return a success message
        DataAccessBase.USER_COL.update_one({"_id": id}, {"$set": kwargs})
        return DataAccessBase.sendSuccess("User updated")

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

    @staticmethod
    @DataAccessBase.dict_wrap
    def reject_user(id: str) -> DictParse:
        """Reject the user from being a user on this platform"""

        # Check if user is in the REGISTER_COL
        user = DataAccessBase.REGISTER_COL.find_one({"_id": id})
        if user is not None:
            # If the user exists delete their record
            DataAccessBase.REGISTER_COL.delete_one({"_id": id})

            # Return
            return DataAccessBase.sendSuccess("User denied")

        # Return an error if else
        return DataAccessBase.sendError("User not found")

    @staticmethod
    @DataAccessBase.dict_wrap
    def kick_user(id: str) -> DictParse:
        """Kick the user from the organization"""

        # Check if user is in the REGISTER_COL
        user = DataAccessBase.USER_COL.find_one({"_id": id})
        if user is not None:
            # Add user to the former user collection
            DataAccessBase.FORMER_USERS_COL.insert_one(user)

            # Get the user's id
            id = user["_id"]

            # Iterate through all the units the user is in
            for i in user["units"]:
                # Get the unit info
                unit = DataAccessBase.UNIT_COL.find_one({"_id": i})

                # Remove user from the officers list, if so
                if id in unit["officers"]:
                    unit["officers"].remove(id)
                # Remove user from the members list, if so
                if id in unit["members"]:
                    unit["members"].remove(id)

                # Replace the unit information
                DataAccessBase.UNIT_COL.replace_one({"_id": unit["_id"]}, unit)

            # If the user exists delete their record
            DataAccessBase.USER_COL.delete_one({"_id": id})

            # Return
            return DataAccessBase.sendSuccess("User kicked out")

        # Return an error if else
        return DataAccessBase.sendError("User not found")
