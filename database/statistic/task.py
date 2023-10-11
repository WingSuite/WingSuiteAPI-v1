# Imports
from utils.dict_parse import DictParse
from database.base import DataAccessBase
# from database.user import UserAccess
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
        data["datetime_taken"] = int(time.time())
        data["requests"] = {}
        data["record"] = {}
        data["not_complete"] = set()
        data["info"] = {}

        # Insert into the collection
        DataAccessBase.TASK_COL.insert_one(data)

        # Return a statement
        return DataAccessBase.sendSuccess("Task created")

    @staticmethod
    @DataAccessBase.dict_wrap
    def delete_task(id: str) -> DictParse:
        """Method to delete an task"""

        # Check if the task based on its id does not exist
        task = DataAccessBase.TASK_COL.find_one({"_id": id})
        if task is None:
            return DataAccessBase.sendError("Task does not exist")

        # Delete the document and return a success message
        DataAccessBase.TASK_COL.delete_one({"_id": id})
        return DataAccessBase.sendSuccess("Task deleted")

    @staticmethod
    @DataAccessBase.dict_wrap
    def update_task(id: str, **kwargs: Any) -> DictParse:
        """Method to delete a task"""

        # Check if the task based on its id does exist
        if DataAccessBase.TASK_COL.find_one({"_id": id}) is None:
            return DataAccessBase.sendError("Task does not exist")

        # Update the document and return a success message
        DataAccessBase.TASK_COL.update_one({"_id": id}, {"$set": kwargs})
        return DataAccessBase.sendSuccess("Task updated")

    @staticmethod
    @DataAccessBase.dict_wrap
    def get_task(id: str) -> DictParse:
        """Method to retrieve a single task based on ID"""

        # Search the collection based on id
        task = DataAccessBase.TASK_COL.find_one(
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
    def get_own_task(
        id: str, page_size: int, page_index: int, sent: bool
    ) -> DictParse:
        """Method to retrieve a multiple task based on the receiver's ID"""

        # Generate query based on whether to return sent or received documents
        query = {"stat_type": "task", "from_user": id}

        # Check if the page_size or page_index is negative
        if page_size <= 0 or page_index < 0:
            return DataAccessBase.sendError("Invalid pagination size or index")

        # Get the total amount of pages based on pagination size
        pages = math.ceil(
            (DataAccessBase.TASK_COL.count_documents(query)) / page_size
        )

        # Check if the page_index is outside the page range
        if page_index >= pages:
            return DataAccessBase.sendError("Pagination index out of bounds")

        # Calculate skip value
        skips = page_size * (page_index)

        # Search the collection based on id
        result = (
            DataAccessBase.TASK_COL.find(query).skip(skips).limit(page_size)
        )

        # Return if the given feedback is not in the database
        if result is None:
            return {
                "status": "error",
                "message": "Feedback not found",
            }

        # Cast result into list format
        result = list(result)

        # Return with a Feedback object
        return DataAccessBase.sendSuccess(result, pages=pages)
