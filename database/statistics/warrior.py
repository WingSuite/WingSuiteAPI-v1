# Imports
from utils.dict_parse import DictParse
from database.base import DataAccessBase
from models.statistics.warrior import Warrior
from typing import Any
import uuid


class WarriorAccess(DataAccessBase):
    """Class that handles Warrior information"""

    @staticmethod
    @DataAccessBase.dict_wrap
    def create_warrior(
        from_user: str, to_user: str, name: str, warrior: str, **kwargs: Any
    ) -> DictParse:
        """Method to create a Warrior"""

        # Prep data to be inserted
        data = {
            k: v for k, v in locals().items() if k not in ["kwargs", "args"]
        }
        data.update(locals()["kwargs"])
        data["_id"] = uuid.uuid4().hex
        data["stat_type"] = "warrior"

        # Insert into the collection
        DataAccessBase.CURRENT_STATS_COL.insert_one(data)

        # Return a statement
        return DataAccessBase.sendSuccess("Warrior created")

    @staticmethod
    @DataAccessBase.dict_wrap
    def delete_warrior(id: str) -> DictParse:
        """Method to delete an Warrior"""

        # Check if the Warrior based on its id does not exist
        warrior = DataAccessBase.CURRENT_STATS_COL.find_one({"_id": id})
        if warrior is None:
            return DataAccessBase.sendError("Warrior does not exist")

        # Delete the document and return a success message
        DataAccessBase.CURRENT_STATS_COL.delete_one({"_id": id})
        return DataAccessBase.sendSuccess("Warrior deleted")

    @staticmethod
    @DataAccessBase.dict_wrap
    def update_warrior(id: str, **kwargs: Any) -> DictParse:
        """Method to delete a warrior"""

        # Check if the warrior based on its id does exist
        if DataAccessBase.CURRENT_STATS_COL.find_one({"_id": id}) is None:
            return DataAccessBase.sendError("Warrior does not exist")

        # Update the document and return a success message
        DataAccessBase.CURRENT_STATS_COL.update_one(
            {"_id": id}, {"$set": kwargs}
        )
        return DataAccessBase.sendSuccess("Warrior updated")

    @staticmethod
    @DataAccessBase.dict_wrap
    def get_warrior(id: str) -> DictParse:
        # Search the collection based on id
        warrior = DataAccessBase.CURRENT_STATS_COL.find_one({"_id": id})

        # Return if the given warrior is not in the database
        if warrior is None:
            return {
                "status": "error",
                "message": "Warrior not found",
            }

        # Return with a warrior object
        return DataAccessBase.sendSuccess(Warrior(**warrior))
