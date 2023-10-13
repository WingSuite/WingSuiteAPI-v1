# Import
from flask import Blueprint

# Blueprint initialization
create_task = Blueprint("create_task", __name__)
get_task_info = Blueprint("get_task_info", __name__)
update_task = Blueprint("update_task", __name__)
request_completion = Blueprint("request_completion", __name__)
reject_completion = Blueprint("reject_completion", __name__)
approve_completion = Blueprint("approve_completion", __name__)
delete_task = Blueprint("delete_task", __name__)

# Import views
from . import views   # noqa
