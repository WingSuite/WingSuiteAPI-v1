# Import the test blueprint
from . import test_bp

# Test endpoint
@test_bp.route('/test')
def test_handler():
    return {"key" : "value"}