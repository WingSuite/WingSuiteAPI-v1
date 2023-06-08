# Imports
from config.config import config
from .base import DataAccessBase
from models.unit import Unit
import pprint
import uuid


class UnitAccess(DataAccessBase):
    """Class that handles unit information"""

    # Store the required arguments for this class
    ARGS = DataAccessBase.REQ_ARGS.unit

    @staticmethod
    @DataAccessBase.dict_wrap
    @DataAccessBase.param_check(ARGS.create_unit.keys())
    def create_unit(**kwargs):
        """Method to create a new unit"""

        # Check if the given data is in the correct data types
        schema = {key: type(value) for key, value in
                  UnitAccess.ARGS.create_unit.items()}
        if not (DataAccessBase.checkDataType(kwargs, schema)):
            return DataAccessBase.sendError(
                "Inputs should be in the following structure:\n"
                + pprint.pformat(schema)
            )

        # If the inputted type is an approved type, return with an
        # error message
        if kwargs["type"] not in config.unitTypes:
            return DataAccessBase.sendError(
                "Unit type not a valid type. Selected from: "
                + ", ".join(config.unitTypes)
            )

        # Prep the incoming data for insertion into the collection
        kwargs["_id"] = uuid.uuid4().hex

        # Insert into the collection and send a success message
        DataAccessBase.UNIT_COL.insert_one(kwargs)
        return DataAccessBase.sendSuccess("Unit added")

    @staticmethod
    @DataAccessBase.dict_wrap
    def delete_unit(id):
        """Method to delete a unit"""

        # Check if the unit based on its id does not exist
        if (DataAccessBase.UNIT_COL.find_one({"_id": id}) is None):
            return DataAccessBase.sendError("Unit does not exist")

        # Delete the document and return a success message
        DataAccessBase.UNIT_COL.delete_one({"_id": id})
        return DataAccessBase.sendSuccess("Unit deleted")

    @staticmethod
    @DataAccessBase.dict_wrap
    def update_unit(id, **kwargs):
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
    def get_unit(id):
        """Method to get a unit by ID"""

        # Delete the document and return a success message
        unit = Unit(**DataAccessBase.UNIT_COL.find_one({"_id": id}))
        return DataAccessBase.sendSuccess("Unit updated")
