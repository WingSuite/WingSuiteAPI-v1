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
        """Constructor for base pfa"""

        # Check if kwargs has the minimum arguments
        for arg in PFA.REQ_ARGS.pfa.init:
            if arg not in kwargs:
                return False

        # Save info
        self.info = DictParse(kwargs)

        # Add composited score to the object's attributes
        self.info.composite_score = self.calculate_composite()

    @staticmethod
    def get_metric_name() -> str:
        """Return metric name"""
        return "PFA"

    @staticmethod
    def get_scoring_ids() -> List:
        """Return composite score and subscore ids"""
        return ["composite_score", "pushup", "situp", "run"]

    @staticmethod
    def get_scoring_type() -> List:
        """Return composite score and subscore datatypes"""
        return ["number", "number", "number", "time"]

    @staticmethod
    def get_scoring_options() -> dict:
        """Return a list of option for the composite and subscore"""
        return {}

    @staticmethod
    def get_scoring_formatted() -> List:
        """Return composite score and subscore ids, formatted"""
        return ["Composite Score", "Push-Ups", "Sit-Ups", "1.5 Mile Run"]

    @staticmethod
    def get_scoring_domains() -> dict:
        """Return composite score and subscore ids' domain range"""
        return {
            "composite_score": [75, 100],
            "pushup": [0, 80],
            "situp": [0, 80],
            "run": [480, 900],
        }

    @staticmethod
    def get_info_ids() -> List:
        """Static method to return info ids"""
        return ["age", "gender"]

    @staticmethod
    def get_info_type() -> List:
        """Static method to return info datatypes"""
        return ["number", "selection"]

    @staticmethod
    def get_info_options() -> dict:
        """Return a list of option for infos"""
        return {"gender": ["Male", "Female"]}

    @staticmethod
    def get_info_formatted() -> List:
        """Static method to return infos, formatted"""
        return ["Age", "Gender"]

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
