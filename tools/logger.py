import shutil, os, errno

isDebug=False
def debugOn():
    global isDebug
    isDebug=True

def Print(thing):
    if isDebug:
        print(thing)