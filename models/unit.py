# Imports
from config.config import arguments
from utils.dict_parse import DictParse


class Unit:
    """Base model unit"""

    # Static variable declaration
    REQ_ARGS = arguments.models.unit

    def __init__(self, **kwargs):
        """Constructor for base unit"""

        # Check if kwargs has the minimum arguments
        for arg in Unit.REQ_ARGS.init:
            if arg not in kwargs:
                return False

        # Save info
        self.info = DictParse(kwargs)

    def add_member(self, id):
        """
        Add a new member to the members list

        NOTE: Remember to add the unit to the user's side as well.
        """

        # Append the user to the list
        self.info.members.append(id)

        # Return true
        return True

    def removed_member(self, id):
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

    def add_child(self, id):
        """Method to add a child"""

        # Add child to the children's list if it doesn't exist
        if id not in self.info.children:
            self.info.children.append(id)

        # Return true
        return True

    def delete_child(self, id):
        """Method to delete a child"""

        # Add child to the children's list if it doesn't exist
        if id in self.info.children:
            self.info.children.remove(id)

        # Return true
        return True