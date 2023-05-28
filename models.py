import uuid
from flask import Flask, jsonify

class User:
    
    def info(self):
      user = {
        "_id": uuid.uuid4().hex,
        "name": "",
        "email": "",
        "password": ""
      }
      return jsonify(user)
