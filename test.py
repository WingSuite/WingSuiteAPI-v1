from models.unit import Unit
from database.unit import UnitAccess
import json


test = Unit(**{
  "name": "Test",
  "type": "flight",
  "parent": "",
  "children": [],
  "officers": [],
  "members": []
})

# print(json.dumps(UnitAccess.create_unit(**test.info), indent=4))

# input()

# print(UnitAccess.get_unit(_id="17ece9492f5e41de95a261a259263c54"))

print(UnitAccess.update_unit(**{"_id": "17ece9492f5e41de95a261a259263c54", "a": 3456}))
