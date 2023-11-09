# Import
from flask import Blueprint

# Blueprint initialization
create_feedback = Blueprint("create_feedback", __name__)
get_feedback_info = Blueprint("get_feedback_info", __name__)
update_feedback = Blueprint("update_feedback", __name__)
delete_feedback = Blueprint("delete_feedback", __name__)

# Import views
from . import views   # noqa
