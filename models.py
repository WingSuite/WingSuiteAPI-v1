# Imports
from config import config
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
        
    def __repr__(self):
        """Return a string representation of itself"""
        return json.dumps(self.info, indent=4)
    
    def get_fullname(self, lastNameFirst):
        """Returns the user's full name"""
        
        # Get the user's names
        first_name = self.info["first_name"]
        last_name = self.info["last_names"]
        middle_initial = ""
        if "middle_initial" in list(self.info.keys()):
            middle_initial = self.info["middle_initial"]
        
        # Return different styles based on given options
        if lastNameFirst:
            return (f"{last_name}, {first_name} {middle_initial}")
        else:
            return(f"{first_name} {last_name} {middle_initial}")