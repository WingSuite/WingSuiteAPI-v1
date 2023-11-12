# Imports
from utils.dict_parse import DictParse
from .base import DataAccessBase
from config.config import config
from models.event import Event
from typing import Any
import time
import uuid


class EventAccess(DataAccessBase):
    """Class that handles event information"""

    @staticmethod
    @DataAccessBase.dict_wrap
    def create_event(
        name: str,
        unit: str,
        location: str,
        start_datetime: int,
        end_datetime: int,
        description: str,
        tag: str,
        **kwargs: Any
    ) -> DictParse:
        """Method to create an event"""

        # Prep data to be inserted
        data = {
            k: v
            for k, v in locals().items()
            if k not in ["kwargs", "args"] and k[0] != "$"
        }
        data.update(
            {k: v for k, v in locals()["kwargs"].items() if k[0] != "$"}
        )
        data["_id"] = uuid.uuid4().hex

        # Check if the tag is an authentic one
        if data["tag"] not in config.tags:
            return DataAccessBase.sendError("Tag is invalid")

        # Insert into the collection
        DataAccessBase.EVENT_COL.insert_one(data)

        # Return a statement
        return DataAccessBase.sendSuccess("Event created", id=data["_id"])

    @staticmethod
    @DataAccessBase.dict_wrap
    def get_event_by_unit_id(
        id: str, start: int = None, end: str = None
    ) -> DictParse:
        """Method to get an event by unit ID"""

        # Set query
        query = {"unit": id}

        # If start and end are provided, search between those datetimes
        if start is not None or end is not None:
            query["start_datetime"] = {"$gte": start, "$lte": end}

        # Search the collection based on id
        events = list(DataAccessBase.EVENT_COL.find(query))

        # Return if the given event is not in the database
        if len(events) == 0:
            return {
                "status": "error",
                "message": "No events found with given unit ID",
            }

        # Cast every event into an event object
        events = [Event(**item) for item in events]

        # Return with a Event object
        return DataAccessBase.sendSuccess(events)

    @staticmethod
    @DataAccessBase.dict_wrap
    def get_event_by_id(id: str) -> DictParse:
        """Method to get an event by ID"""

        # Search the collection based on id
        event = DataAccessBase.EVENT_COL.find_one({"_id": id})

        # Return if the given event is not in the database
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
        events = DataAccessBase.EVENT_COL.find({"name": {"$regex": name}})

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

    @staticmethod
    @DataAccessBase.dict_wrap
    def get_occurring_events(offset: int = 0) -> DictParse:
        """Method to get events that are currently happening right now"""

        # Get current time with offset (in minutes)
        current_time = int(time.time()) + (offset * 60)

        # Search the collection based on id
        events = DataAccessBase.EVENT_COL.find(
            {
                "start_datetime": {"$lte": current_time},
                "$or": [
                    {"heads_up_dispatched": {"$ne": True}},
                    {"heads_up_dispatched": {"$exists": False}},
                ],
            }
        )

        # Return if the given event is not in the database
        if events is None:
            return {
                "status": "error",
                "message": "No events happening right now at the moment",
            }

        # Cast every event into an event object
        events = [Event(**item) for item in events]

        # Return with a Event object
        return DataAccessBase.sendSuccess(events)

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
    def delete_event(id: str) -> DictParse:
        """Method to delete an event"""

        # Check if the event based on its id does not exist
        event = DataAccessBase.EVENT_COL.find_one({"_id": id})
        if event is None:
            return DataAccessBase.sendError("Event does not exist")

        # Delete the document and return a success message
        DataAccessBase.EVENT_COL.delete_one({"_id": id})
        return DataAccessBase.sendSuccess("Event deleted", id=id)
