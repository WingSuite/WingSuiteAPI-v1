# Import the test blueprint
from . import home, login, dashboard, signout
from flask import Flask, jsonify, request
from models import User
import db
import pymongo

# Test endpoint
@home.route('')
def test_handler():
    return "Home"

@login.route('/login/', methods=['POST', 'GET'])
def login_handler():
    try:
        if request.headers.get('Content-Type') == 'application/json':
            data = request.get_json()
            
            email = data['email']
            password = data['password']

            response_data = {
                'email': email,
                'password': password,
                'profileImage': "",
                'refresh': "",
                'access': "",
                'success': "success"
            }
            
            response_json = jsonify(response_data)
            
            return response_json
        else:
            return jsonify({'error': 'Invalid Content-Type. Expected application/json.'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


    #return "Login Page"

@dashboard.route('/dashboard/')
def dashboard_handler():
    return User().info()


@signout.route('/signout/')
def signout_handler():
    return "Signout"