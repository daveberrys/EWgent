import json

def getKey(file, key):
    with open(file, 'r') as f:
        data = json.load(f)
        return data[key]

def saveKey(file, key, value):
    with open(file, 'w') as f:
        data = json.load(f)
        data[key] = value
        json.dump(data, f)

def deleteKey(file, key):
    with open(file, 'w') as f:
        data = json.load(f)
        del data[key]
        json.dump(data, f)