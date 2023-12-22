# Imports
from endpoints.base import (
    success_response,
    client_error_response,
    is_root,
    permissions_required,
    param_check,
    error_handler,
    ARGS,
)
from . import (
    create_unit,
    add_members,
    add_officers,
    update_unit,
    update_frontpage,
    update_communication_settings,
    get_unit_info,
    get_unit_types,
    get_all_units,
    get_all_officers,
    get_specified_personnel,
    get_all_members,
    is_superior_officer,
    get_all_five_point_data,
    get_all_pfa_data,
    get_all_warrior_data,
    delete_unit,
    delete_members,
    delete_officers,
)
from utils.communications.email import send_email
from utils.permissions import isOfficerFromAbove
from utils.html import read_html_file
from config.config import config
from flask_jwt_extended import jwt_required
from flask import request
from database.statistic.five_point import FivePointAccess
from database.statistic.warrior import WarriorAccess
from database.statistic.pfa import PFAAccess
from database.unit import UnitAccess
from database.user import UserAccess
from urllib.parse import quote


def _update_personnel_helper(id, users, operation, participation):
    """Helper function to update personnel for a unit"""

    # Get the vocab based on the operation
    past_tense = "added" if operation == "add" else "deleted"
    ion_word = "addition" if operation == "add" else "deletion"

    # Get the unit object
    unit = UnitAccess.get_unit(id)

    # If content is not in result of getting the unit, return the
    # error message
    if unit.status == "error":
        return unit, 400

    # Get the content from the unit fetch
    unit = unit.message

    # Iterate through the list of members
    results = {}
    for user in users:
        # Get the user object of the iterated person
        user_obj = UserAccess.get_user(user)

        # If the user object query results an error, track it and continue
        if user_obj.status == "error":
            results[user] = "User not found"
            continue

        # Extract user object
        user_obj = user_obj.message

        # Calculate the recipient's appropriate name
        to_user_name = (
            user_obj.info.rank + " " + user_obj.info.full_name
            if "rank" in user_obj.info
            else user_obj.info.first_name
        )

        # Do an add operation if operation is "add"
        if operation == "add":
            res = user_obj.add_unit(id)
            if res:
                if participation == "member":
                    unit.add_member(user)
                elif participation == "officer":
                    unit.add_officer(user)

        # Do a delete operation if operation is "delete"
        elif operation == "delete":
            res = None
            if participation == "member":
                res = unit.delete_member(user)
            elif participation == "officer":
                res = unit.delete_officer(user)
            if res:
                user_obj.delete_unit(id)

        # Update user
        UserAccess.update_user(user_obj.info._id, **user_obj.info)

        # Track result
        results[user] = (
            f"User {past_tense}"
            if res
            else f"User already {past_tense} as an officer or member"
        )

        # Send added email if the user was successfully added
        if operation == "add" and res:
            # Get feedback HTML content
            content = read_html_file(
                "unit.added",
                to_user=to_user_name,
                unit_name=unit.info.name,
                unit_link=f"{config.wingsuite_dashboard_link}/unit/"
                + f"{quote(unit.info.name)}/frontpage",
            )

            # Send an email with the HTML content
            send_email(
                receiver=user_obj.info.email,
                subject=f"Added to {unit.info.name}",
                content=content,
                emoji=config.message_emoji.unit.added,
            )

        # Send added email if the user was successfully added
        elif operation == "delete" and res:
            # Get feedback HTML content
            content = read_html_file(
                "unit.kicked", to_user=to_user_name, unit_name=unit.info.name
            )

            # Send an email with the HTML content
            send_email(
                receiver=user_obj.info.email,
                subject=f"Kicked from {unit.info.name}",
                content=content,
                emoji=config.message_emoji.unit.kicked,
            )

    # Push unit changes
    UnitAccess.update_unit(id, **unit.info)

    # Make the message
    message = {
        "status": "success",
        "message": f"{participation.capitalize()} {ion_word} have been applied"
        + f" to {unit.info.name}. Refer to results for what has been "
        + "applied",
        "results": results,
    }

    # Return
    return message, 200


def _handle_error(unit_result, unit_id):
    """Function help handle errors when parsing over unit trees"""

    # Return error if the result is error
    if unit_result.status == "error":
        return client_error_response(
            f"Error occurred when processing unit: {unit_id}"
        )

    # Return nothing is all is good
    return None


#
#   CREATE OPERATIONS
#   region
#


