# Imports
from utils.dict_parse import DictParse
from database.users import UserAccess
from config.config import config
import json

class Unit:
    """Base model unit"""
    
    # Static variable declaration
    REQ_ARGS = config.neededArguments.Unit
    
    def __init__(self, **kwargs):
        """Constructor for base unit"""
        
        # Check if kwargs has the minimum arguments
        for arg in Unit.REQ_ARGS.init:
            if arg not in kwargs:
                return False
            
        # Save info
        self.info = DictParse(kwargs)
    
    def add_member(self, id):
        """Add a new member to the members list"""
        
        # Append the user to the list
        self.info.members.append(id)
        
        # Get the user's instance based from the ID
        user = UserAccess.get_user(obj=True, _id=id)["content"]
        
        # Update user's side if the user is valid for operation
        if user["status"] != "error":
            user.add_unit(self.info.id)
            UserAccess.set_user(_id=user.info._id, value=user.info)
