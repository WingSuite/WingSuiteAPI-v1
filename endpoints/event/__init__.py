# Import
from flask import Blueprint

# Blueprint initialization
create_event = Blueprint("create_event", __name__)
update_event = Blueprint("update_event", __name__)
get_event_info = Blueprint("get_event_info", __name__)
delete_event = Blueprint("delete_event", __name__)

# Import views
from . import views   # noqa
