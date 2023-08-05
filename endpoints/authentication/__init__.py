# Import
from flask import Blueprint

# Blueprint initialization
register = Blueprint("register", __name__)
login = Blueprint("login", __name__)
get_register_requests = Blueprint("get_register_requests", __name__)
refresh = Blueprint("refresh", __name__)
authorize = Blueprint("authorize", __name__)
signout = Blueprint("signout", __name__)
reject = Blueprint("reject", __name__)
kick_user = Blueprint("kick_user", __name__)

# Import views
from . import views   # noqa