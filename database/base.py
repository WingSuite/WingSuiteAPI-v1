# Imports
from config.config import config
import pymongo

class DataAccessBase:
    """Encapsulation of all database actions"""
    
    # Static Variable Create
    CLIENT = pymongo.MongoClient('mongodb://localhost:27018/')
    DB = CLIENT['Det025']
    USER_COL = DB['users']
    REGISTER_COL = DB['registerList']
    REQ_ARGS = config.neededArguments.DataAccess