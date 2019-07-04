import re

def findFileNames(filePath):
    findFileNames =[] #A set is faster for searching through
    fileName = re.compile(r'(\d\d\d\d-\d\d\d\d)([ABCDEF])?(auto)?(\d)?(\d)?')
    with open(filePath, 'r') as file
        fileContent = file.read()
    
    toAdd = fileName.findall(fileContent)
    for x in toAdd:
        y = x[0] + x[1] + x[2] + x[3] + x[4]
        findFileNames.append(y)
    findFileNames.sort()
    
    return findFileName
