import os.path

def getFileSize(path:str):
    return int(os.path.getsize(path)/1024)


