# Imports
from .base import DataAccessBase
from models.user import User
from utils.hash import sha256
import uuid

class UserAccess(DataAccessBase):
    """Class that handles user information"""
    
    @staticmethod
    def get_user(**kwargs):
        """Method that returns the user object based on the given information"""
        
        # Check if kwargs has the minimum arguments
        check = DataAccessBase.args_checker(kwargs, "get_user")
        if check:
            return check
        
        # Hash and save the given password to kwargs
        kwargs["password"] = sha256(
            kwargs["password"], 
            DataAccessBase.CONFIG.database.spicer
        )
        
        # Get the results from the query
        user_data = DataAccessBase.USER_COL.find_one(kwargs)

        # Return if the given user is not in the database
        if user_data == None:
            return {"status": "error", "message": "Check your inputted credentials"}
        # Return the user object
        else:
            return {
                "status": "success", 
                "content": User(**user_data).get_generic_info()
            }
    
    @staticmethod
    def add_user(**kwargs):
        """Method that handles adding a user to the system"""
  
        # Check if kwargs has the minimum arguments
        check = DataAccessBase.args_checker(kwargs, "add_user")
        if check:
            return check

        # Add user to the list and return success if the given 
        # information is not the system
        user = DataAccessBase.REGISTER_COL.find_one({"email": kwargs["email"]})
        if user != None:   
            # Insert user into the database, remove from REGISTER_COL and return success
            DataAccessBase.USER_COL.insert_one(user)
            DataAccessBase.REGISTER_COL.delete_one({"email": kwargs["email"]})
            return {"status": "success", "message": "User added to the system"}
        # Return false if the given information exists
        else:
            return {"status": "error", "message": "User didn't register"}
        
    @staticmethod
    def register_user(**kwargs):
        """Method that handles registering a user to the system"""
  
        # Check if kwargs has the minimum arguments
        check = DataAccessBase.args_checker(kwargs, "register_user")
        if check:
            return check
    
        # Add user to the list and return success if the given 
        # information is not the system
        if DataAccessBase.USER_COL.find_one({"email": kwargs["email"]}) == None and \
        DataAccessBase.REGISTER_COL.find_one({"email": kwargs["email"]}) == None:
            # Prep data to be inserted
            kwargs["_id"] = uuid.uuid4().hex
            
            # Hash and save the given password
            kwargs["password"] = sha256(
                kwargs["password"], 
                DataAccessBase.CONFIG.database.spicer
            )
   
            # Insert user into the database and return success
            DataAccessBase.REGISTER_COL.insert_one(kwargs)
            return {"status": "success", "message": "User is up for authorization"}
        # Return false if the given information exists
        else:
            return {"status": "error", "message": "User has registered or is authorized"}
    
    @staticmethod
    def add_permission(**kwargs):
        pass