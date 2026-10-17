from config.mongodb import db
from pymongo import ReturnDocument
def convert_salary(data):
    """
    Convert the salary field from Decimal to float for MongoDB insertion.
    """
    if "salary" in data:
        data["salary"] = float(data["salary"])
    return data

def uniqueId_generate():
        counter = db.counters.find_one_and_update(
             {"_id": "employee_id"},{"$inc": {"seq": 1}},upsert=True,return_document=ReturnDocument.AFTER)
        employee_id = 1000 + counter["seq"]
        return employee_id