import os

def extension(path):
    if os.path.isfile(path):
        return "file/" + path.split(".")[-1]

    elif os.path.isdir(path):
        return "file/folder"
    
    else:
        return "file/other"