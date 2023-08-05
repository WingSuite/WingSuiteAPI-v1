# Imports
from utils.dict_parse import DictParse
from config.config import config
from functools import wraps
from typing import Any
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
    EVENT_COL = DB["events"]
    BLACKLIST_COL = DB["jwtBlacklist"]
    CURRENT_STATS_COL = DB["currentStats"]
    NOTIFICATION_COL = DB["notifications"]
    FORMER_USERS_COL = DB["formerUsers"]

    # Set config constants
    CONFIG = config

    def sendError(message: str, **kwargs: Any) -> dict:
        """Error message format method"""

        # Prep the message
        message = {"status": "error", "message": message}
        message.update(kwargs)

        # Return the success message
        return message

    def sendSuccess(message: str, **kwargs: Any) -> dict:
        """Success message format method"""

        # Prep the message
        message = {"status": "success", "message": message}
        message.update(kwargs)

        # Return the success message
        return message

    def dict_wrap(func: object) -> object:
        """Dictionary to object wrapper"""

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> DictParse:
            """Wrapping definition"""

            # Return with parsing wrapping if all else is good
            return DictParse(func(*args, **kwargs))

        # End of wrapper definition
        return wrapper
