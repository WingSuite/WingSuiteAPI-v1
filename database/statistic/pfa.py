# Imports
from utils.dict_parse import DictParse
from database.base import DataAccessBase
from models.statistic.pfa import PFA
from typing import Any
import uuid
import math


class PFAAccess(DataAccessBase):
    """Class that handles PFA information"""

    @staticmethod
    @DataAccessBase.dict_wrap
    def create_pfa(
        from_user: str,
        to_user: str,
        name: str,
        datetime_taken: int,
        pushup: int,
        situp: int,
        run: str,
        age: int,
        gender: str,
        **kwargs: Any
    ) -> DictParse:
        """Method to create a PFA"""

        # Combine kwargs and args
        data = {
            k: v for k, v in locals().items() if k not in ["kwargs", "args"]
        }

        # Ensure that the gender is either male or female
        if gender.lower() != "male" and gender.lower() != "female":
            return DataAccessBase.sendError("Incorrect gender")

        # Add or update data
        data.update(locals()["kwargs"])
        data["_id"] = uuid.uuid4().hex
        data["stat_type"] = "pfa"
        data["subscores"] = {
            "pushup": pushup,
            "situp": situp,
            "run": run,
        }
        data["info"] = {
            "age": age,
            "gender": gender.lower(),
        }

        # Remove unncessary data
        del data["pushup"]
        del data["situp"]
        del data["run"]
        del data["age"]
        del data["gender"]

        # Get an object representation of the given info
        pfa_obj = PFA(**data)

        # Insert into the collection
        DataAccessBase.CURRENT_STATS_COL.insert_one(pfa_obj.info)

        # Return a statement
        return DataAccessBase.sendSuccess("PFA created")

    @staticmethod
    @DataAccessBase.dict_wrap
    def get_pfa(id: str) -> DictParse:
        """Get PFA based on PFA ID"""

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

    @staticmethod
    @DataAccessBase.dict_wrap
    def get_user_pfa(id: str, page_size: int, page_index: int) -> DictParse:
        """Method to retrieve a multiple pfa based on the receiver's ID"""

        # Check if the page_size or page_index is negative
        if page_size <= 0 or page_index < 0:
            return DataAccessBase.sendError("Invalid pagination size or index")

        # Set query
        query = {"stat_type": "pfa", "to_user": id}

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

        # Return if the given pfa is not in the database
        if result is None:
            return {
                "status": "error",
                "message": "PFA not found",
            }

        # Turn result into a list
        result = list(result)

        # Return with a PFA object
        return DataAccessBase.sendSuccess(result, pages=pages)

    @staticmethod
    @DataAccessBase.dict_wrap
    def get_test_pfa(
        pushup: int, situp: int, run: str, age: int, gender: str, **kwargs: Any
    ):
        """Calculate the user's test PFA information"""
        # Combine kwargs and args
        data = {
            k: v for k, v in locals().items() if k not in ["kwargs", "args"]
        }

        # Ensure that the gender is either male or female
        if gender.lower() != "male" and gender.lower() != "female":
            return DataAccessBase.sendError("Incorrect gender")

        # Add or update data
        data.update(locals()["kwargs"])
        data["_id"] = uuid.uuid4().hex
        data["stat_type"] = "pfa"
        data["subscores"] = {
            "pushup": pushup,
            "situp": situp,
            "run": run,
        }
        data["info"] = {
            "age": age,
            "gender": gender.lower(),
        }

        # Remove unncessary data
        del data["pushup"]
        del data["situp"]
        del data["run"]
        del data["age"]
        del data["gender"]

        # Get an object representation of the given info
        pfa_obj = PFA(**data, from_user=0, to_user=0, name=0, datetime_taken=0)

        # Return results
        return DataAccessBase.sendSuccess(pfa_obj.info.composite_score)

    @staticmethod
    @DataAccessBase.dict_wrap
    def update_pfa(id: str, **kwargs: Any) -> DictParse:
        """Method to update a PFA"""

        # Check if the PFA based on its id does exist
        if DataAccessBase.CURRENT_STATS_COL.find_one({"_id": id}) is None:
            return DataAccessBase.sendError("PFA does not exist")

        # Ensure that the gender is either male or female
        if (
            kwargs["info"]["gender"] != "male"
            and kwargs["info"]["gender"] != "female"
        ):
            return DataAccessBase.sendError("Incorrect gender")

        # Update the document and return a success message
        DataAccessBase.CURRENT_STATS_COL.update_one(
            {"_id": id}, {"$set": kwargs}
        )
        return DataAccessBase.sendSuccess("PFA updated")

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
