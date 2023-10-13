# Imports
from utils.dict_parse import DictParse
from database.base import DataAccessBase
from database.user import UserAccess
from models.statistic.task import Task
from typing import Any, List
import uuid
import math
import time


class TaskAccess(DataAccessBase):
    """Class that handles task information"""

    @staticmethod
    @DataAccessBase.dict_wrap
    def create_task(
        from_user: str,
        to_users: List[str],
        name: str,
        description: str,
        suspense: int,
        auto_accept_requests: bool,
        **kwargs: Any
    ) -> DictParse:
        """Method to create a task"""

        # Prep data to be inserted
        data = {
            k: v for k, v in locals().items() if k not in ["kwargs", "args"]
        }
        data.update(locals()["kwargs"])
        data["_id"] = uuid.uuid4().hex
        data["stat_type"] = "task"
        data["datetime_created"] = int(time.time())
        data["requests"] = {}
        data["record"] = {}
        data["not_complete"] = []

        # Insert into the collection
        DataAccessBase.CURRENT_STATS_COL.insert_one(data)

        # Return a statement
        return DataAccessBase.sendSuccess("Task created")

    @staticmethod
    @DataAccessBase.dict_wrap
    def delete_task(id: str) -> DictParse:
        """Method to delete an task"""

        # Check if the task based on its id does not exist
        task = DataAccessBase.CURRENT_STATS_COL.find_one({"_id": id})
        if task is None:
            return DataAccessBase.sendError("Task does not exist")

        # Delete the document and return a success message
        DataAccessBase.CURRENT_STATS_COL.delete_one({"_id": id})
        return DataAccessBase.sendSuccess("Task deleted")

    @staticmethod
    @DataAccessBase.dict_wrap
    def update_task(id: str, **kwargs: Any) -> DictParse:
        """Method to delete a task"""

        # Check if the task based on its id does exist
        if DataAccessBase.CURRENT_STATS_COL.find_one({"_id": id}) is None:
            return DataAccessBase.sendError("Task does not exist")

        # Disable the changing of time_created attribute
        if ("datetime_created" in kwargs):
            return DataAccessBase.sendError("Cannot change creation datetime")

        # Update the document and return a success message
        DataAccessBase.CURRENT_STATS_COL.update_one(
            {"_id": id}, {"$set": kwargs}
        )
        return DataAccessBase.sendSuccess("Task updated")

    @staticmethod
    @DataAccessBase.dict_wrap
    def get_task(id: str) -> DictParse:
        """Method to retrieve a single task based on ID"""

        # Search the collection based on id
        task = DataAccessBase.CURRENT_STATS_COL.find_one(
            {"stat_type": "task", "_id": id}
        )

        # Return if the given task is not in the database
        if task is None:
            return {
                "status": "error",
                "message": "Task not found",
            }

        # Return with a task object
        return DataAccessBase.sendSuccess(Task(**task))

    @staticmethod
    @DataAccessBase.dict_wrap
    def get_own_task(id: str, page_size: int, page_index: int) -> DictParse:
        """Method to retrieve a multiple task based on the receiver's ID"""

        # Generate query based on whether to return sent or received documents
        query = {"stat_type": "task", "from_user": id}

        # Check if the page_size or page_index is negative
        if page_size <= 0 or page_index < 0:
            return DataAccessBase.sendError("Invalid pagination size or index")

        # Get the total amount of pages based on pagination size
        pages = math.ceil(
            (DataAccessBase.CURRENT_STATS_COL.count_documents(query))
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
                query,
                {"requests": 0, "record": 0, "not_complete": 0, "to_users": 0},
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

        # Add a formatted from_user key for each feedback
        memoize = DictParse({})
        result = list(result)
        for i in result:
            # Add key if the iterated from_user is not memoized
            if i["from_user"] not in memoize:
                # Add user's formatted name to the memoization
                from_user = UserAccess.get_user(
                    i["from_user"], check_former=True
                ).message
                memoize[i["from_user"]] = from_user.get_fullname(
                    lastNameFirst=True, with_rank=True
                )

            # Add formatted key
            i["formatted_from_user"] = memoize[i["from_user"]]

        # Return with a Feedback object
        return DataAccessBase.sendSuccess(result, pages=pages)
