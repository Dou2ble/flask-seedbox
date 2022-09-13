import os

def type(path):
    if os.path.isdir(path):
        return "folder"

    elif os.path.isfile(path):
        return "file"