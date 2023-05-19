# Import
from flask import Blueprint

# Blueprint initialization
test_bp = Blueprint('test', __name__)

# Import all views from views.py
from . import views