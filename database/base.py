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