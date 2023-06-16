# Imports
from flask_jwt_extended import decode_token
from utils.dict_parse import DictParse
from .base import DataAccessBase
from typing import Union, Any
from models.stats import Stats


class UserAccess(DataAccessBase):
    """Class that handles user information"""

    @staticmethod
    @DataAccessBase.dict_wrap
    def add_meta(id: str) -> DictParse:
        """Method that handles adding metadata to the system"""

        # Add metadata to the list and return success if the given
        # information is not the system
        stat = DataAccessBase.META_COL.find_one({"_id": id})
        if stat is not None:
            # Insert metadata into the database and return sucess
            DataAccessBase.META_COL.insert_one(stat)
            return DataAccessBase.sendSuccess("Metadata added to system")
        # Return false if the given information exists
        else:
            return DataAccessBase.sendError("Metadata already exists")

    @staticmethod
    @DataAccessBase.dict_wrap
    def update_meta(id: str, **kwargs: Any) -> DictParse:
        """Update the specified user's information"""

        # Delete the id in the kwargs
        del kwargs["_id"]

        # Check if the unit based on its id does exist
        if DataAccessBase.META_COL.find_one({"_id": id}) is None:
            return DataAccessBase.sendError("MEtadata does not exist")

        # Update the document and return a success message
        DataAccessBase.META_COL.update_one({"_id": id}, {"$set": kwargs})
        return DataAccessBase.sendSuccess("Metadata updated")

    @staticmethod
    @DataAccessBase.dict_wrap
    def get_meta(id: str) -> Union[Stats, DictParse]:
        """Base method for get_meta methods"""

        # Get the results from the query
        stat = DataAccessBase.META_COL.find_one({"_id": id})

        # Return if the given user is not in the database
        if stat is None:
            return DataAccessBase.sendError("Metadata not found")

        # Return results based on types of representation
        return DataAccessBase.sendSuccess(Stats(**stat))
