# Import
import logging
from main import app

# Set up logging
logging.basicConfig(level=logging.INFO)

# Main run thread
if __name__ == "__main__":
    logging.info("Starting the application...")
    app.run()
