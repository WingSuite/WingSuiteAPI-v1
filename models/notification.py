# Imports
from utils.dict_parse import DictParse
from config.config import arguments
from typing import Any


class Notification:
    """Feedback model class"""

    # Static variable declaration
    REQ_ARGS = arguments.models

    def __init__(self: "Notification", **kwargs: Any) -> None:
        """Constructor for base unit"""

        # Check if kwargs has the minimum arguments
        for arg in Notification.REQ_ARGS.notification.init:
            if arg not in kwargs:
                return False

        # Save info
        self.info = DictParse(kwargs)
