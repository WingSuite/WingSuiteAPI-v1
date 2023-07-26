# Imports
from utils.dict_parse import DictParse
from config.config import arguments
from typing import Any, List


class Warrior:
    """Warrior model class"""

    # Static variable declaration
    REQ_ARGS = arguments.models.statistic

    def __init__(self: "Warrior", **kwargs: Any) -> None:
        """Constructor for base unit"""

        # Check if kwargs has the minimum arguments
        for arg in Warrior.REQ_ARGS.warrior.init:
            if arg not in kwargs:
                return False

        # Save info
        self.info = DictParse(kwargs)

    @staticmethod
    def get_metrics() -> List:
        """
        Static method to return composite score and subscore ids with datatype
        """
        return {"composite_score": "number"}

    @staticmethod
    def get_metrics_formatted() -> List:
        """
        Static method to return composite score and subscore ids, formatted
        """
        return ["Composite Score"]