@create_unit.route("/create_unit/", methods=["POST"])
@permissions_required(["unit.create_unit"])
@param_check(ARGS.unit.create_unit)
@error_handler
def create_unit_endpoint(**kwargs):
    """Method to handle the creation of a new unit"""

    # Parse information from the call's body
    data = request.get_json()

    # Add the unit to the database
    result = UnitAccess.create_unit(**data)

    # Return response data
    return result, (200 if result.status == "success" else 400)


@add_members.route("/add_members/", methods=["POST"])
@is_root
@permissions_required(["unit.add_members"])
@param_check(ARGS.unit.add_members)
@error_handler
def add_members_endpoint(**kwargs):
    """Method to add a new members to the unit"""

    # Parse information from the call's body
    data = request.get_json()

    # Get the unit object of the target unit and return if error
    unit = UnitAccess.get_unit(data["id"])
    if unit.status == "error":
        return unit, 400
    unit = unit.message.info

    # Check if the user is an officer of a superior unit
    is_superior_officer = isOfficerFromAbove(data["id"], kwargs["id"])

    # Check if the user is rooted or is officer of the unit
    if (
        kwargs["isRoot"]
        or kwargs["id"] in unit.officers
        or is_superior_officer
    ):
        # Return response data
        return _update_personnel_helper(
            **data, operation="add", participation="member"
        )

    # Return error if not
    return client_error_response("You don't have access to this information")


@add_officers.route("/add_officers/", methods=["POST"])
@is_root
@permissions_required(["unit.add_officers"])
@param_check(ARGS.unit.add_officers)
@error_handler
def add_officers_endpoint(**kwargs):
    """Method to add a new officers to the unit"""

    # Parse information from the call's body
    data = request.get_json()

    # Get the unit object of the target unit and return if error
    unit = UnitAccess.get_unit(data["id"])
    if unit.status == "error":
        return unit, 400
    unit = unit.message.info

    # Check if the user is an officer of a superior unit
    is_superior_officer = isOfficerFromAbove(data["id"], kwargs["id"])

    # Check if the user is rooted or is officer of the unit
    if (
        kwargs["isRoot"]
        or kwargs["id"] in unit.officers
        or is_superior_officer
    ):
        # Return response data
        return _update_personnel_helper(
            **data, operation="add", participation="officer"
        )

    # Return error if not
    return client_error_response("You don't have access to this information")


#   endregion

#
#   READ OPERATIONS
#   region
#


@get_unit_info.route("/get_unit_info/", methods=["POST"])
@is_root
@param_check(ARGS.unit.get_unit_info)
@error_handler
def get_unit_info_endpoint(**kwargs):
    """Method to get the info of a unit"""

    # Parse information from the call's body
    data = request.get_json()

    # Get the id of the target unit
    id = data.pop("id")

    # Get the unit's information from the database
    result = UnitAccess.get_unit(id)

    # Return error if the result is in error
    if result.status == "error":
        return client_error_response(result)

    # Serialize the Unit object instance
    result.message = result.message.info

    # If the user requests for communication settings, check if they have
    # proper permissions
    if "communications" in data:
        if data["communications"]:
            # Check if the user is an officer of a superior unit
            is_superior_officer = isOfficerFromAbove(
                [data["id"]], kwargs["id"]
            )

            # If the user is not rooted nor is officer of the unit, err
            if not (
                kwargs["isRoot"]
                or kwargs["id"] in result.message.officers
                or is_superior_officer
            ):
                # Return error if not
                return client_error_response(
                    "You don't have access to this information with this query"
                )

            # Return response data
            return result, (200 if result.status == "success" else 400)

    # Delete the communication field
    if data["communications"]:
        del result.message.communications

    # Return response data
    return result, (200 if result.status == "success" else 400)


@get_unit_types.route("/get_unit_types/", methods=["GET"])
@jwt_required()
@error_handler
def get_unit_types_endpoint(**kwargs):
    """Return the unit types"""
    # Return content
    return success_response(config.unit_types)


