# Imports
from utils.dict_parse import DictParse
from .base import DataAccessBase
from models.event import Event
from typing import Any
import uuid


class EventAccess(DataAccessBase):
    """Class that handles event information"""

    @staticmethod
    @DataAccessBase.dict_wrap
    def create_event(
        name: str,
        unit: str,
        location: str,
        datetime: int,
        description: str,
        **kwargs: Any
    ) -> DictParse:
        """Method to create an event"""

        # Prep data to be inserted
        data = {
            k: v for k, v in locals().items() if k not in ["kwargs", "args"]
        }
        data.update(locals()["kwargs"])
        data["_id"] = uuid.uuid4().hex

        # Insert into the collection
        DataAccessBase.EVENT_COL.insert_one(data)

        # Return a statement
        return DataAccessBase.sendSuccess("Event created", id=data["_id"])

    @staticmethod
    @DataAccessBase.dict_wrap
    def delete_event(id: str) -> DictParse:
        """Method to delete an event"""

        # Check if the event based on its id does not exist
        event = DataAccessBase.EVENT_COL.find_one({"_id": id})
        if event is None:
            return DataAccessBase.sendError("Event does not exist")

        # Delete the document and return a success message
        DataAccessBase.EVENT_COL.delete_one({"_id": id})
        return DataAccessBase.sendSuccess("Event deleted", id=id)

    @staticmethod
    @DataAccessBase.dict_wrap
    def update_event(id: str, **kwargs: Any) -> DictParse:
        """Method to delete a event"""

        # Check if the event based on its id does exist
        if DataAccessBase.EVENT_COL.find_one({"_id": id}) is None:
            return DataAccessBase.sendError("Event does not exist")

        # Update the document and return a success message
        DataAccessBase.EVENT_COL.update_one({"_id": id}, {"$set": kwargs})
        return DataAccessBase.sendSuccess("Event updated")

    @staticmethod
    @DataAccessBase.dict_wrap
    def get_event_by_id(id: str) -> DictParse:
        """Method to get an event by ID"""

        # Search the collection based on id
        event = DataAccessBase.EVENT_COL.find_one({"_id": id})

        # Return if the given ueventnit is not in the database
        if event is None:
            return {
                "status": "error",
                "message": "Event not found",
            }

        # Return with a Event object
        return DataAccessBase.sendSuccess(Event(**event))

    @staticmethod
    @DataAccessBase.dict_wrap
    def get_event_by_name(name: str) -> DictParse:
        """Method to get an event by name"""

        # Search the collection based on id
        events = DataAccessBase.EVENT_COL.find({'name': {'$regex': name}})

        # Return if the given event is not in the database
        if events is None:
            return {
                "status": "error",
                "message": "Event not found",
            }

        # Process a list of Event objects
        results = []
        for item in events:
            results.append(Event(**item))

        # Return with a list of Event objects
        return DataAccessBase.sendSuccess(results)
