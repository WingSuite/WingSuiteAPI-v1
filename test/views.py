# Import the test blueprint
from . import home, login, dashboard, signout
from flask import Flask, jsonify, request, json
from models import User
import db
import pymongo
from pprint import pprint
from bson.json_util import dumps, loads
from flask_cors import CORS

# Test endpoint
@home.route('')
def test_handler():
    return "Home"


@login.route('/login/', methods=['POST'])
def login_handler():
    try:
        if request.headers.get('Content-Type') == 'application/json':
            data = request.get_json('http://localhost:2501/')
            email = data['email']
            password = data['password']
             #
            json_string = json.dumps(data)
            print(json_string)
            #
            response_data = db.check_user(email, password)

             #
            pprint(response_data)

            json_string = json.dumps(response_data)

            print(json_string)
            #
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