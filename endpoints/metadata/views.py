# Import the test blueprint
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
)
from . import get_metadata, delete_metadata, update_metadata
from endpoints.base import (
    permissions_required,
    param_check,
    serverErrorResponse,
    ARGS,
)
from database.user import UserAccess
from flask import request


@get_metadata.route("/get/", methods=["GET"])
@param_check(ARGS.authentication.login)
def get_endpoint():
    return "sucess"


@update_metadata.route("/update/", methods=["GET"])
@param_check(ARGS.authentication.login)
def update_endpoint():
    try:
        data = request.get_json()
        return "sucess"
    except:
        return


@delete_metadata.route("/delete/", methods=["GET"])
@param_check(ARGS.authentication.login)
def delete_endpoint():
    return "sucess"
