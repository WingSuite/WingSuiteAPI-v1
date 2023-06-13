# Import the test blueprint
from endpoints.base import (
    permissions_required,
    param_check,
    serverErrorResponse,
    ARGS
)
from . import (
    create_unit,
    update_unit,
    get_unit_info,
    delete_unit,
    add_members,
    delete_members
)
from database.unit import UnitAccess
from flask import request


@create_unit.route("/create_unit/", methods=["POST"])
@permissions_required(["user.create_unit"])
@param_check(ARGS.unit.create_unit)
def create_unit_endpoint():
    """Method to handle the creation of new units"""

    # Try to parse information
    try:
        # Parse information from the call's body
        data = request.get_json()

        # Add the unit to the database
        result = UnitAccess.create_unit(**data)

        # Return response data
        return result, (200 if result.status == "success" else 400)

    # Error handling
    except Exception as e:
        return serverErrorResponse(str(e))