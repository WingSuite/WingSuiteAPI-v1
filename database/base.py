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
    BLACKLIST_COL = DB["jwt_blacklist"]

    # Set config constants
    CONFIG = config

    def sendError(message: str) -> dict:
        """Error message format method"""
        return {"status": "error", "message": message}

    def sendSuccess(message: str) -> dict:
        """Success message format method"""
        return {"status": "success", "message": message}

    def dict_wrap(func: object) -> object:
        """Dictionary to object wrapper"""

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> DictParse:
            """Wrapping definition"""

            # Return with parsing wrapping if all else is good
            return DictParse(func(*args, **kwargs))

        # End of wrapper definition
        return wrapper
