import pymongo
from flask import request, jsonify

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['Det025']
collection = db['users']


def insert_data():
	if request.method == 'POST':
		name = request.form['name']
		email = request.form['email']
		password = request.form['pass']

		reg_user = {}
		reg_user['name'] = name
		reg_user['email'] = email
		reg_user['password'] = password

		if collection.find_one({"email":email}) == None:
			collection.insert_one(reg_user)
			return True
		else:
			return False


def check_user(email, password):

	user = {
		"email": email,
		"password": password
	}

	user_data = collection.find_one(user)
	user_data.pop('_id', None)
	#user_data.pop('password', None)
	resp = jsonify(user_data)


	if user_data == None:
		return ""
	else:
		return resp