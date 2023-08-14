# Import
from flask import Blueprint

# Blueprint initialization
create_five_point = Blueprint("create_five_point", __name__)
get_five_point_info = Blueprint("get_five_point_info", __name__)
get_user_five_point_info = Blueprint("get_user_five_point_info", __name__)
get_five_point_format_info = Blueprint("get_five_point_format_info", __name__)
get_test_five_point_score = Blueprint("get_test_five_point_score", __name__)
update_five_point = Blueprint("update_five_point", __name__)
delete_five_point = Blueprint("delete_five_point", __name__)

# Import views
from . import views   # noqa
