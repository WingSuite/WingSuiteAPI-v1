# Import
from flask import Blueprint

# Blueprint initialization
create_warrior = Blueprint("create_warrior", __name__)
get_warrior_info = Blueprint("get_warrior_info", __name__)
get_user_warrior_info = Blueprint("get_user_warrior_info", __name__)
get_warrior_format_info = Blueprint("get_warrior_format_info", __name__)
get_test_warrior_score = Blueprint("get_test_warriorscore", __name__)
delete_warrior = Blueprint("delete_warrior", __name__)
update_warrior = Blueprint("update_warrior", __name__)

# Import views
from . import views   # noqa
