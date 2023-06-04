# Import
from flask import Blueprint

# Blueprint initialization
login = Blueprint('login', __name__)
register = Blueprint('register', __name__)
authorize = Blueprint('authorize', __name__)
add_permission = Blueprint('add_permission', __name__)
delete_permission = Blueprint('delete_permission', __name__)

home = Blueprint('home', __name__)
dashboard = Blueprint('dashboard', __name__)
signout = Blueprint('signout', __name__)

# Import all views from views.py
from . import views