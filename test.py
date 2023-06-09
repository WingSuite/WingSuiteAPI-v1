# from models.unit import Unit
# from database.unit import UnitAccess
# from utils.dict_parse import DictParse
# import json


# test = Unit(
#     **{
#         "_id": "1234",
#         "name": "Test",
#         "unit_type": "flight",
#         "parent": "",
#         "children": [],
#         "officers": [],
#         "members": [],
#     }
# )

# # a = DictParse(test)

# # print(UnitAccess.get_unit("74943ec7241642988275f769b3fe13db").message)

# # print(json.dumps(UnitAccess.create_unit(**test.info), indent=4))

# # # input()

# # print(UnitAccess.delete_unit("74943ec7241642988275f769b3fe13db"))

# # print(UnitAccess.update_unit("74943ec7241642988275f769b3fe13db",
# #   **{"_id": "74943ec7241642988275f769b3fe13db",
# #   "a": 3456}))

# # def some_func(a, b, c=3, *args, **kwargs):
# #     params = {k: v for k, v in locals().items()
# #               if k not in ["kwargs", "args"]}
# #     params.update(locals()["kwargs"])
# #     print({...params, "Test":})

# # some_func(1, 2, d=6, e=7)