# Import
from flask import Blueprint

# Blueprint initialization
add_permission = Blueprint("add_permission", __name__)
delete_permission = Blueprint("delete_permission", __name__)

# Import all views from views.py
from . import views