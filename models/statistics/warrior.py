# Imports
from utils.dict_parse import DictParse
from config.config import arguments
from typing import Any


class Warrior:
    """Warrior model class"""

    # Static variable declaration
    REQ_ARGS = arguments.models.statistics

    def __init__(self: "Warrior", **kwargs: Any) -> None:
        """Constructor for base unit"""

        # Check if kwargs has the minimum arguments
        for arg in Warrior.REQ_ARGS.warrior.init:
            if arg not in kwargs:
                return False

        # Save info
        self.info = DictParse(kwargs)
