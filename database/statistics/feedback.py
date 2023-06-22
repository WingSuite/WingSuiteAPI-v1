# Imports
from utils.dict_parse import DictParse
from database.base import DataAccessBase
from models.statistics.feedback import Feedback
from typing import Any
import uuid


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
        # Search the collection based on id
        feedback = DataAccessBase.CURRENT_STATS_COL.find_one({"_id": id})

        # Return if the given feedback is not in the database
        if feedback is None:
            return {
                "status": "error",
                "message": "Feedback not found",
            }

        # Return with a Feedback object
        return DataAccessBase.sendSuccess(Feedback(**feedback))
