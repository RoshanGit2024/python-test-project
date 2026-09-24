def convert_salary(data):
    """
    Convert the salary field from Decimal to float for MongoDB insertion.
    """
    if "salary" in data:
        data["salary"] = float(data["salary"])
    return data