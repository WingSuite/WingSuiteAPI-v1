# Import
from flask import Blueprint

# Blueprint initialization
add_permissions = Blueprint("add_permissions", __name__)
delete_permissions = Blueprint("delete_permissions", __name__)
who_am_i = Blueprint("who_am_i", __name__)

# Import views
from . import views   # noqa
