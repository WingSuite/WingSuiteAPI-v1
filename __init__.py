# Import
from flask import Flask
from test import home, login, dashboard, signout, home

# Make app name
app = Flask(__name__)

# Register all blueprints
app.register_blueprint(home, url_prefix="/home/")
app.register_blueprint(login, url_prefix="/user/")
app.register_blueprint(dashboard, url_prefix="/user/")
app.register_blueprint(signout, url_prefix="/user/")


# Main run thread
if __name__ == '__main__':
    app.run()