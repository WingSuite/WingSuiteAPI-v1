from models.statistics.pfa import PFA

a = PFA(
    **{
        "_id": 1234,
        "stat_type": "pfa",
        "from_user": 0,
        "to_user": 1,
        "name": "TEST PFA",
        "datetime_taken": 0,
        "subscores": {"pushup": 78, "situp": 68, "run": "11:07"},
        "info": {"age": 19, "gender": "male"},
    }
)

print(a.info)
