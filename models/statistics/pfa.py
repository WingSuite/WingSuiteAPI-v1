# Imports
from utils.dict_parse import DictParse
from config.config import arguments
from typing import Any


class Pfa:
    """Pfa model class"""

    # Static variable declaration
    REQ_ARGS = arguments.models.statistics

    def __init__(self: "Pfa", **kwargs: Any) -> None:
        """Constructor for base unit"""

        # Check if kwargs has the minimum arguments
        for arg in Pfa.REQ_ARGS.pfa.init:
            if arg not in kwargs:
                return False

        # Save info
        self.info = DictParse(kwargs)
