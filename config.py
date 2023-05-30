# Import(s)
import json

def Config(config):
    """
    Convert dictionary into instance allowing access to dictionary keys using
    dot notation (attributes).
    """
    
    class ConfigObject(dict):
        """
        Represents configuration options' group, works like a dict
        """
        def __init__(self, *args, **kwargs):
            dict.__init__(self, *args, **kwargs)
        def __getattr__(self, name):
            return self[name]
        def __setattr__(self, name, val):
            self[name] = val

    # Return requested information
    if isinstance(config, dict):
        result = ConfigObject()
        for key in config:
            result[key] = Config(config[key])
        return result
    else:
        return config

# Export config
config = Config(json.load(open("config.json")))