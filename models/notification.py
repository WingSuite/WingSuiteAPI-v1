# Imports
from utils.dict_parse import DictParse
from config.config import arguments
from typing import Any


class Notification:
    """Feedback model class"""

    # Static variable declaration
    REQ_ARGS = arguments.models

    def __init__(self: "Notification", **kwargs: Any) -> None:
        """Constructor for base unit"""

        # Check if kwargs has the minimum arguments
        for arg in Notification.REQ_ARGS.notification.init:
            if arg not in kwargs:
                return False

        # Save info
        self.info = DictParse(kwargs)

    @staticmethod
    def get_available_tags() -> DictParse:
        """Method to return the available tags for the notification"""
        return DictParse({
            "Announcement": "#D3D3D3",
            "INFO": "#ADD8E6",
            "Community": "#90EE90",
            "Volunteer": "#FFD700",
            "Morale": "#FF70FF",
            "Award": "#FFA500",
            "Scholarship": "#FF8C00",
            "WK": "#82FFE2",
            "PT": "#75E1FF",
            "LLAB": "#9DD1FC",
            "PDT": "#52F29A",
            "Event": "#52E7F2",
            "Cadre": "#FFCCCC",
            "TASK": "#FF9999",
            "ACTION": "#FF6666",
            "URGENT": "#FF0000",
            "<< ARCHIVED >>": "#A3A3A3",
        })
