# Imports
from utils.dict_parse import DictParse
from database.base import DataAccessBase
from database.user import UserAccess
from database.unit import UnitAccess
from config.config import config
from models.notification import Notification
from typing import Any
import uuid
import time


class NotificationAccess(DataAccessBase):
    """Class that handles notification information"""

    @staticmethod
    @DataAccessBase.dict_wrap
    def create_notification(
        name: str, unit: str, notification: str, author: str, **kwargs: Any
    ) -> DictParse:
        """Method to create a notification"""

        # Prep data to be inserted
        data = {
            k: v for k, v in locals().items() if k not in ["kwargs", "args"]
        }
        data.update(
            {k: v for k, v in locals()["kwargs"].items() if k[0] != "$"}
        )
        data["_id"] = uuid.uuid4().hex
        data["created_datetime"] = int(time.time())

        # Throw error if the tag is one of the available keys
        if data["tag"] not in config.tags:
            return DataAccessBase.sendError(
                f"{data['tag']} is not an available tag"
            )

        # Insert into the collection
        DataAccessBase.NOTIFICATION_COL.insert_one(data)

        # Return a statement
        return DataAccessBase.sendSuccess("Notification created")

    @staticmethod
    @DataAccessBase.dict_wrap
    def delete_notification(id: str) -> DictParse:
        """Method to delete an notification"""

        # Check if the notification based on its id does not exist
        notification = DataAccessBase.NOTIFICATION_COL.find_one({"_id": id})
        if notification is None:
            return DataAccessBase.sendError("Notification does not exist")

        # Delete the document and return a success message
        DataAccessBase.NOTIFICATION_COL.delete_one({"_id": id})
        return DataAccessBase.sendSuccess("Notification deleted")

    @staticmethod
    @DataAccessBase.dict_wrap
    def update_notification(id: str, **kwargs: Any) -> DictParse:
        """Method to delete a notification"""

        # Check if the notification based on its id does exist
        if DataAccessBase.NOTIFICATION_COL.find_one({"_id": id}) is None:
            return DataAccessBase.sendError("Notification does not exist")

        # Check if the given tag value is a proper tag
        if "tag" in kwargs:
            if kwargs["tag"] not in config.tags:
                return DataAccessBase.sendError(
                    f"{kwargs['tag']} is not an available tag"
                )

        # Update the document and return a success message
        DataAccessBase.NOTIFICATION_COL.update_one(
            {"_id": id}, {"$set": kwargs}
        )
        return DataAccessBase.sendSuccess("Notification updated")

    @staticmethod
    @DataAccessBase.dict_wrap
    def get_notification(id: str) -> DictParse:
        """Method to retrieve a single notification based on ID"""

        # Search the collection based on id
        notification = DataAccessBase.NOTIFICATION_COL.find_one({"_id": id})

        # Return if the given notification is not in the database
        if notification is None:
            return {
                "status": "error",
                "message": "Notification not found",
            }

        # Return with a Notification object
        return DataAccessBase.sendSuccess(Notification(**notification))

    @staticmethod
    @DataAccessBase.dict_wrap
    def get_notification_by_unit_id(
        id: str, start: int = None, end: str = None
    ) -> DictParse:
        """Method to get an notification by unit ID"""

        # Set query
        query = {"unit": id}

        # If start and end are provided, search between those datetimes
        if start is not None or end is not None:
            query["created_datetime"] = {"$gte": start, "$lte": end}

        # Search the collection based on id
        notifications = list(DataAccessBase.NOTIFICATION_COL.find(query))

        # Return if the given notification is not in the database
        if len(notifications) == 0:
            return {
                "status": "error",
                "message": "No notifications found with given unit ID",
            }

        # Format the notifications for better readability
        author_memoize = DictParse({})
        unit_memoize = DictParse({})
        for idx, i in enumerate(notifications):
            # Get Notification representation of the iteration
            item = Notification(**i).info

            # Add author id if the iterated item's author is not memoized
            if item.author not in author_memoize:
                # Add author's formatted name to the memoization
                author = UserAccess.get_user(
                    item.author, check_former=True
                ).message
                author_memoize[item.author] = author.get_fullname(
                    lastNameFirst=True, with_rank=True
                )

            # Add unit id if the iterated 8nit is not memoized
            if item.unit not in unit_memoize:
                # Add unit's formatted name to the memoization
                unit = UnitAccess.get_unit(item.unit).message.info
                unit_memoize[item.unit] = unit.name

            # Add formatted information to the notifications
            i["formatted_author"] = author_memoize[item.author]
            i["formatted_unit"] = unit_memoize[item.unit]

            # # Cast iterated item to model version
            notifications[idx] = Notification(**i)

        # Return with a Notification object
        return DataAccessBase.sendSuccess(notifications)
