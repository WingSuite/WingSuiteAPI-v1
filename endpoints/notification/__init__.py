# Import
from flask import Blueprint

# Blueprint initialization
create_notification = Blueprint("create_notification", __name__)
get_notification_info = Blueprint("get_notification_info", __name__)
delete_notification = Blueprint("delete_notification", __name__)
update_notification = Blueprint("update_notification", __name__)

# Import views
from . import views   # noqa
