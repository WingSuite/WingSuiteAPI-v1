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
    BLACKLIST_COL = DB["jwt_blacklist"]

    # Set config constants
    REQ_ARGS = arguments.dataAccess
    CONFIG = config

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
