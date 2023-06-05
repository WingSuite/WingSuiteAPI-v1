# Imports
from config.config import permissions
from .base import DataAccessBase
from utils.hash import sha256
from models.user import User
import uuid

class UserAccess(DataAccessBase):
    """Class that handles user information"""
    
    @staticmethod
    def get_user(secure=False, obj=False, **kwargs):
        """Base method for get_user methods"""
        
        # Get the results from the query
        user_data = DataAccessBase.USER_COL.find_one(kwargs)

        # Return if the given user is not in the database
        if user_data == None:
            return {"status": "error", "message": "Check your inputted credentials"}
        
        # Return the user object
        else:
            # Get the content of the user based on wether 
            # we want to get all or some data
            content = User(**user_data).info if not secure else \
                User(**user_data).get_generic_info()
            
            # Return results based on types of representation
            return {
                "status": "success", 
                "content": content if not obj else User(**user_data)
            }
    
    @staticmethod
    def login(**kwargs):
        """Method that returns the user object based on the given user and pass"""
        
        # Check if kwargs has the minimum arguments
        check = DataAccessBase.args_checker(kwargs, "login")
        if check:
            return check
        
        # Hash and save the given password to kwargs
        kwargs["password"] = sha256(
            kwargs["password"], 
            DataAccessBase.CONFIG.database.spicer
        )
        
        # Return user content
        return UserAccess.get_user(secure=True, **kwargs)
    
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
            return {"status": "error", "message": "User did not register"}
        
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
            kwargs["permissions"] = []
            
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
    def change_permission(operation, **kwargs):
        """Add permission values based on the given id"""
        
        # Check if kwargs has the minimum arguments
        check = DataAccessBase.args_checker(kwargs, "change_permission")
        if check:
            return check

        # Check if the permission value is a list 
        if not isinstance(kwargs["permissions"], list):
            return {"status": "error", "message": "Permission value not in list format"}
        
        # Check if the operation value is one of the accepted options
        if operation not in ["add", "delete"]:
            return {"status": "error", "message": "Operation value is not an accepted value"}
        
        # Get user object
        user = UserAccess.get_user(obj=True, _id=kwargs["_id"])["content"]
        
        # Add new permission(s) and track changes
        results = {}
        for permission in kwargs["permissions"]:
            # If the given permission is not part of the approved list of permission
            # track that is is not added with an exaplanation and continue
            if permission not in permissions:
                results[permission] = "Not Added (Invalid Permission)"
                continue
            
            # Attempt add permission
            res = user.add_permission(permission) if operation == "add" else \
                user.delete_permission(permission)
            
            # Track changes
            results[permission] = ("Added" if operation == "add" else "Deleted") \
                if res else "Not Added (Already " + ("Added)" if operation == "add" \
                else "Deleted or is Missing)")
        
        # Update database
        DataAccessBase.USER_COL.update_one(
            {"_id": user.info["_id"]},
            {"$set": {"permissions" : user.info["permissions"]}}
        )
        
        # Return success message
        operation_type = "addition" if operation == "add" else "deletion"
        return {
            "status": "success", 
            "message": 
                f"Permission {operation_type} have been applied to {user.get_fullname(lastNameFirst=True)}. Refer to results for what has been applied",
            "results": results
        }