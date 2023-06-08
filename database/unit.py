# Imports
from utils.dict_parse import DictParse
from config.config import config
from .base import DataAccessBase
from typing import Union, Any
from models.unit import Unit
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
                "Unit type not a valid type. Selected from: "
                + ", ".join(config.unitTypes)
            )

        # Prep data to be inserted
        data = {k: v for k, v in locals().items()
                if k not in ["kwargs", "args"]}
        data.update(locals()["kwargs"])
        data["_id"] = uuid.uuid4().hex

        # Insert into the collection and send a success message
        DataAccessBase.UNIT_COL.insert_one(data)
        return DataAccessBase.sendSuccess("Unit added")

    @staticmethod
    @DataAccessBase.dict_wrap
    def delete_unit(id: str) -> DictParse:
        """Method to delete a unit"""

        # Check if the unit based on its id does not exist
        if (DataAccessBase.UNIT_COL.find_one({"_id": id}) is None):
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
        if (DataAccessBase.UNIT_COL.find_one({"_id": id}) is None):
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
