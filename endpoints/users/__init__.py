# Import
from flask import Blueprint

# Blueprint initialization
add_permissions = Blueprint("add_permissions", __name__)
delete_permissions = Blueprint("delete_permissions", __name__)

# Import all views from views.py
from . import views