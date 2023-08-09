# Imports
from utils.dict_parse import DictParse
from database.base import DataAccessBase
from models.statistics.five_point import FivePoint
from typing import Any
import uuid
import math


class FivePointAccess(DataAccessBase):
    """Class that handles FivePoint information"""

    @staticmethod
    @DataAccessBase.dict_wrap
    def create_five_point(
        from_user: str,
        to_user: str,
        name: str,
        datetime_taken: int,
        category_1: int,
        category_2: int,
        category_3: int,
        category_4: int,
        category_5: int,
        **kwargs: Any
    ) -> DictParse:
        """Method to create a five point"""

        # Combine kwargs and args
        data = {
            k: v for k, v in locals().items() if k not in ["kwargs", "args"]
        }

        # Add or update data
        data.update(locals()["kwargs"])
        data["_id"] = uuid.uuid4().hex
        data["stat_type"] = "five_point"
        data["subscores"] = {
            "category_1": category_1,
            "category_2": category_2,
            "category_3": category_3,
            "category_4": category_4,
            "category_5": category_5,
        }
        data["info"] = {}

        # Remove unncessary data
        del data["category_1"]
        del data["category_2"]
        del data["category_3"]
        del data["category_4"]
        del data["category_5"]

        # Get an object representation of the given info
        five_point_obj = FivePoint(**data)

        # Insert into the collection
        DataAccessBase.CURRENT_STATS_COL.insert_one(five_point_obj.info)

        # Return a statement
        return DataAccessBase.sendSuccess("Five point evaluation created")

    @staticmethod
    @DataAccessBase.dict_wrap
    def get_five_point(id: str) -> DictParse:
        """Get Five Point based on Five Point ID"""

        # Search the collection based on id
        five_point = DataAccessBase.CURRENT_STATS_COL.find_one({"_id": id})

        # Return if the given five point is not in the database
        if five_point is None:
            return {
                "status": "error",
                "message": "Five Point evaluation not found",
            }

        # Return with a five point object
        return DataAccessBase.sendSuccess(FivePoint(**five_point))

    @staticmethod
    @DataAccessBase.dict_wrap
    def get_user_five_point(
        id: str, page_size: int, page_index: int
    ) -> DictParse:
        """Method to retrieve a multiple five points based on the given ID"""

        # Check if the page_size or page_index is negative
        if page_size <= 0 or page_index < 0:
            return DataAccessBase.sendError("Invalid pagination size or index")

        # Set query
        query = {"stat_type": "five_point", "to_user": id}

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

        # Return if the given five point is not in the database
        if result is None:
            return {
                "status": "error",
                "message": "Five point evaluation not found",
            }

        # Turn result into a list
        result = list(result)

        # Return with a five point object
        return DataAccessBase.sendSuccess(result, pages=pages)

    @staticmethod
    @DataAccessBase.dict_wrap
    def get_test_five_point(
        category_1: int,
        category_2: int,
        category_3: int,
        category_4: str,
        category_5: str,
        **kwargs: Any
    ):
        """Calculate the user's test five point information"""
        # Combine kwargs and args
        data = {
            k: v for k, v in locals().items() if k not in ["kwargs", "args"]
        }

        # Add or update data
        data.update(locals()["kwargs"])
        data["_id"] = uuid.uuid4().hex
        data["stat_type"] = "five_point"
        data["subscores"] = {
            "category_1": category_1,
            "category_2": category_2,
            "category_3": category_3,
            "category_4": category_4,
            "category_5": category_5,
        }
        data["info"] = {}

        # Remove unncessary data
        del data["category_1"]
        del data["category_2"]
        del data["category_3"]
        del data["category_4"]
        del data["category_5"]

        # Get an object representation of the given info
        five_point_obj = FivePoint(
            **data, from_user=0, to_user=0, name=0, datetime_taken=0
        )

        # Return results
        return DataAccessBase.sendSuccess(five_point_obj.info.composite_score)

    @staticmethod
    @DataAccessBase.dict_wrap
    def update_five_point(id: str, **kwargs: Any) -> DictParse:
        """Method to update a five point"""

        # Check if the five point based on its id does exist
        if DataAccessBase.CURRENT_STATS_COL.find_one({"_id": id}) is None:
            return DataAccessBase.sendError(
                "Five point evaluation does not exist"
            )

        # Update the document and return a success message
        DataAccessBase.CURRENT_STATS_COL.update_one(
            {"_id": id}, {"$set": kwargs}
        )
        return DataAccessBase.sendSuccess("Five point updated")

    @staticmethod
    @DataAccessBase.dict_wrap
    def delete_five_point(id: str) -> DictParse:
        """Method to delete a five point"""

        # Check if the five point based on its id does not exist
        five_point = DataAccessBase.CURRENT_STATS_COL.find_one({"_id": id})
        if five_point is None:
            return DataAccessBase.sendError(
                "Five point evaluation does not exist"
            )

        # Delete the document and return a success message
        DataAccessBase.CURRENT_STATS_COL.delete_one({"_id": id})
        return DataAccessBase.sendSuccess("Five point evaluation deleted")
