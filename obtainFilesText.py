import re

def findFileNames(filePath):
    findFileNames =[] #A set is faster for searching through
    fileName = re.compile(r'(\d\d\d\d-\d\d\d\d)([ABCDEF])?(auto)?(\d)?')
    file = open(filePath, 'r')
    fileContent = file.read()
    toAdd = fileName.findall(fileContent)

    for x in toAdd:
        string  = ''
        for y in x:
            string += str(y)
        findFileNames.append(string)

    return findFileNames
