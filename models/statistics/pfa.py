# Imports
from utils.pfa.calculator import calculate_pfa
from utils.dict_parse import DictParse
from config.config import arguments
from typing import Any, List


class PFA:
    """Pfa model class"""

    # Static variable declaration
    REQ_ARGS = arguments.models.statistic

    def __init__(self: "PFA", **kwargs: Any) -> None:
        """Constructor for base unit"""

        # Check if kwargs has the minimum arguments
        for arg in PFA.REQ_ARGS.pfa.init:
            if arg not in kwargs:
                return False

        # Save info
        self.info = DictParse(kwargs)

        # Add composited score to the object's attributes
        self.info.composite_score = self.calculate_composite()

    @staticmethod
    def get_metrics() -> List:
        """
        Static method to return composite score and subscore ids with datatype
        """
        return {
            "composite_score": "number",
            "pushup": "number",
            "situp": "number",
            "run": "time",
        }

    @staticmethod
    def get_metrics_formatted() -> List:
        """
        Static method to return composite score and subscore ids, formatted
        """
        return ["Composite Score", "Push-Ups", "Sit-Ups", "1.5 Mile Run"]

    def calculate_composite(self: "PFA") -> float:
        """Method to calculate the composite score from raw subscores"""

        # Return composite score
        return calculate_pfa(
            self.info.info.gender,
            self.info.info.age,
            self.info.subscores.pushup,
            self.info.subscores.situp,
            self.info.subscores.run,
        )
