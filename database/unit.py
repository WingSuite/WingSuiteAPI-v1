# Imports
from utils.dict_parse import DictParse
from config.config import config
from .base import DataAccessBase
from typing import Union, Any
from database.user import UserAccess
from models.unit import Unit
from models.user import User
import uuid


class UnitAccess(DataAccessBase):
    """Class that handles unit information"""

    @staticmethod
    @DataAccessBase.dict_wrap
    def create_unit(
        name: str,
        unit_type: str,
        parent: str,
        children: list,
        officers: list,
        members: list,
        **kwargs: Any
    ) -> DictParse:
        """Method to create a new unit"""

        # If the inputted type is an approved type, return with an
        # error message
        if unit_type not in config.unitTypes:
            return DataAccessBase.sendError(
                "Unit type is not a valid type. \nSelect from: "
                + ", ".join(config.unitTypes)
            )

        # Prep data to be inserted
        data = {
            k: v for k, v in locals().items() if k not in ["kwargs", "args"]
        }
        data.update(locals()["kwargs"])
        data["_id"] = uuid.uuid4().hex

        # Insert into the collection
        DataAccessBase.UNIT_COL.insert_one(data)

        # Add the inputted officers and members into the unit
        for item in officers + members:
            # Get the user object based on iterated item
            user = UserAccess.get_user(item).message

            # Continue if the iterated user is not a User
            if type(user) != User:
                continue

            # Add the officer to the unit
            user.add_unit(data["_id"])

            # Update officer
            UserAccess.update_user(item, **user.info)

        # Iterate through the children's list and update pointers
        for item in children:
            # Get the unit object based on the iterated item
            unit = UnitAccess.get_unit(item).message

            # Continue if the iterated unit is not a Unit
            if type(user) != Unit:
                continue

            # Update their parent pointer
            unit.info.parent = data["_id"]

            # Update child unit
            UnitAccess.update_unit(item, **unit.info)

        # Update the unit's parent node if one is provided
        if parent != "":
            # Get the unit object based on the iterated item
            unit = UnitAccess.get_unit(parent).message

            # Update children info
            unit.add_child(data["_id"])

            # Update child unit
            UnitAccess.update_unit(unit.info._id, **unit.info)

        # Send success message after successful operation
        return DataAccessBase.sendSuccess("Unit added")

    @staticmethod
    @DataAccessBase.dict_wrap
    def delete_unit(id: str) -> DictParse:
        """Method to delete a unit"""

        # Check if the unit based on its id does not exist
        if DataAccessBase.UNIT_COL.find_one({"_id": id}) is None:
            return DataAccessBase.sendError("Unit does not exist")

        # Delete the document and return a success message
        DataAccessBase.UNIT_COL.delete_one({"_id": id})
        return DataAccessBase.sendSuccess("Unit deleted")

    @staticmethod
    @DataAccessBase.dict_wrap
    def update_unit(id: str, **kwargs) -> DictParse:
        """Method to delete a unit"""

        # Delete the id in the kwargs
        del kwargs["_id"]

        # Check if the unit based on its id does exist
        if DataAccessBase.UNIT_COL.find_one({"_id": id}) is None:
            return DataAccessBase.sendError("Unit does not exist")

        # Update the document and return a success message
        DataAccessBase.UNIT_COL.update_one({"_id": id}, {"$set": kwargs})
        return DataAccessBase.sendSuccess("Unit updated")

    @staticmethod
    @DataAccessBase.dict_wrap
    def get_unit(id: str) -> Union[Unit, DictParse]:
        """Method to get a unit by ID"""

        # Search the collection based on id
        unit = DataAccessBase.UNIT_COL.find_one({"_id": id})

        # Return if the given unit is not in the database
        if unit is None:
            return {
                "status": "error",
                "message": "Unit not found",
            }

        # Return with a User object
        return DataAccessBase.sendSuccess(Unit(**unit))
