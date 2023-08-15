# Imports
from utils.dict_parse import DictParse
from config.config import arguments
from typing import Any


class Feedback:
    """Feedback model class"""

    # Static variable declaration
    REQ_ARGS = arguments.models.statistic

    def __init__(self: "Feedback", **kwargs: Any) -> None:
        """Constructor for base unit"""

        # Check if kwargs has the minimum arguments
        for arg in Feedback.REQ_ARGS.feedback.init:
            if arg not in kwargs:
                return False

        # Save info
        self.info = DictParse(kwargs)
