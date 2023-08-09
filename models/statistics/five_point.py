# Imports
from utils.dict_parse import DictParse
from config.config import arguments
from typing import Any, List


class FivePoint:
    """FivePoint model class"""

    # Static variable declaration
    REQ_ARGS = arguments.models.statistic

    def __init__(self: "FivePoint", **kwargs: Any) -> None:
        """Constructor for the FivePoint Evaluation Metric"""

        # Check if kwargs has the minimum arguments
        for arg in FivePoint.REQ_ARGS.pfa.init:
            if arg not in kwargs:
                return False

        # Save info
        self.info = DictParse(kwargs)

        # Add composited score to the object's attributes
        subscores = self.info.subscores
        self.info.composite_score = sum(subscores.values()) / len(subscores)

    @staticmethod
    def get_scoring_ids() -> List:
        """Return composite score and subscore ids"""
        return [
            "composite_score",
            "category_1",
            "category_2",
            "category_3",
            "category_4",
            "category_5",
        ]

    @staticmethod
    def get_scoring_type() -> List:
        """Return composite score and subscore datatypes"""
        return [
            "number",
            "selection",
            "selection",
            "selection",
            "selection",
            "selection",
        ]

    @staticmethod
    def get_scoring_options() -> dict:
        """Return a list of option for the composite and subscore"""
        return {
            "category_1": [0, 1, 2, 3, 4, 5],
            "category_2": [0, 1, 2, 3, 4, 5],
            "category_3": [0, 1, 2, 3, 4, 5],
            "category_4": [0, 1, 2, 3, 4, 5],
            "category_5": [0, 1, 2, 3, 4, 5],
        }

    @staticmethod
    def get_scoring_formatted() -> List:
        """Return composite score and subscore ids, formatted"""
        return [
            "Composite Score",
            "Category 1",
            "Category 2",
            "Category 3",
            "Category 4",
            "Category 5",
        ]

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
