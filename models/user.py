# Imports
from utils.dict_parse import DictParse
from config.config import config


class User:
    """User class model"""

    # Static variable declaration
    REQ_ARGS = config.neededArguments.Users

    def __init__(self, **kwargs):
        """Constructor for the User class"""

        # Check if kwargs has the minimum arguments
        for arg in User.REQ_ARGS.init:
            if arg not in kwargs:
                return False

        # Save info
        self.info = DictParse(kwargs)

    def get_generic_info(self, includeFullName=True, lastNameFirst=True):
        """Returns content that doesn't include any security concerns"""

        # FIlter out any secure data
        data = {
            k: v for k, v in self.info.items() if k not in config.privateInfo
        }

        # Append full name information to the data based on the
        # given parameters
        if includeFullName:
            data["full_name"] = self.get_fullname(lastNameFirst)

        # Return the data
        return data

    def get_fullname(self, lastNameFirst):
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

    def add_permission(self, permission):
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

    def delete_permission(self, permission):
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

    def add_unit(self, id):
        """Unit adder method"""

        # If "units" is not in the instance's metadata, add it for the user
        if "units" not in self.info:
            self.info.units = [id]

        # If not, append to the end of the list
        else:
            self.info.units.append(id)
