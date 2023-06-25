# Imports
from utils.dict_parse import DictParse
from database.base import DataAccessBase
from models.statistics.pfa import PFA
from typing import Any
import uuid


class PFAAccess(DataAccessBase):
    """Class that handles PFA information"""

    @staticmethod
    @DataAccessBase.dict_wrap
    def create_pfa(
        from_user: str,
        to_user: str,
        name: str,
        pushup: str,
        situp: str,
        run: str,
        points: str,
        **kwargs: Any
    ) -> DictParse:
        """Method to create a PFA"""

        # Prep data to be inserted
        data = {
            k: v for k, v in locals().items() if k not in ["kwargs", "args"]
        }
        data.update(locals()["kwargs"])
        data["_id"] = uuid.uuid4().hex
        data["stat_type"] = "pfa"

        # Insert into the collection
        DataAccessBase.CURRENT_STATS_COL.insert_one(data)

        # Return a statement
        return DataAccessBase.sendSuccess("PFA created")

    @staticmethod
    @DataAccessBase.dict_wrap
    def delete_pfa(id: str) -> DictParse:
        """Method to delete an PFA"""

        # Check if the PFA based on its id does not exist
        pfa = DataAccessBase.CURRENT_STATS_COL.find_one({"_id": id})
        if pfa is None:
            return DataAccessBase.sendError("PFA does not exist")

        # Delete the document and return a success message
        DataAccessBase.CURRENT_STATS_COL.delete_one({"_id": id})
        return DataAccessBase.sendSuccess("PFA deleted")

    @staticmethod
    @DataAccessBase.dict_wrap
    def update_pfa(id: str, **kwargs: Any) -> DictParse:
        """Method to delete a PFA"""

        # Check if the PFA based on its id does exist
        if DataAccessBase.CURRENT_STATS_COL.find_one({"_id": id}) is None:
            return DataAccessBase.sendError("PFA does not exist")

        # Update the document and return a success message
        DataAccessBase.CURRENT_STATS_COL.update_one(
            {"_id": id}, {"$set": kwargs}
        )
        return DataAccessBase.sendSuccess("PFA updated")

    @staticmethod
    @DataAccessBase.dict_wrap
    def get_pfa(id: str) -> DictParse:
        # Search the collection based on id
        pfa = DataAccessBase.CURRENT_STATS_COL.find_one({"_id": id})

        # Return if the given PFA is not in the database
        if pfa is None:
            return {
                "status": "error",
                "message": "PFA not found",
            }

        # Return with a PFA object
        return DataAccessBase.sendSuccess(PFA(**pfa))
