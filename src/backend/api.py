import webview as wv
import sys
import os
from pyder import *
import json

from src.backend.utils.json import getAllFileNames, getFileContent, saveFileContent, deleteFileEntry

class API:
    def __init__(self):
        self.appID = f"{pyder_domainSystem}.{pyder_projectID}"
        self._maximized = False
        self._saved_geometry = None

    def getWindow(self):
        activeWindow = wv.active_window()

        if activeWindow:
            return activeWindow
        elif len(wv.windows) > 0:
            return wv.windows[0]
        else:
            return None
    
    def getConfigPath(self):
        if sys.platform == "win32":
            configPath = os.path.join(os.getenv("APPDATA"), self.appID)
        elif sys.platform == "darwin":
            configPath = os.path.join(os.getenv("HOME"), "Library", "Application Support", self.appID)
        elif sys.platform == "linux":
            configPath = os.path.join(os.getenv("HOME"), ".config", self.appID)
        else:
            configPath = os.path.join(os.getenv("HOME"), ".config", self.appID)
        return configPath

    # system stuff
    def exitApp(self):
        currentWindow = self.getWindow()

        if currentWindow == None:
            print("Window was null. App could not exit.")
            return None
        else:
            currentWindow.destroy()
            exit()
    def maximizeApp(self):
        currentWindow = self.getWindow()

        if currentWindow == None:
            print("Window was null. App could not maximize.")
            return None

        def unmaximize(window):
            native = getattr(window, 'native', None)
            _unmaximize = getattr(native, 'unmaximize', None)
            if callable(_unmaximize):
                _unmaximize()

        if self._maximized:
            unmaximize(currentWindow)
            self._maximized = False
        else:
            currentWindow.maximize()
            self._maximized = True
        return True
    def minimizeApp(self):
        currentWindow = self.getWindow()

        if currentWindow == None:
            print("Window was null. App could not minimize.")
            return None
        else:
            currentWindow.minimize()
            return True

    # file management
    def getDataPath(self):
        return os.path.join(self.getConfigPath(), "data.json")
    def appInit(self):
        configPath = self.getConfigPath()
        configFile = os.path.join(configPath, "data.json")
        if not os.path.exists(configPath):
            os.makedirs(configPath)
        if not os.path.exists(configFile):
            with open(configFile, "w") as f:
                json.dump({}, f)
        return
    def getFiles(self):
        return getAllFileNames(self.getDataPath())
    def getFileContent(self, fileName):
        return getFileContent(self.getDataPath(), fileName)
    def saveFile(self, fileName, content):
        saveFileContent(self.getDataPath(), fileName, content)
        return True
    def deleteFile(self, fileName):
        deleteFileEntry(self.getDataPath(), fileName)
        return True
    def copyToClipboard(self, text):
        import subprocess, sys, os
        try:
            #sonion i'm crine
            if sys.platform == "darwin":
                p = subprocess.Popen(["pbcopy"], stdin=subprocess.PIPE)
            elif sys.platform == "win32":
                p = subprocess.Popen(["clip"], stdin=subprocess.PIPE, shell=True)
            elif os.system("which xclip > /dev/null 2>&1") == 0:
                p = subprocess.Popen(["xclip", "-selection", "clipboard"], stdin=subprocess.PIPE)
            elif os.system("which wl-copy > /dev/null 2>&1") == 0:
                p = subprocess.Popen(["wl-copy"], stdin=subprocess.PIPE)
            else:
                return False
            p.communicate(input=text.encode("utf-8"))
            return True
        except Exception:
            return False