# Imports
from config import config
from models import User
import pymongo
import uuid

class DataAccess:
    """Encapsulation of all database actions"""
    
    # Static Variable Create
    CLIENT = pymongo.MongoClient('mongodb://localhost:27018/')
    DB = CLIENT['Det025']
    USER_COL = DB['users']
    REGISTER_COL = DB['registerList']
    REQ_ARGS = config.neededArguments.DataAccess

    @staticmethod
    def add_user(**kwargs):
        """Method that handles adding a user to the system"""
  
        # Check if kwargs has the minimum arguments
        for arg in DataAccess.REQ_ARGS.add_user:
            if arg not in kwargs:
                return {
                    "status": "error", 
                    "message": "Call needs the following arguments: " \
                        + ", ".join(DataAccess.REQ_ARGS.add_user)
                }

        # Add user to the list and return success if the given 
        # information is not the system
        user = DataAccess.REGISTER_COL.find_one({"email": kwargs["email"]})
        if user != None:   
            # Insert user into the database, remove from REGISTER_COL and return success
            DataAccess.USER_COL.insert_one(user)
            DataAccess.REGISTER_COL.delete_one({"email": kwargs["email"]})
            return {"status": "success", "message": "User added to the system"}
        # Return false if the given information exists
        else:
            return {"status": "error", "message": "User didn't register"}
        
    @staticmethod
    def register_user(**kwargs):
        """Method that handles registering a user to the system"""
  
        # Check if kwargs has the minimum arguments
        for arg in DataAccess.REQ_ARGS.register_user:
            if arg not in kwargs:
                return {
                    "status": "error", 
                    "message": "Call needs the following arguments: " \
                        + ", ".join(DataAccess.REQ_ARGS.register_user)
                }

        # Add user to the list and return success if the given 
        # information is not the system
        if DataAccess.USER_COL.find_one({"email": kwargs["email"]}) == None and \
        DataAccess.REGISTER_COL.find_one({"email": kwargs["email"]}) == None:
            # Prep data to be inserted
            kwargs["_id"] = uuid.uuid4().hex
   
            # Insert user into the database and return success
            DataAccess.REGISTER_COL.insert_one(kwargs)
            return {"status": "success", "message": "User is up for authorization"}
        # Return false if the given information exists
        else:
            return {"status": "error", "message": "User has registered or is authorized"}


    @staticmethod
    def get_user(**kwargs):
        """Method that returns the user object based on the given information"""
        
        # Check if kwargs has the minimum arguments
        for arg in DataAccess.REQ_ARGS.get_user:
            if arg not in kwargs:
                return False
        
        # Get the results from the query
        user_data = DataAccess.USER_COL.find_one(kwargs)

        # Return if the given user is not in the database
        if user_data == None:
            return {"status": "error", "message": "Check your inputted credentials"}
        # Return the user object
        else:
            return {"status": "success", "content": str(User(**user_data))}