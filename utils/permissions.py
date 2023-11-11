# Imports
from database.unit import UnitAccess
from typing import List


def isOfficerFromAbove(units: List[dict], user: str) -> str:
    """Check if the given user is an officer from a superior unit"""

    # Transform units to a list object if not provided as a list
    if type(units) is not list:
        units = [units]

    # Get the list of officers from superior units of the given units
    superior_officers = [
        i.officers for i in UnitAccess.get_units_above(units).message
    ]
    superior_officers = set(
        element for sublist in superior_officers for element in sublist
    )

    # Return true if the user's ID is in the list
    return user in superior_officers
