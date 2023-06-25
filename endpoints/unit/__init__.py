# Import
from flask import Blueprint

# Blueprint initialization
create_unit = Blueprint("create_unit", __name__)
update_unit = Blueprint("update_unit", __name__)
get_unit_info = Blueprint("get_unit_info", __name__)
get_all_units = Blueprint("get_all_units", __name__)
delete_unit = Blueprint("delete_unit", __name__)
add_members = Blueprint("add_members", __name__)
delete_members = Blueprint("delete_members", __name__)
add_officers = Blueprint("add_officers", __name__)
delete_officers = Blueprint("delete_officers", __name__)

# Import views
from . import views   # noqa
