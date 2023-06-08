# Imports
from config.config import config
from .base import DataAccessBase
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
        return DataAccessBase.sendSuccess(
            f"{kwargs['name']} added to units list"
        )