@get_all_units.route("/get_all_units/", methods=["POST"])
@param_check(ARGS.unit.get_all_units)
@jwt_required()
@error_handler
def get_all_units_endpoint(**kwargs):
    """Method to get all unit IDs"""

    # Parse information from the call's body
    data = request.get_json()

    # Check if the body also has a tree attribute format
    tree_format = False
    if "tree_format" in data:
        tree_format = data["tree_format"]
        del data["tree_format"]

    # Get the content information based on the given page size and
    # page index
    results = UnitAccess.get_all_units(**data)

    # If the resulting information is in error, respond with error
    if results.status == "error":
        return client_error_response(results.message)

    # Respond with a tree format if the tree_format was wanted
    if tree_format:
        # Extract result
        nodes = results.message

        # Sort the nodes
        id_to_node_dict = {node.info._id: node.info for node in nodes}

        # set children key for all nodes
        for node in id_to_node_dict.values():
            node["children"] = []

        # connect parent nodes with their children and find the root
        roots = []
        for node in nodes:
            if node.info.parent:
                parent_id = node.info["parent"]
                parent_node = id_to_node_dict[parent_id]
                parent_node["children"].append(node.info)
            else:
                roots.append(node.info)

        # Return processed tree
        return success_response(roots)

    # Sort and Format message
    results.message = [item.info for item in results.message]
    results.message = sorted(
        results.message,
        key=lambda x: (config.unit_types.index(x["unit_type"]), x["name"]),
    )

    # Return the content of the information
    return results, 200


@get_all_members.route("/get_all_members/", methods=["POST"])
@is_root
@param_check(ARGS.unit.get_all_members)
@error_handler
def get_all_members_endpoint(**kwargs):
    """Function to handle getting all the members of a unit"""

    # Parse information from the call's body
    data = request.get_json()

    # Get the unit object of the target unit
    unit = UnitAccess.get_unit(data["id"])

    # Check if the unit exists
    if unit.status == "error":
        return unit, 400

    # Extract unit information
    unit = unit.message.info

    # Get the user's information from the database
    user = UserAccess.get_user(kwargs["id"]).message.info

    # Process unit information
    units = UnitAccess.get_units_below(user.units).message
    units = [item._id for item in units]

    # # Check if the user is rooted or is officer of the unit
    # if (
    #     kwargs["isRoot"]
    #     or kwargs["id"] in unit.officers
    #     or kwargs["id"] in unit.members
    #     or unit._id in units
    # ):
    #     # Get the list of members in the unit
    #     members = [
    #         UserAccess.get_user(member).message.get_generic_info(
    #             other_protections=["units", "permissions"]
    #         )
    #         for member in unit.members
    #     ]

    #     # Return information
    #     return success_response(members)

    # Get the list of members in the unit
    members = [
        UserAccess.get_user(member).message.get_generic_info(
            other_protections=["units", "permissions"]
        )
        for member in unit.members
    ]

    # Return information
    return success_response(members)


@get_all_officers.route("/get_all_officers/", methods=["POST"])
@is_root
@param_check(ARGS.unit.get_all_officers)
@error_handler
def get_all_officers_endpoint(**kwargs):
    """Function to handle getting all the officers of a unit"""

    # Parse information from the call's body
    data = request.get_json()

    # Get the unit object of the target unit
    unit = UnitAccess.get_unit(data["id"])

    # Check if the unit exists
    if unit.status == "error":
        return unit, 400

    # Extract unit information
    unit = unit.message.info

    # Get the user's information from the database
    user = UserAccess.get_user(kwargs["id"]).message.info

    # Process unit information
    units = UnitAccess.get_units_below(user.units).message
    units = [item._id for item in units]

    # # Check if the user is rooted or is officer of the unit
    # if (
    #     kwargs["isRoot"]
    #     or kwargs["id"] in unit.officers
    #     or kwargs["id"] in unit.members
    #     or unit._id in units
    # ):
    #     # Get the list of members in the unit
    #     officers = [
    #         UserAccess.get_user(member).message.get_generic_info(
    #             other_protections=["units", "permissions"]
    #         )
    #         for member in unit.officers
    #     ]

    #     # Return information
    #     return success_response(officers)

    # Get the list of members in the unit
    officers = [
        UserAccess.get_user(member).message.get_generic_info(
            other_protections=["units", "permissions"]
        )
        for member in unit.officers
    ]

    # Return information
    return success_response(officers)


