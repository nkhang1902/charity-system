from flask import request

def getValuesFromBody(key):
    if request.is_json:
        return request.json.get(key)
    return request.values.get(key)