# Imports
from utils.dict_parse import DictParse
from config.config import config
from .base import DataAccessBase
from typing import Any, List
from database.user import UserAccess
from models.unit import Unit
from models.user import User
import uuid
import math


class UnitAccess(DataAccessBase):
    """Class that handles unit information"""

    @staticmethod
    @DataAccessBase.dict_wrap
    def create_unit(
        name: str,
        unit_type: str,
        parent: str,
        children: list,
        officers: list,
        members: list,
        **kwargs: Any
    ) -> DictParse:
        """Method to create a new unit"""

        # If the inputted type is an approved type, return with an
        # error message
        if unit_type not in config.unit_types:
            return DataAccessBase.sendError(
                "Unit type is not a valid type. \nSelect from: "
                + ", ".join(config.unit_types)
            )

        # Prep data to be inserted
        data = {
            k: v for k, v in locals().items() if k not in ["kwargs", "args"]
        }
        data.update(locals()["kwargs"])
        data["_id"] = uuid.uuid4().hex
        data["frontpage"] = ""
        data["events"] = []

        # Insert into the collection
        DataAccessBase.UNIT_COL.insert_one(data)

        # Add the inputted officers and members into the unit
        for item in officers + members:
            # Get the user object based on iterated item
            user = UserAccess.get_user(item).message

            # Continue if the iterated user is not a User
            if type(user) != User:
                continue

            # Add the officer to the unit
            user.add_unit(data["_id"])

            # Update officer
            UserAccess.update_user(item, **user.info)

        # Iterate through the children's list and update pointers
        for item in children:
            # Get the unit object based on the iterated item
            unit = UnitAccess.get_unit(item).message

            # Continue if the iterated unit is not a Unit
            if type(user) != Unit:
                continue

            # Update their parent pointer
            unit.info.parent = data["_id"]

            # Update child unit
            UnitAccess.update_unit(item, **unit.info)

        # Update the unit's parent node if one is provided
        if parent != "":
            # Get the unit object based on the iterated item
            unit = UnitAccess.get_unit(parent).message

            # Update children info
            unit.add_child(data["_id"])

            # Update child unit
            UnitAccess.update_unit(unit.info._id, **unit.info)

        # Send success message after successful operation
        return DataAccessBase.sendSuccess("Unit added")

    @staticmethod
    @DataAccessBase.dict_wrap
    def delete_unit(id: str) -> DictParse:
        """Method to delete a unit"""

        # Check if the unit based on its id does not exist
        unit = DataAccessBase.UNIT_COL.find_one({"_id": id})
        if unit is None:
            return DataAccessBase.sendError("Unit does not exist")

        # Get a Unit object representation
        unit = Unit(**unit)

        # Update the information from the members and offices of the unit
        for item in unit.info.officers + unit.info.members:
            # Get the user object based on iterated item
            user = UserAccess.get_user(item).message

            # Continue if the iterated user is not a User
            if type(user) != User:
                continue

            # Add the officer to the unit
            user.delete_unit(id)

            # Update officer
            UserAccess.update_user(item, **user.info)

        # Iterate through the children's list and update pointers
        for item in unit.info.children:
            # Get the unit object based on the iterated item
            iter_unit = UnitAccess.get_unit(item).message

            # Continue if the iterated unit is not a Unit
            if type(iter_unit) != Unit:
                continue

            # Update their parent pointer
            iter_unit.info.parent = ""

            # Update child unit
            UnitAccess.update_unit(item, **iter_unit.info)

        # Update the unit's parent node if one is provided
        if unit.info.parent != "":
            # Get the unit object based on the iterated item
            iter_unit = UnitAccess.get_unit(unit.info.parent).message

            # Update children info
            iter_unit.delete_child(id)

            # Update child unit
            UnitAccess.update_unit(iter_unit.info._id, **iter_unit.info)

        # Delete the document and return a success message
        DataAccessBase.UNIT_COL.delete_one({"_id": id})
        return DataAccessBase.sendSuccess("Unit deleted")

    @staticmethod
    @DataAccessBase.dict_wrap
    def update_unit(id: str, **kwargs: Any) -> DictParse:
        """Method to delete a unit"""

        # Check if the unit based on its id does exist
        if DataAccessBase.UNIT_COL.find_one({"_id": id}) is None:
            return DataAccessBase.sendError("Unit does not exist")

        # If the kwargs include the changing of a unit type, check for its
        # validity
        if (
            "unit_type" in kwargs
            and kwargs["unit_type"] not in config.unit_types
        ):
            return DataAccessBase.sendError(
                "Unit type is not a valid type. \nSelect from: "
                + ", ".join(config.unit_types)
            )

        # Update the document and return a success message
        DataAccessBase.UNIT_COL.update_one({"_id": id}, {"$set": kwargs})
        return DataAccessBase.sendSuccess("Unit updated")

    @staticmethod
    @DataAccessBase.dict_wrap
    def get_unit(id: str) -> DictParse:
        """Method to get a unit by ID"""

        # Search the collection based on id
        unit = DataAccessBase.UNIT_COL.find_one({"_id": id})

        # Return if the given unit is not in the database
        if unit is None:
            return {
                "status": "error",
                "message": "Unit not found",
            }

        # Return with a Unit object
        return DataAccessBase.sendSuccess(Unit(**unit))

    @staticmethod
    @DataAccessBase.dict_wrap
    def get_all_units(page_size: int, page_index: int) -> DictParse:
        """Get a list of units based on the page size and the index"""

        # Check if the page_size or page_index is negative
        if page_size <= 0 or page_index < 0:
            return DataAccessBase.sendError("Invalid pagination size or index")

        # Get the total amount of pages based on pagination size
        pages = math.ceil(
            DataAccessBase.UNIT_COL.count_documents({}) / page_size
        )

        # Check if the page_index is outside the page range
        if page_index >= pages:
            return DataAccessBase.sendError("Pagination index out of bounds")

        # Calculate skip value
        skips = page_size * (page_index)

        # Get the list of units based on the given page size and index
        results = DataAccessBase.UNIT_COL.find().skip(skips).limit(page_size)

        # Turn each document into a Unit object
        results = [Unit(**item) for item in list(results)]

        # Return the results and the page size
        return DataAccessBase.sendSuccess(results, pages=pages)

    @staticmethod
    @DataAccessBase.dict_wrap
    def get_units_below(
        user_units: List[str], tracked: List[str] = []
    ) -> DictParse:
        """Method to get the units below the user's units"""

        # Iterate through the user's units and get their event information
        tracked = set(tracked)
        units = set()
        stack = list(user_units)
        while stack:
            # Get the top of the stack
            node = stack.pop()

            # Set ptr on start of given ID
            ptr = UnitAccess.get_unit(node).message.info

            # Skip if the pointer ID has been tracked
            if ptr._id in tracked:
                continue
            tracked.add(ptr._id)

            # Add child ID to tracker
            units.add(ptr._id)

            # Pass if the length of children is 1
            if len(ptr.children) > 2:
                pass

            # Iterate through each children and append to stack
            for child in reversed(ptr.children):
                # Append to stack if the child node is not in the stack
                if child not in units:
                    stack.append(child)

        # Process unit information
        units = [UnitAccess.get_unit(unit).message.info for unit in units]
        units = sorted(
            units,
            key=lambda x: (
                config.unit_types.index(x["unit_type"]),
                x["name"],
            ),
            reverse=True
        )

        # Return the units
        return DataAccessBase.sendSuccess(units)

    @staticmethod
    @DataAccessBase.dict_wrap
    def get_units_above(user_units: List[str]) -> DictParse:
        """Method to get the units below the user's units"""

        # Iterate through the user's units and get their event information
        units = set()
        for root in user_units:
            # Set ptr on start of given ID
            ptr = UnitAccess.get_unit(root)

            # Iterate through the stack to reverse upwards
            while ptr.status == "success":
                # Add iterate unit id to the units set
                units.add(ptr.message.info._id)

                # Iterate upwards
                ptr = UnitAccess.get_unit(ptr.message.info.parent)

        # Process unit information
        units = [UnitAccess.get_unit(unit).message.info for unit in units]

        # Return the units
        return DataAccessBase.sendSuccess(units)
