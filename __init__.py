# Import
from flask import Flask
from test import test_bp

# Make app name
app = Flask(__name__)

# Register all blueprints
app.register_blueprint(test_bp, url_prefix="/test/")

# Main run thread
if __name__ == '__main__':
    app.run()