# Import
from flask import Blueprint

# Blueprint initialization
home = Blueprint('home', __name__)
login = Blueprint('login', __name__)
dashboard = Blueprint('dashboard', __name__)
signout = Blueprint('signout', __name__)

# Import all views from views.py
from . import views