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
    def get_metric_name() -> str:
        """Return metric name"""
        return "Five Point Evaluation"

    @staticmethod
    def get_scoring_ids() -> List:
        """Return composite score and subscore ids"""
        return [
            "composite_score",
            "professionalism",
            "receptiveness",
            "team_build",
            "communication",
            "performance",
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
            "professionalism": [0, 1, 2, 3, 4, 5],
            "receptiveness": [0, 1, 2, 3, 4, 5],
            "team_build": [0, 1, 2, 3, 4, 5],
            "communication": [0, 1, 2, 3, 4, 5],
            "performance": [0, 1, 2, 3, 4, 5],
        }

    @staticmethod
    def get_scoring_formatted() -> List:
        """Return composite score and subscore ids, formatted"""
        return [
            "Composite Score",
            "Professionalism",
            "Receptiveness to Training",
            "Team-Building",
            "Effective Communication",
            "PMT Performance",
        ]

    @staticmethod
    def get_scoring_domains() -> dict:
        """Return composite score and subscore ids' domain range"""
        return {
            "composite_score": [0, 5],
            "professionalism": [0, 5],
            "receptiveness": [0, 5],
            "team_build": [0, 5],
            "communication": [0, 5],
            "performance": [0, 5],
        }

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
