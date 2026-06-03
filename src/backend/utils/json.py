import json
import os

def readJSON(file):
    if not os.path.exists(file):
        return {"files": {}}
    with open(file, "r") as f:
        return json.load(f)

def writeJSON(file, data):
    os.makedirs(os.path.dirname(file), exist_ok=True)
    with open(file, "w") as f:
        json.dump(data, f, indent=2)

def getAllFileNames(file):
    data = readJSON(file)
    return list(data.get("files", {}).keys())

def getFileContent(file, fileName):
    data = readJSON(file)
    return data.get("files", {}).get(fileName, {}).get("content", "")

def saveFileContent(file, fileName, content):
    data = readJSON(file)
    if "files" not in data:
        data["files"] = {}
    data["files"][fileName] = {"content": content}
    writeJSON(file, data)

def deleteFileEntry(file, fileName):
    data = readJSON(file)
    if fileName in data.get("files", {}):
        del data["files"][fileName]
    writeJSON(file, data)
