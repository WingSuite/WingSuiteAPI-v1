def DictParse(config):
    """
    Convert dictionary into instance allowing access to dictionary keys using
    dot notation (attributes).
    """

    class ConfigObject(dict):
        """
        Represents configuration options' group, works like a dict
        """

        def __init__(self, *args, **kwargs):
            """Initialization of the parsed dictionary"""
            dict.__init__(self, *args, **kwargs)

        def __getattr__(self, name):
            """Get attribute"""
            return self[name]

        def __setattr__(self, name, val):
            """Set attribute"""
            self[name] = val

        def __delattr__(self, name):
            """Delete attribute"""
            del self[name]

    # Return requested information
    if isinstance(config, dict):
        result = ConfigObject()
        for key in config:
            result[key] = DictParse(config[key])
        return result
    else:
        return config
