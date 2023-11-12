# Imports
from utils.dict_parse import DictParse
from database.base import DataAccessBase
from models.statistic.warrior import Warrior
from typing import Any
import uuid
import math
import time


class WarriorAccess(DataAccessBase):
    """Class that handles Warrior information"""

    @staticmethod
    @DataAccessBase.dict_wrap
    def create_warrior(
        from_user: str,
        to_user: str,
        name: str,
        datetime_taken: int,
        points_earned: int,
        total_points: int,
        **kwargs: Any
    ) -> DictParse:
        """Method to create a Warrior"""

        # Combine kwargs and args
        data = {
            k: v for k, v in locals().items() if k not in ["kwargs", "args"]
        }

        # Prep data to be inserted
        data.update(
            {k: v for k, v in locals()["kwargs"].items() if k[0] != "$"}
        )
        data["_id"] = uuid.uuid4().hex
        data["datetime_created"] = int(time.time())
        data["stat_type"] = "warrior"
        data["subscores"] = {
            "points_earned": points_earned,
            "total_points": total_points,
        }
        data["info"] = {}

        # Remove unnecessary data
        del data["points_earned"]
        del data["total_points"]

        # Get an object representation of the given info
        warrior = Warrior(**data)

        # Insert into the collection
        DataAccessBase.CURRENT_STATS_COL.insert_one(warrior.info)

        # Return a statement
        return DataAccessBase.sendSuccess("Warrior knowledge created")

    @staticmethod
    @DataAccessBase.dict_wrap
    def get_warrior(id: str) -> DictParse:
        # Search the collection based on id
        warrior = DataAccessBase.CURRENT_STATS_COL.find_one({"_id": id})

        # Return if the given warrior is not in the database
        if warrior is None:
            return {
                "status": "error",
                "message": "Warrior knowledge not found",
            }

        # Return with a warrior object
        return DataAccessBase.sendSuccess(Warrior(**warrior))

    @staticmethod
    @DataAccessBase.dict_wrap
    def get_user_warrior(
        id: str, page_size: int, page_index: int
    ) -> DictParse:
        """
        Method to retrieve a multiple warrior knowledge based on the
        receiver's ID
        """

        # Check if the page_size or page_index is negative
        if page_size <= 0 or page_index < 0:
            return DataAccessBase.sendError("Invalid pagination size or index")

        # Set query
        query = {"stat_type": "warrior", "to_user": id}

        # Get the total amount of pages based on pagination size
        pages = math.ceil(
            (DataAccessBase.CURRENT_STATS_COL.count_documents(query))
            / page_size
        )

        # Check if the page_index is outside the page range
        if page_index >= pages and pages != 0:
            return DataAccessBase.sendError("Pagination index out of bounds")

        # Calculate skip value
        skips = page_size * (page_index)

        # Search the collection based on id
        result = (
            DataAccessBase.CURRENT_STATS_COL.find(query)
            .skip(skips)
            .limit(page_size)
        )

        # Return if the given warrior knowledge is not in the database
        if result is None:
            return {
                "status": "error",
                "message": "Warrior Knowledge not found",
            }

        # Turn result into a list
        result = list(result)

        print(result)

        # Return with a warrior knowledge object
        return DataAccessBase.sendSuccess(result, pages=pages)

    @staticmethod
    @DataAccessBase.dict_wrap
    def get_test_warrior(points_earned: int, total_points: int, **kwargs: Any):
        """Calculate the user's test PFA information"""
        # Combine kwargs and args
        data = {
            k: v for k, v in locals().items() if k not in ["kwargs", "args"]
        }

        # Prep data to be inserted
        data.update(
            {k: v for k, v in locals()["kwargs"].items() if k[0] != "$"}
        )
        data["_id"] = uuid.uuid4().hex
        data["datetime_created"] = int(time.time())
        data["stat_type"] = "warrior"
        data["subscores"] = {
            "points_earned": points_earned,
            "total_points": total_points,
        }
        data["info"] = {}

        # Remove unnecessary data
        del data["points_earned"]
        del data["total_points"]

        # Get an object representation of the given info
        warrior_obj = Warrior(
            **data, from_user=0, to_user=0, name=0, datetime_taken=0
        )

        # Return results
        return DataAccessBase.sendSuccess(warrior_obj.info.composite_score)

    @staticmethod
    @DataAccessBase.dict_wrap
    def update_warrior(id: str, **kwargs: Any) -> DictParse:
        """Method to delete a warrior"""

        # Check if the warrior based on its id does exist
        if DataAccessBase.CURRENT_STATS_COL.find_one({"_id": id}) is None:
            return DataAccessBase.sendError("Warrior knowledge does not exist")

        # Disable the changing of time_created attribute
        if "datetime_created" in kwargs:
            return DataAccessBase.sendError("Cannot change creation datetime")

        # Update the document and return a success message
        DataAccessBase.CURRENT_STATS_COL.update_one(
            {"_id": id}, {"$set": kwargs}
        )
        return DataAccessBase.sendSuccess("Warrior knowledge updated")

    @staticmethod
    @DataAccessBase.dict_wrap
    def delete_warrior(id: str) -> DictParse:
        """Method to delete an Warrior"""

        # Check if the Warrior based on its id does not exist
        warrior = DataAccessBase.CURRENT_STATS_COL.find_one({"_id": id})
        if warrior is None:
            return DataAccessBase.sendError("Warrior knowledge does not exist")

        # Delete the document and return a success message
        DataAccessBase.CURRENT_STATS_COL.delete_one({"_id": id})
        return DataAccessBase.sendSuccess("Warrior knowledge deleted")