@get_specified_personnel.route("/get_specified_personnel/", methods=["POST"])
@is_root
@param_check(ARGS.unit.get_specified_personnel)
@error_handler
def get_specified_personnel_endpoint(**kwargs):
    """Endpoint to get the users that the callee is wanting to extract"""

    # Parse information from the call's body
    data = request.get_json()

    # Initialize result set to store processed items
    result = set()

    # Process each item in the raw data
    for raw_item in data["raw"]:
        # Split item for easier processing
        item = raw_item.split(", ")

        # Directly add the user if the action is "User"
        if item[0] == "User":
            result.add(item[1])
            continue

        # Extract specifications from the iteration
        action, user_type, unit_id = item

        # Function to handle error for a given unit
        def handle_error(unit_result):
            if unit_result.status == "error":
                return client_error_response(
                    f"Error occurred when processing unit: {unit_id}"
                )
            return None

        # Fetch the units based on action: "Cascade" or "No Cascade"
        units = []
        if action == "Cascade":
            response = UnitAccess.get_units_below([unit_id])
            error_response = _handle_error(response, unit_id)
            if error_response:
                return error_response
            units = response.message
        elif action == "No Cascade":
            response = UnitAccess.get_unit(unit_id)
            error_response = _handle_error(response, unit_id)
            if error_response:
                return error_response
            units = [response.message.info]

        # Process users based on user type: "All", "Members-Only", or
        # "Officers-Only"
        for unit in units:
            if user_type == "All":
                result.update(unit["officers"], unit["members"])
            elif user_type == "Members-Only":
                result.update(unit["members"])
            elif user_type == "Officers-Only":
                result.update(unit["officers"])

    # Return results
    return success_response(list(result))


@is_superior_officer.route("/is_superior_officer/", methods=["POST"])
@is_root
@param_check(ARGS.unit.is_superior_officer)
@error_handler
def is_superior_officer_endpoint(**kwargs):
    """Method to check if the user is a superior unit"""

    # Parse information from the call's body
    data = request.get_json()

    # Get the unit object of the target unit and return if error
    unit = UnitAccess.get_unit(data["id"])
    if unit.status == "error":
        return unit, 400
    unit = unit.message.info

    # Check if the user is an officer of a superior unit
    res = isOfficerFromAbove(data["id"], kwargs["id"])

    # Return result
    return success_response(True) if res else client_error_response(False)


@get_all_five_point_data.route("/get_all_five_point_data/", methods=["POST"])
@is_root
@permissions_required(["unit.get_all_five_point_data"])
@param_check(ARGS.unit.get_all_five_point_data)
@error_handler
def get_all_five_point_data_endpoint(**kwargs):
    """
    Respond with a given unit's five point data for all its members and
    officers
    """

    # Parse information from the call's body
    data = request.get_json()

    # Get the unit object of the target unit and return if error
    unit = UnitAccess.get_unit(data["id"])
    if unit.status == "error":
        return client_error_response(unit.message)
    unit = unit.message.info

    # Check if the user is an officer of a superior unit
    is_superior_officer = isOfficerFromAbove(data["id"], kwargs["id"])

    # If the user is not rooted nor is officer of the unit, return error
    if not (
        kwargs["isRoot"]
        or kwargs["id"] in unit.officers
        or is_superior_officer
    ):
        # Return error if not
        return client_error_response(
            "You don't have access to this information"
        )

    # Get a list of all units and their members below
    below = UnitAccess.get_units_below([unit._id]).message

    # Get all of the users' five point info and the mapping for the unit they
    # are in
    mapper = {}
    memoize = set()
    for item in below:
        track = []
        for user in item.members + item.officers:
            if user in memoize:
                continue
            res = FivePointAccess.get_user_five_point(user, 10000, 0).message
            for i in res:
                i["full_name"] = UserAccess.get_user(
                    i["to_user"]
                ).message.info.full_name
            memoize.add(user)
            track += res
        track = sorted(
            track,
            key=lambda x: x["composite_score"],
            reverse=True,
        )
        mapper[item.name] = track

    # Success return
    return success_response(mapper)


@get_all_pfa_data.route("/get_all_pfa_data/", methods=["POST"])
@is_root
@permissions_required(["unit.get_all_pfa_data"])
@param_check(ARGS.unit.get_all_pfa_data)
@error_handler
def get_all_pfa_data_endpoint(**kwargs):
    """Endpoint to return a unit's PFA data for all its members and officers"""

    # Parse information from the call's body
    data = request.get_json()

    # Get the unit object of the target unit and return if error
    unit = UnitAccess.get_unit(data["id"])
    if unit.status == "error":
        return client_error_response(unit.message)
    unit = unit.message.info

    # Check if the user is an officer of a superior unit
    is_superior_officer = isOfficerFromAbove(data["id"], kwargs["id"])

    # If the user is not rooted nor is officer of the unit, return error
    if not (
        kwargs["isRoot"]
        or kwargs["id"] in unit.officers
        or is_superior_officer
    ):
        # Return error if not
        return client_error_response(
            "You don't have access to this information"
        )

    # Get a list of all units and their members below
    below = UnitAccess.get_units_below([unit._id]).message

    # Get all of the users' PFA info and the mapping for the unit they are in
    mapper = {}
    memoize = set()
    for item in below:
        track = []
        for user in item.members + item.officers:
            if user in memoize:
                continue
            res = PFAAccess.get_user_pfa(user, 10000, 0).message
            for i in res:
                i["full_name"] = UserAccess.get_user(
                    i["to_user"]
                ).message.info.full_name
            memoize.add(user)
            track += res
        track = sorted(
            track,
            key=lambda x: x["composite_score"],
            reverse=True,
        )
        mapper[item.name] = track

    # Success return
    return success_response(mapper)


