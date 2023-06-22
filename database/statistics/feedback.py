# Imports
from utils.dict_parse import DictParse
from database.base import DataAccessBase
from models.statistics.feedback import Feedback
from models.user import User
from typing import Any
import uuid
import math
import time


class FeedbackAccess(DataAccessBase):
    """Class that handles feedback information"""

    @staticmethod
    @DataAccessBase.dict_wrap
    def create_feedback(
        from_user: str, to_user: str, name: str, feedback: str, **kwargs: Any
    ) -> DictParse:
        """Method to create a feedback"""

        # Prep data to be inserted
        data = {
            k: v for k, v in locals().items() if k not in ["kwargs", "args"]
        }
        data.update(locals()["kwargs"])
        data["_id"] = uuid.uuid4().hex
        data["stat_type"] = "feedback"
        data["datetime_created"] = int(time.time())

        # Insert into the collection
        DataAccessBase.CURRENT_STATS_COL.insert_one(data)

        # Return a statement
        return DataAccessBase.sendSuccess("Feedback created")

    @staticmethod
    @DataAccessBase.dict_wrap
    def delete_feedback(id: str) -> DictParse:
        """Method to delete an feedback"""

        # Check if the feedback based on its id does not exist
        feedback = DataAccessBase.CURRENT_STATS_COL.find_one({"_id": id})
        if feedback is None:
            return DataAccessBase.sendError("Feedback does not exist")

        # Delete the document and return a success message
        DataAccessBase.CURRENT_STATS_COL.delete_one({"_id": id})
        return DataAccessBase.sendSuccess("Feedback deleted")

    @staticmethod
    @DataAccessBase.dict_wrap
    def update_feedback(id: str, **kwargs: Any) -> DictParse:
        """Method to delete a feedback"""

        # Check if the feedback based on its id does exist
        if DataAccessBase.CURRENT_STATS_COL.find_one({"_id": id}) is None:
            return DataAccessBase.sendError("Feedback does not exist")

        # Update the document and return a success message
        DataAccessBase.CURRENT_STATS_COL.update_one(
            {"_id": id}, {"$set": kwargs}
        )
        return DataAccessBase.sendSuccess("Feedback updated")

    @staticmethod
    @DataAccessBase.dict_wrap
    def get_feedback(id: str) -> DictParse:
        """Method to retrieve a single feedback based on ID"""

        # Search the collection based on id
        feedback = DataAccessBase.CURRENT_STATS_COL.find_one(
            {"stat_type": "feedback", "_id": id}
        )

        # Return if the given feedback is not in the database
        if feedback is None:
            return {
                "status": "error",
                "message": "Feedback not found",
            }

        # Return with a Feedback object
        return DataAccessBase.sendSuccess(Feedback(**feedback))

    @staticmethod
    @DataAccessBase.dict_wrap
    def get_own_feedback(
        id: str, page_size: int, page_index: int
    ) -> DictParse:
        """Method to retrieve a multiple feedback based on the receiver's ID"""

        # Check if the page_size or page_index is negative
        if page_size <= 0 or page_index < 0:
            return DataAccessBase.sendError("Invalid pagination size or index")

        # Get the total amount of pages based on pagination size
        pages = math.ceil(
            (
                DataAccessBase.CURRENT_STATS_COL.count_documents(
                    {"stat_type": "feedback", "to_user": id}
                )
            )
            / page_size
        )

        # Check if the page_index is outside the page range
        if page_index >= pages:
            return DataAccessBase.sendError("Pagination index out of bounds")

        # Calculate skip value
        skips = page_size * (page_index)

        # Search the collection based on id
        result = (
            DataAccessBase.CURRENT_STATS_COL.find(
                {"stat_type": "feedback", "to_user": id}
            )
            .skip(skips)
            .limit(page_size)
        )

        # Return if the given feedback is not in the database
        if result is None:
            return {
                "status": "error",
                "message": "Feedback not found",
            }

        # Turn result into a list
        result = list(result)

        # Convert every `from_user`'s ID to name
        for i in range(len(result)):
            # Get the information of the iterated ID
            user = User(**DataAccessBase.USER_COL.find_one(
                {"_id": result[i]["from_user"]}
            ))

            # Replace the content of the `from_user` attribute in the current
            # result list
            result[i]["from_user"] = user.get_fullname(lastNameFirst=True)

        # Return with a Feedback object
        return DataAccessBase.sendSuccess(result, pages=pages)
