# Imports
from config.config import config
import json

class User:
    """User class model"""
    
    # Static variable declaration
    REQ_ARGS = config.neededArguments.DataAccess
    
    def __init__(self, **kwargs):
        """Constructor for the User class"""
        
        # Check if kwargs has the minimum arguments
        for arg in User.REQ_ARGS.add_user:
            if arg not in kwargs:
                return False
        
        # Save info
        self.info = kwargs
    
    def get_generic_info(self):
        """Returns content that doesn't include any security concerns"""
        return {k: v for k, v in self.info.items() if k not in config.privateInfo}
    
    def get_fullname(self, lastNameFirst):
        """Returns the user's full name"""
        
        # Get the user's names
        first_name = self.info["first_name"]
        last_name = self.info["last_name"]
        middle_initial = ""
        if "middle_initial" in list(self.info.keys()):
            middle_initial = " " + self.info["middle_initial"]
        
        # Return different styles based on given options
        if lastNameFirst:
            return (f"{last_name}, {first_name}{middle_initial}")
        else:
            return(f"{first_name}{middle_initial} {last_name}")
    
    def add_permission(self, permission):
        "Add new permissions to the user"
        
        # If the given permission is already in the permissions list, return false
        if permission in self.info["permissions"]:
            return False
            
        # If not existent, append the new permissions to the list and return true
        else:
            self.info["permissions"].append(permission)
            return True
    
    def delete_permission(self, permission):
        "Remove permission to the user"
        
        # If the given permission is already in the permissions list, remove and return true
        if permission in self.info["permissions"]:
            self.info["permissions"].remove(permission)
            return True
            
        # If not existent, append the new permission to the list and return true
        else:
            return False