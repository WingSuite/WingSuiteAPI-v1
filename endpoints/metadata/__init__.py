# Import
from flask import Blueprint

# Blueprint initialization
delete_metadata = Blueprint("delete_metadata", __name__)
update_metadata = Blueprint("update_metadata", __name__)
get_metadata = Blueprint("get_metadata", __name__)

# Import views
from . import views   # noqa
