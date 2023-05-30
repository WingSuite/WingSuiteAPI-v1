# Import
from flask import Flask
from authentication import *
from flask_cors import CORS


# Make app name and initialize CORS
app = Flask(__name__)
CORS(app, methods=['POST', 'GET'])

# Register all blueprints
app.register_blueprint(home, url_prefix="/home/")
app.register_blueprint(login, url_prefix="/user/")
app.register_blueprint(register, url_prefix="/user/")
app.register_blueprint(authorize, url_prefix="/user/")
app.register_blueprint(dashboard, url_prefix="/user/")
app.register_blueprint(signout, url_prefix="/user/")

# Main run thread
if __name__ == '__main__':
    app.run()