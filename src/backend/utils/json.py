import json
import os
import time

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
    files = data.get("files", {})
    sortedFiles = sorted(
        files.items(), 
        key=lambda x: x[1].get("created", 0), 
        reverse=True
    )
    return [name for name, _ in sortedFiles]

def getFileContent(file, fileName):
    data = readJSON(file)
    return data.get("files", {}).get(fileName, {}).get("content", "")

def saveFileContent(file, fileName, content):
    data = readJSON(file)
    if "files" not in data:
        data["files"] = {}
    
    if fileName not in data["files"]:
        data["files"][fileName] = {
            "content": content,
            "created": time.time()
        }
    else:
        data["files"][fileName]["content"] = content
        
    writeJSON(file, data)

def renameFileEntry(file, oldName, newName):
    data = readJSON(file)
    if oldName in data.get("files", {}) and newName not in data["files"]:
        data["files"][newName] = data["files"].pop(oldName)
        writeJSON(file, data)
        return True
    return False

def deleteFileEntry(file, fileName):
    data = readJSON(file)
    if fileName in data.get("files", {}):
        del data["files"][fileName]
    writeJSON(file, data)
