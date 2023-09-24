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
            "Announcement": "bg-[#D3D3D3]",
            "INFO": "bg-[#ADD8E6]",
            "Community": "bg-[#90EE90]",
            "Morale": "bg-[#FFFF99]",
            "Volunteer": "bg-[#FFD700]",
            "Award": "bg-[#FFA500]",
            "Scholarship": "bg-[#FF8C00]",
            "PT": "bg-[#20B2AA]",
            "PDT": "bg-[#3CB371]",
            "LLAB": "bg-[#4682B4]",
            "WK": "bg-[#87CEEB]",
            "Cadre": "bg-[#FFCCCC]",
            "TASK": "bg-[#FF9999]",
            "ACTION": "bg-[#FF6666]",
            "URGENT": "bg-[#FF0000]",
        })