@get_all_warrior_data.route("/get_all_warrior_data/", methods=["POST"])
@is_root
@permissions_required(["unit.get_all_warrior_data"])
@param_check(ARGS.unit.get_all_warrior_data)
@error_handler
def get_all_warrior_data_endpoint(**kwargs):
    """Endpoint to return a unit's WK data for all its members and officers"""

    # Parse information from the call's body
    data = request.get_json()

    # Get the unit object of the target unit and return if error
    unit = UnitAccess.get_unit(data["id"])
    if unit.status == "error":
        return client_error_response(unit.message)
    unit = unit.message.info

    # Check if the user is an officer of a superior unit
    is_superior_officer = isOfficerFromAbove(data["id"], kwargs["id"])

    # If the user is not rooted nor is officer of the unit, return error
    if not (
        kwargs["isRoot"]
        or kwargs["id"] in unit.officers
        or is_superior_officer
    ):
        # Return error if not
        return client_error_response(
            "You don't have access to this information"
        )

    # Get a list of all units and their members below
    below = UnitAccess.get_units_below([unit._id]).message

    # Get all of the users' WK info and the mapping for the unit they are in
    mapper = {}
    memoize = set()
    for item in below:
        track = []
        for user in item.members + item.officers:
            if user in memoize:
                continue
            res = WarriorAccess.get_user_warrior(user, 10000, 0).message
            for i in res:
                i["full_name"] = UserAccess.get_user(
                    i["to_user"]
                ).message.info.full_name
            memoize.add(user)
            track += res
        track = sorted(
            track,
            key=lambda x: x["composite_score"],
            reverse=True,
        )
        mapper[item.name] = track

    # Success return
    return success_response(mapper)


#   endregion

#
#   UPDATE OPERATIONS
#   region
#


@update_unit.route("/update_unit/", methods=["POST"])
@permissions_required(["unit.update_unit"])
@param_check(ARGS.unit.update_unit)
@error_handler
def update_unit_endpoint(**kwargs):
    """Method to handle the update of a unit"""

    # Parse information from the call's body
    data = request.get_json()

    # Get the unit object of the target unit and return if error
    unit = UnitAccess.get_unit(data["id"])
    if unit.status == "error":
        return unit, 400
    unit = unit.message.info

    # Check if the user specified the parent class
    if "parent" in data:
        # Get the old parent unit and update it
        old_unit = UnitAccess.get_unit(unit.parent)
        if old_unit.status == "success":
            old_unit = old_unit.message
            old_unit.delete_child(unit._id)
            UnitAccess.update_unit(old_unit.info._id, **old_unit.info)

        # If parent is empty, keep going forward
        if data["parent"] == "":
            pass

        # If not, proceed
        else:
            # Get the unit in question
            new_unit = UnitAccess.get_unit(data["parent"])
            if new_unit.status == "error":
                return client_error_response(
                    "The new parent unit doesn't exist"
                )
            new_unit = new_unit.message

            # Update the new parent unit
            new_unit.add_child(unit._id)
            UnitAccess.update_unit(new_unit.info._id, **new_unit.info)

    # Prevent certain attributes
    if (
        "children" in data
        or "members" in data
        or "officers" in data
        or "communications" in data
    ):
        return client_error_response("Cannot change unit given attributes")

    # Get the id of the target unit
    id = data.pop("id")

    # Add the unit to the database
    result = UnitAccess.update_unit(id, **data)

    # Return response data
    return result, (200 if result.status == "success" else 400)


