# Imports
from config.config import config, arguments
from utils.dict_parse import DictParse
from functools import wraps
import pymongo


class DataAccessBase:
    """Encapsulation of all database actions"""

    # Get MongoDB information
    CLIENT = pymongo.MongoClient(
        f"mongodb://{config.database.domain}:{config.database.port}/"
    )
    DB = CLIENT[config.database.db]

    # Collection constant definition
    USER_COL = DB["users"]
    REGISTER_COL = DB["registerList"]
    UNIT_COL = DB["units"]
    BLACKLIST_COL = DB["jwt_blacklist"]

    # Set config constants
    REQ_ARGS = arguments.dataAccess
    CONFIG = config

    def sendError(message):
        """Error message format method"""
        return {"status": "error", "message": message}

    def sendSuccess(message):
        """Success message format method"""
        return {"status": "success", "message": message}

    def checkDataType(data, schema):
        """Method that checks if the given data follows the datatype schema"""

        # Iterate through every key, value pair in the data dictionary
        for key, value in data.items():
            # Check if the datatype of the iterated value is the same
            # as the corresponding schema value. If not, return false
            if key in schema.keys() and type(value) is not schema[key]:
                return False

        # Return true
        return True

    def param_check(required_params):
        """Method that checks for minimum parameters"""

        def decorator(func):
            """Decorator definition"""

            @wraps(func)
            def wrapper(*args, **kwargs):
                """Wrapping definition"""

                # Check if the given arguments has the minimum arguments
                for arg in required_params:
                    if arg not in kwargs:
                        return {
                            "status": "error",
                            "message": "Call needs the following arguments: "
                            + ", ".join(required_params),
                        }

                # Return normally if all else is good
                return func(*args, **kwargs)

            # End of wrapper definition
            return wrapper

        # End of decorator definition
        return decorator

    def dict_wrap(func):
        """Dictionary to object wrapper"""

        @wraps(func)
        def wrapper(*args, **kwargs):
            """Wrapping definition"""

            # Return with parsing wrapping if all else is good
            return DictParse(func(*args, **kwargs))

        # End of wrapper definition
        return wrapper
