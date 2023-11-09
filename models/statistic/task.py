# Imports
from utils.dict_parse import DictParse
from config.config import arguments
from typing import Any


class Task:
    """Task model class"""

    # Static variable declaration
    REQ_ARGS = arguments.models.statistic

    def __init__(self: "Task", **kwargs: Any) -> None:
        """Constructor for base task"""

        # Check if kwargs has the minimum arguments
        for arg in Task.REQ_ARGS.task.init:
            if arg not in kwargs:
                return False

        # Save info
        self.info = DictParse(kwargs)