@update_frontpage.route("/update_frontpage/", methods=["POST"])
@is_root
@permissions_required(["unit.update_frontpage"])
@param_check(ARGS.unit.update_frontpage)
@error_handler
def update_frontpage_endpoint(**kwargs):
    """Endpoint to update the unit's frontpage"""

    # Parse information from the call's body
    data = request.get_json()

    # Get the unit object of the target unit and return if error
    unit = UnitAccess.get_unit(data["id"])
    if unit.status == "error":
        return unit, 400
    unit = unit.message.info

    # Check if the user is an officer of a superior unit
    is_superior_officer = isOfficerFromAbove(data["id"], kwargs["id"])

    # Check if the user is rooted or is officer of the unit
    if (
        kwargs["isRoot"]
        or kwargs["id"] in unit.officers
        or is_superior_officer
    ):
        # Update the front page
        res = UnitAccess.update_unit(
            id=data["id"], frontpage=data["frontpage"]
        )

        # Return message
        return (
            client_error_response(res.message)
            if res.status == "error"
            else success_response("Frontpage Updated")
        )

    # Return error if not
    return client_error_response("You don't have access to this information")


@update_communication_settings.route(
    "/update_communication_settings/", methods=["POST"]
)
@is_root
@permissions_required(["unit.update_communication_settings"])
@param_check(ARGS.unit.update_communication_settings)
@error_handler
def update_communication_settings_endpoint(**kwargs):
    """Endpoint to update a unit's communication settings"""

    # Parse information from the call's body
    data = request.get_json()

    # Get the unit object of the target unit and return if error
    unit = UnitAccess.get_unit(data["id"])
    if unit.status == "error":
        return client_error_response(unit.message)
    unit = unit.message.info

    # Check if the user is an officer of a superior unit
    is_superior_officer = isOfficerFromAbove(data["id"], kwargs["id"])

    # If the user is not rooted nor is officer of the unit, return error
    if not (
        kwargs["isRoot"]
        or kwargs["id"] in unit.officers
        or is_superior_officer
    ):
        # Return error if not
        return client_error_response(
            "You don't have access to this information"
        )

    # Update the unit's communication setting
    update_data = {
        f"communication.{data['communication']}.{nested_field}": new_value
        for nested_field, new_value in data["settings"].items()
    }
    result = UnitAccess.update_unit(data["id"], **update_data)

    # Return response data
    return result, (200 if result.status == "success" else 400)


#   endregion

#
#   DELETE OPERATIONS
#   region
#


@delete_unit.route("/delete_unit/", methods=["POST"])
@permissions_required(["unit.delete_unit"])
@param_check(ARGS.unit.delete_unit)
@error_handler
def delete_unit_endpoint(**kwargs):
    """Method to handle the deletion of a unit"""

    # Parse information from the call's body
    data = request.get_json()

    # Add the unit to the database
    result = UnitAccess.delete_unit(**data)

    # Return response data
    return result, (200 if result.status == "success" else 400)


@delete_members.route("/delete_members/", methods=["POST"])
@is_root
@permissions_required(["unit.delete_members"])
@param_check(ARGS.unit.delete_members)
@error_handler
def delete_members_endpoint(**kwargs):
    """Method to delete members to the unit"""

    # Parse information from the call's body
    data = request.get_json()

    # Get the unit object of the target unit and return if error
    unit = UnitAccess.get_unit(data["id"])
    if unit.status == "error":
        return unit, 400
    unit = unit.message.info

    # Check if the user is an officer of a superior unit
    is_superior_officer = isOfficerFromAbove(data["id"], kwargs["id"])

    # Check if the user is rooted or is officer of the unit
    if (
        kwargs["isRoot"]
        or kwargs["id"] in unit.officers
        or is_superior_officer
    ):
        # Return response data
        return _update_personnel_helper(
            **data, operation="delete", participation="member"
        )

    # Return error if not
    return client_error_response("You don't have access to this information")


@delete_officers.route("/delete_officers/", methods=["POST"])
@is_root
@permissions_required(["unit.delete_officers"])
@param_check(ARGS.unit.delete_officers)
@error_handler
def delete_officers_endpoint(**kwargs):
    """Method to delete officers to the unit"""

    # Parse information from the call's body
    data = request.get_json()

    # Get the unit object of the target unit and return if error
    unit = UnitAccess.get_unit(data["id"])
    if unit.status == "error":
        return unit, 400
    unit = unit.message.info

    # Check if the user is an officer of a superior unit
    is_superior_officer = isOfficerFromAbove(data["id"], kwargs["id"])

    # Check if the user is rooted or is officer of the unit
    if (
        kwargs["isRoot"]
        or kwargs["id"] in unit.officers
        or is_superior_officer
    ):
        # Return response data
        return _update_personnel_helper(
            **data, operation="delete", participation="officer"
        )

    # Return error if not
    return client_error_response("You don't have access to this information")


#   endregion
