from models.statistics.feedback import Feedback

b = {
    "_id": "Test",
    "feedback_type": "Regular",
    "feedback_id": 1234,
    "from": "C/Borden",
    "to": "C/Herrera",
    "name": "Test Feedback",
    "feedback": "Test",
}

a = Feedback(**b).info

print(a)
