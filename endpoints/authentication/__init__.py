# Import
from flask import Blueprint

# Blueprint initialization
login = Blueprint("login", __name__)
refresh = Blueprint("refresh", __name__)
register = Blueprint("register", __name__)
authorize = Blueprint("authorize", __name__)
reject = Blueprint("reject", __name__)
signout = Blueprint("signout", __name__)

# Import views
from . import views   # noqa