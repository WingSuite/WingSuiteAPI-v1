# Imports
from config.config import arguments
from utils.dict_parse import DictParse


class Stats:
    """Stats class model"""
    """When created make sure to create an id type specefic to user"""

    # Static variable declaration
    REQ_ARGS = arguments.models.stats

    def __init__(self, **kwargs):
        """Constructor for the Stats class"""

        # Check if kwargs has the minimum arguments
        for arg in Stats.REQ_ARGS.init:
            if arg not in kwargs:
                return False

        # Save info
        self.info = DictParse(kwargs)

    def update_type(self, type, id):
        """Stats adder method"""

        # If "type"(PFA, Feedback, WK) is not in the instance then add it
        if type not in self.info:
            self.info.type = [id]

        # If not, check if it exists
        else:
            if id not in self.info.type:
                # If not, append to the end of the list
                self.info.type.append(id)
                # Return true
                return True
            else:
                return False

    def delete_type(self, type, id):
        "Remove type from the stats"

        # If the given type is already in the type list,
        # remove and return true
        if id in self.info.type[type]:
            self.info.type.remove(id)
            return True

        # If not existent, append the new permission to the list
        # and return true
        else:
            return False
