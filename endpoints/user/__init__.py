# Import
from flask import Blueprint

# Blueprint initialization
add_permissions = Blueprint("add_permissions", __name__)
who_am_i = Blueprint("who_am_i", __name__)
everyone = Blueprint("everyone", __name__)
get_user = Blueprint("get_user", __name__)
get_feedbacks = Blueprint("feedback", __name__)
get_events = Blueprint("get_events", __name__)
get_notifications = Blueprint("get_notifications", __name__)
get_pfa_data = Blueprint("get_pfa_data", __name__)
get_warrior_data = Blueprint("get_warrior_data", __name__)
get_tasks = Blueprint("get_tasks", __name__)
get_users_units = Blueprint("get_users_units", __name__)
get_permissions_list = Blueprint("get_permissions_list", __name__)
update_permissions = Blueprint("update_permissions", __name__)
update_rank = Blueprint("update_rank", __name__)
delete_permissions = Blueprint("delete_permissions", __name__)

# Import views
from . import views  # noqa
