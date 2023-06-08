from models.unit import Unit
from database.unit import UnitAccess
import json


test = Unit(**{
  "id": "1234",
  "name": "Test",
  "type": "flight",
  "parent": "",
  "children": [],
  "officers": [],
  "members": []
})

print(json.dumps(UnitAccess.create_unit(**test.info), indent=4))
