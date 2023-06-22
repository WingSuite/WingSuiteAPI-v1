# Imports
from utils.dict_parse import DictParse
from config.config import arguments
from datetime import datetime
from typing import Any


class Event:
    """Event model class"""

    # Static variable declaration
    REQ_ARGS = arguments.models.event

    def __init__(self: "Event", **kwargs: Any) -> None:
        """Constructor for base unit"""

        # Check if kwargs has the minimum arguments
        for arg in Event.REQ_ARGS.init:
            if arg not in kwargs:
                return False

        # Save info
        self.info = DictParse(kwargs)

    def get_formatted_datetime(self: "Event") -> str:
        """Method to return the formatted datetime"""
        return datetime.fromtimestamp(self.info.datetime).strftime(
            "%d %m %Y, %H:%M"
        )
