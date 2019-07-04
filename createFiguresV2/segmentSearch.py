import os
import re

fileNameResult = re.compile(r'(\d\d\d\d-\d\d\d\d)([ABCDEF])?(auto)?(\d)?(\d)?')
fileName = re.compile(r'(\d\d\d\d-\d\d\d\d)([ABCDEF])?')

def searchForSegments(dataPath):
    fileDirectory = []
    allResultFiles = []

    for root, dirs, files in os.walk(dataPath):
        for file in files:
            if file.endswith('_fooof_results.mat'):
                fileDirectory.append(os.path.join(root, file))

    for x in fileDirectory:
        name = fileNameResult.search(x)
        if name is not None and name not in allResultFiles:
            allResultFiles.append(name[0])
        allResultFiles.sort()

    return allResultFiles

def removeSegments(resultsList, removeList):

    for x in removeList:
    name = fileNameResult.search(x)
    if name[3] is None:
        for y in resultsList:
            remove = fileName.search(y)
            if x == remove[0]:
                 resultsList.remove(y)
    else:
        try:
            resultsList.remove(x)
        except:
            continue

    return
