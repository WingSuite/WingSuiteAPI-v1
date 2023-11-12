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

        # Calculate composite score
        denominator = self.info.subscores.total_points
        if (denominator == 0):
            denominator = 1
        self.info.composite_score = round(
            (
                self.info.subscores.points_earned
                / denominator
            )
            * 100,
            2,
        )

    @staticmethod
    def get_metric_name() -> str:
        """Return metric name"""
        return "Warrior Knowledge"

    @staticmethod
    def get_scoring_ids() -> List:
        """Return composite score and subscore ids"""
        return ["composite_score", "points_earned", "total_points"]

    @staticmethod
    def get_scoring_type() -> List:
        """Return composite score and subscore datatypes"""
        return ["number", "number", "number"]

    @staticmethod
    def get_scoring_options() -> dict:
        """Return a list of option for the composite and subscore"""
        return {}

    @staticmethod
    def get_scoring_formatted() -> List:
        """Return composite score and subscore ids, formatted"""
        return ["Composite Score", "Points Earned", "Total Points"]

    @staticmethod
    def get_scoring_domains() -> dict:
        """Return composite score and subscore ids' domain range"""
        return {"composite_score": [0, 100]}

    @staticmethod
    def get_info_ids() -> List:
        """Static method to return info ids"""
        return []

    @staticmethod
    def get_info_type() -> List:
        """Static method to return info datatypes"""
        return []

    @staticmethod
    def get_info_options() -> dict:
        """Return a list of option for infos"""
        return {}

    @staticmethod
    def get_info_formatted() -> List:
        """Static method to return infos, formatted"""
        return []
