# Import(s)
from utils.dict_parse import DictParse
import json

# Export configs
permissions = set(json.load(open("./config/permissions.json")))
arguments = DictParse(json.load(open("./config/arguments.json")))
config = DictParse(json.load(open("./config/config.json")))
html_map = DictParse(json.load(open("./config/html_map.json")))
