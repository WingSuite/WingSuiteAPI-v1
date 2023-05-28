# Import the test blueprint
from . import home, login, dashboard, signout
from flask import Flask, jsonify, request
from models import User
import db
import pymongo
from bson.json_util import dumps, loads

# Test endpoint
@home.route('')
def test_handler():
    return "Home"

@login.route('/login/', methods=['POST', 'GET'])
def login_handler():
    try:
        if request.headers.get('Content-Type') == 'application/json':
            data = request.get_json('http://localhost:2501/')
            email = data['email']
            password = data['password']
            
            response_data = db.check_user(email, password)
            return response_data
        else:
            return jsonify({'error': 'Invalid Content-Type. Expected application/json.'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@dashboard.route('/dashboard/')
def dashboard_handler():
    return User().info()


@signout.route('/signout/')
def signout_handler():
    return "Signout"