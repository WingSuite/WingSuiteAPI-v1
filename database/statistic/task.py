# Imports
from utils.time import seconds_to_largest_time_unit
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
        incomplete: List[str],
        name: str,
        description: str,
        suspense: int,
        auto_accept_requests: bool,
        reminders: dict,
        **kwargs: Any,
    ) -> DictParse:
        """Method to create a task"""

        # Prep data to be inserted
        data = {
            k: v for k, v in locals().items() if k not in ["kwargs", "args"]
        }
        data.update(
            {k: v for k, v in locals()["kwargs"].items() if k[0] != "$"}
        )
        data["_id"] = uuid.uuid4().hex
        data["stat_type"] = "task"
        data["datetime_created"] = int(time.time())
        data["pending"] = {}
        data["complete"] = {}

        # Insert into the collection
        DataAccessBase.CURRENT_STATS_COL.insert_one(data)

        # Return a statement
        return DataAccessBase.sendSuccess("Task created")

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

        # Get a list of users from the incomplete, pending, complete areas
        users_in_task = (
            list(task["incomplete"].keys())
            + list(task["pending"].keys())
            + list(task["complete"].keys())
        )

        # Get a mapping of their names
        mapping = {}
        for i in users_in_task:
            # Get the user's object
            user = UserAccess.get_user(i)

            # Save their name to mapping
            mapping[i] = user.message.get_fullname(with_rank=True)

        # Add info to the task details
        task["name_map"] = mapping

        # Return with a task object
        return DataAccessBase.sendSuccess(Task(**task))

    @staticmethod
    @DataAccessBase.dict_wrap
    def get_own_task(
        id: str, page_size: int, page_index: int, get_completed: bool
    ) -> DictParse:
        """Method to retrieve a multiple task based on the receiver's ID"""

        # Generate query based on whether to return sent or received documents
        incomplete = [
            {f"pending.{id}": {"$exists": True}},
            {f"incomplete.{id}": {"$exists": True}},
        ]
        query = {
            "$and": [
                {"stat_type": "task"},
                {
                    "$or": [{f"complete.{id}": {"$exists": get_completed}}]
                    if get_completed
                    else incomplete
                },
            ]
        }

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
            )
            .skip(skips)
            .limit(page_size)
        )

        # Return if the given task is not in the database
        if result is None:
            return {
                "status": "error",
                "message": "Task not found",
            }

        # Add a formatted from_user key for each task
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

            # Replace statuses with single status
            if id in i["incomplete"]:
                i["status"] = "incomplete"
                i["message"] = i["incomplete"][id]
            elif id in i["pending"]:
                i["status"] = "pending"
                i["message"] = i["pending"][id]
            elif id in i["complete"]:
                i["status"] = "complete"
                i["message"] = i["complete"][id]

            # Delete sensitive content
            del i["incomplete"]
            del i["pending"]
            del i["complete"]

            # Add formatted key
            i["formatted_from_user"] = memoize[i["from_user"]]

        # Return with a Feedback object
        return DataAccessBase.sendSuccess(result, pages=pages)

    @staticmethod
    @DataAccessBase.dict_wrap
    def get_dispatched_tasks(
        id: str, page_size: int, page_index: int
    ) -> DictParse:
        """Method to retrieve a multiple task based on the receiver's ID"""

        # Generate query based on whether to return sent or received documents
        query = {
            "$and": [
                {"stat_type": "task"},
                {"from_user": id},
            ]
        }

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
            )
            .skip(skips)
            .limit(page_size)
        )

        # Return if the given task is not in the database
        if result is None:
            return {
                "status": "error",
                "message": "Task not found",
            }

        # Add a formatted from_user key for each task
        result = list(result)

        # Return with a Feedback object
        return DataAccessBase.sendSuccess(result, pages=pages)

    @staticmethod
    @DataAccessBase.dict_wrap
    def get_upcoming_tasks() -> DictParse:
        """Method to get tasks that are upcoming"""

        # Get the current timestamp in seconds
        current_timestamp = int(time.time())

        # Search the collection based on id
        tasks = DataAccessBase.CURRENT_STATS_COL.find(
            {"reminders": {"$elemMatch": {"$lte": current_timestamp}}}
        )
        tasks = list(tasks)

        # Return if the given event is not in the database
        if tasks is None:
            return {
                "status": "error",
                "message": "No events happening right now at the moment",
            }

        # Update resulting items
        DataAccessBase.CURRENT_STATS_COL.update_many(
            {
                "reminders": {"$elemMatch": {"$lte": current_timestamp}},
                "stat_type": "task",
            },
            {"$pull": {"reminders": {"$lte": current_timestamp}}},
        )

        # Add a parsed time remaining value
        tasks_temp = []
        for item in tasks:
            item["formatted_time_remain"] = seconds_to_largest_time_unit(
                item["suspense"] - current_timestamp
            )
            tasks_temp.append(item)

        # Cast every event into an event object
        tasks = [Task(**item) for item in tasks_temp]

        # Return with a Event object
        return DataAccessBase.sendSuccess(tasks)

    @staticmethod
    @DataAccessBase.dict_wrap
    def update_task(id: str, **kwargs: Any) -> DictParse:
        """Method to delete a task"""

        # Check if the task based on its id does exist
        if DataAccessBase.CURRENT_STATS_COL.find_one({"_id": id}) is None:
            return DataAccessBase.sendError("Task does not exist")

        # Disable the changing of certain attributes
        immutable = [
            "datetime_created",
            "notify_email",
            "incomplete",
            "pending",
            "complete",
        ]
        if any(i in kwargs for i in immutable):
            return DataAccessBase.sendError(
                "Cannot change the following attributes: "
                + ", ".join(immutable)
            )

        # Update the document and return a success message
        DataAccessBase.CURRENT_STATS_COL.update_one(
            {"_id": id}, {"$set": kwargs}
        )
        return DataAccessBase.sendSuccess("Task updated")

    @staticmethod
    @DataAccessBase.dict_wrap
    def request_completion(task_id: str, user_id: str, msg: str) -> DictParse:
        """Method to handle the user's completion request"""

        # Check if the task based on its id does not exist
        task = DataAccessBase.CURRENT_STATS_COL.find_one({"_id": task_id})
        if task is None:
            return DataAccessBase.sendError("Task does not exist")

        # Check if the user is part of the task's incomplete list
        if user_id not in task["incomplete"]:
            # If the user is pending approval, send a message about that
            if user_id in task["pending"]:
                return DataAccessBase.sendError(
                    "You are pending approval for completing this task"
                )
            # If the user completed this task, send a message about that
            else:
                return DataAccessBase.sendError(
                    "You are not assigned to this task"
                )

        # Automatically approve user if requesting
        del task["incomplete"][user_id]
        if task["auto_accept_requests"]:
            task["complete"][user_id] = msg
            result_message = "Task completed"
        else:
            task["pending"][user_id] = msg
            result_message = "Request filed"

        # Update database and return message
        DataAccessBase.CURRENT_STATS_COL.replace_one({"_id": task_id}, task)
        return DataAccessBase.sendSuccess(result_message)

    @staticmethod
    @DataAccessBase.dict_wrap
    def change_status(
        task_id: str, user_id: str, msg: str, action: str
    ) -> DictParse:
        """Method to handle the placement of users to different statuses"""

        # Check if the task based on its id does not exist
        task = DataAccessBase.CURRENT_STATS_COL.find_one({"_id": task_id})
        if task is None:
            return DataAccessBase.sendError("Task does not exist")

        # Check if the user is incomplete status
        if user_id in task["incomplete"]:
            return DataAccessBase.sendError(
                "This user is in incomplete stage. You cannot do anything."
            )

        # Check if the request is to deny
        if action == "deny" and user_id in task["complete"]:
            # Move the user from complete to incomplete stage
            del task["complete"][user_id]
            task["incomplete"][user_id] = msg
            result_message = "User moved to incomplete stage"

        # Check if the request is to reject
        elif action == "reject" and user_id in task["pending"]:
            # Move the user from complete to incomplete stage
            del task["pending"][user_id]
            task["incomplete"][user_id] = msg
            result_message = "User moved to incomplete stage"

        # Check if the request is to approve
        elif action == "approve" and user_id in task["pending"]:
            # Move the user from complete to incomplete stage
            del task["pending"][user_id]
            task["complete"][user_id] = msg
            result_message = "User moved to complete stage"

        # If anything else, return an error
        else:
            return DataAccessBase.sendError("Invalid option configuration")

        # Update database and return message
        DataAccessBase.CURRENT_STATS_COL.replace_one({"_id": task_id}, task)
        return DataAccessBase.sendSuccess(result_message)

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
