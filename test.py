# from models.unit import Unit

# test = Unit(**{
#   "id": "1234",
#   "name": "Test",
#   "type": "flight",
#   "parent": None,
#   "children": None,
#   "officers": [],
#   "members": []
# })

# test.add_member(id="5832ed31a3e741cc8bc625c6ae6b3c41")

# print(test.info)

def foo(a, b, **kwargs):
  print(kwargs)
  
foo(**{"a": 2, "b": 3, "c": 2})