# Imports
from utils.dict_parse import DictParse
from config.config import arguments
from typing import Any


class Unit:
    """Base model unit"""

    # Static variable declaration
    REQ_ARGS = arguments.models.unit

    def __init__(self: "Unit", **kwargs: Any) -> None:
        """Constructor for base unit"""

        # Check if kwargs has the minimum arguments
        for arg in Unit.REQ_ARGS.init:
            if arg not in kwargs:
                return False

        # Save info
        self.info = DictParse(kwargs)

    def add_member(self: "Unit", id: str) -> bool:
        """
        Add a new member to the members list

        NOTE: Remember to add the unit to the user's side as well.
        """

        # Append the user to the list
        self.info.members.append(id)

        # Return true
        return True

    def delete_member(self: "Unit", id: str) -> bool:
        """
        Remove a member to the members list

        NOTE: Remember to add the unit to the user's side as well.
        """

        # Try to remove
        try:
            # Append the user to the list
            self.info.members.remove(id)

        # Catch error
        except Exception:
            # Return false
            return False

        # Return true
        return True

    def add_officer(self: "Unit", id: str) -> bool:
        """
        Add a new officer to the officers list

        NOTE: Remember to add the unit to the user's side as well.
        """

        # Append the user to the list
        self.info.officers.append(id)

        # Return true
        return True

    def delete_officer(self: "Unit", id: str) -> bool:
        """
        Remove a officer to the officers list

        NOTE: Remember to add the unit to the user's side as well.
        """

        # Try to remove
        try:
            # Append the user to the list
            self.info.officers.remove(id)

        # Catch error
        except Exception:
            # Return false
            return False

        # Return true
        return True

    def add_child(self: "Unit", id: str) -> bool:
        """Method to add a child"""

        # Add child to the children's list if it doesn't exist
        if id not in self.info.children:
            self.info.children.append(id)

        # Return true
        return True

    def delete_child(self: "Unit", id: str) -> bool:
        """Method to delete a child"""

        # Add child to the children's list if it doesn't exist
        if id in self.info.children:
            self.info.children.remove(id)

        # Return true
        return True
