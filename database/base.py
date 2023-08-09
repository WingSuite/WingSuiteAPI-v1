# Imports
from utils.dict_parse import DictParse
from config.config import config
from functools import wraps
from typing import Any
import pymongo
import os


class DataAccessBase:
    """Encapsulation of all database actions"""

    # Get the different database configurations based on the run type
    if int(os.environ.get("RUN_MODE")) == 1:
        db_spec = config.database.production
    else:
        db_spec = config.database.development

    # Set MongoDB information based on the database specifications
    if db_spec.user != "" and db_spec.password != "":
        CLIENT = pymongo.MongoClient(
            f"mongodb://{db_spec.user}:{db_spec.password}@{db_spec.domain}"
            + f":{db_spec.port}/{db_spec.db}"
        )
        DB = CLIENT[db_spec.db]
    else:
        CLIENT = pymongo.MongoClient(
            f"mongodb://{db_spec.domain}:{db_spec.port}/"
        )
        DB = CLIENT[db_spec.db]

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
    DB_SPECS = db_spec
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
