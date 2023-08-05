# Imports
from config.config import config, arguments
from utils.dict_parse import DictParse
from typing import Any, List


class User:
    """User class model"""

    # Static variable declaration
    REQ_ARGS = arguments.models.user

    def __init__(self: "User", **kwargs: Any) -> None:
        """Constructor for the User class"""

        # Check if kwargs has the minimum arguments
        for arg in User.REQ_ARGS.init:
            if arg not in kwargs:
                return False

        # Save info
        self.info = DictParse(kwargs)

        # Calculate user's full name
        self.info.full_name = self.get_fullname(True)

    def get_generic_info(
        self: "User",
        includeFullName: bool = True,
        lastNameFirst: bool = True,
        other_protections: List[str] = [],
    ) -> DictParse:
        """Returns content that doesn't include any security concerns"""

        # FIlter out any secure data
        data = {
            k: v
            for k, v in self.info.items()
            if k not in config.private_info + other_protections
        }

        # Append full name information to the data based on the
        # given parameters
        if includeFullName:
            data["full_name"] = self.get_fullname(lastNameFirst)

        # Return the data
        return data

    def get_fullname(self: "User", lastNameFirst: bool) -> str:
        """Returns the user's full name"""

        # Get the user's names
        first_name = self.info.first_name
        last_name = self.info.last_name
        middle_initial = ""
        if "middle_initial" in self.info:
            middle_initial = " " + self.info.middle_initial

        # Return different styles based on given options
        if lastNameFirst:
            return f"{last_name}, {first_name}{middle_initial}"
        else:
            return f"{first_name}{middle_initial} {last_name}"

    def add_permission(self: "User", permission: str) -> bool:
        "Add new permissions to the user"

        # If the given permission is already in the permissions
        # list, return false
        if permission in self.info.permissions:
            return False

        # If not existent, append the new permissions to the list
        # and return true
        else:
            self.info.permissions.append(permission)
            return True

    def delete_permission(self: "User", permission: str) -> bool:
        "Remove permission to the user"

        # If the given permission is already in the permissions list,
        # remove and return true
        if permission in self.info["permissions"]:
            self.info.permissions.remove(permission)
            return True

        # If not existent, append the new permission to the list
        # and return true
        else:
            return False

    def add_unit(self: "User", id: str) -> bool:
        """Unit adder method"""

        # Add the ID of the unit to the user's information if the ID is not
        # in the units list
        if id not in self.info.units:
            self.info.units.append(id)

        # If not, return false
        else:
            return False

        # Return true
        return True

    def delete_unit(self: "User", id: str) -> bool:
        """Unit remover method"""

        # Remove the ID of the unit to the user's information if the ID is not
        # in the units list
        if id in self.info.units:
            self.info.units.remove(id)

        # If not, return false
        else:
            return False

        # Return true
        return True
