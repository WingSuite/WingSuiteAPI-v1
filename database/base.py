# Imports
from config.config import config
import pymongo

class DataAccessBase:
    """Encapsulation of all database actions"""
    
    # Get MongoDB information
    CLIENT = pymongo.MongoClient(
        f'mongodb://{config.database.domain}:{config.database.port}/'
    )
    DB = CLIENT[config.database.db]
    USER_COL = DB['users']
    REGISTER_COL = DB['registerList']
    
    # Set config constants    
    REQ_ARGS = config.neededArguments.DataAccess
    CONFIG = config
    
    @staticmethod
    def args_checker(args, key):
        """Check if the given args is sufficient"""

        # Check if the given arumgents has the minimum arguments
        for arg in DataAccessBase.REQ_ARGS[key]:
            if arg not in args:
                return {
                    "status": "error", 
                    "message": "Call needs the following arguments: " \
                        + ", ".join(DataAccessBase.REQ_ARGS[key])
                }

        # Return None if nothing else
        return None