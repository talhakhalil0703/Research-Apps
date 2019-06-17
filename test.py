import os
import re
dataPath = '/Users/talhakhalil/Desktop/Research/Data'


fileDirectory = []
for root, dirs, files in os.walk(dataPath):
    for file in files:
        if file.endswith('.smr'):
            fileDirectory.append(os.path.join(root, file)) #stored the directory with the name.

fileName = re.compile(r'(\d\d\d\d-\d\d\d\d)([ABCDEFabcdef])?');
allFiles = []
for x in fileDirectory:
    name = fileName.search(x)
    if name!= None:
        allFiles.append(name[0])



