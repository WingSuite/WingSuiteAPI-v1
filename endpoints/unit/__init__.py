# Import
from flask import Blueprint

# Blueprint initialization
create_unit = Blueprint("create_unit", __name__)
add_members = Blueprint("add_members", __name__)
add_officers = Blueprint("add_officers", __name__)
update_unit = Blueprint("update_unit", __name__)
update_frontpage = Blueprint("update_frontpage", __name__)
get_unit_info = Blueprint("get_unit_info", __name__)
get_unit_types = Blueprint("get_unit_types", __name__)
get_all_units = Blueprint("get_all_units", __name__)
get_all_members = Blueprint("get_all_members", __name__)
get_all_officers = Blueprint("get_all_officers", __name__)
get_specified_personnel = Blueprint("get_specified_personnel", __name__)
is_superior_officer = Blueprint("is_superior_officer", __name__)
get_all_five_point_data = Blueprint("get_all_five_point_data", __name__)
get_all_pfa_data = Blueprint("get_all_pfa_data", __name__)
get_all_warrior_data = Blueprint("get_all_warrior_data", __name__)
delete_unit = Blueprint("delete_unit", __name__)
delete_members = Blueprint("delete_members", __name__)
delete_officers = Blueprint("delete_officers", __name__)

# Import views
from . import views   # noqa
