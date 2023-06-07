# Import(s)
from utils.dict_parse import DictParse
import json

# Export configs
permissions = set(json.load(open("./config/permissions.json")))
config = DictParse(json.load(open("./config/config.json")))