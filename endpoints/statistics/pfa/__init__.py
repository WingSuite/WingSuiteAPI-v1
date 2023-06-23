# Import
from flask import Blueprint

# Blueprint initialization
create_pfa = Blueprint("create_pfa", __name__)
delete_pfa = Blueprint("delete_pfa", __name__)
update_pfa = Blueprint("update_pfa", __name__)
get_pfa_info = Blueprint("get_pfa_info", __name__)

# Import views
from . import views   # noqa
