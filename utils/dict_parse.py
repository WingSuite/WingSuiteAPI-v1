# Imports
from typing import Any


def DictParse(config: dict):
    """
    Convert dictionary into instance allowing access to dictionary keys using
    dot notation (attributes).
    """

    class ConfigObject(dict):
        """
        Represents configuration options' group, works like a dict
        """

        def __init__(self: "ConfigObject", *args: Any, **kwargs: Any) -> None:
            """Initialization of the parsed dictionary"""
            dict.__init__(self, *args, **kwargs)

        def __getattr__(self: "ConfigObject", name: str) -> Any:
            """Get attribute"""
            return self[name]

        def __setattr__(self: "ConfigObject", name: str, val: Any) -> Any:
            """Set attribute"""
            self[name] = val

        def __delattr__(self: "ConfigObject", name: str) -> Any:
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
