import re

def findFileNames(filePath):
    findFileNames =[] #A set is faster for searching through
    fileName = re.compile(r'(\d\d\d\d-\d\d\d\d)([ABCDEF])?(auto)?(\d)?(\d)?')
    file = open(filePath, 'r')
    fileContent = file.read()
    toAdd = fileName.findall(fileContent)
    for x in toAdd:
        y = x[0] + x[1] + x[2] + x[3] + x[4]
        findFileNames.append(y)
    return findFileNames
