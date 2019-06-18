import scipy.io as sio
import os
import re
import matplotlib.pyplot as plt
import matlab.engine
from iteration_utilities import duplicates
from iteration_utilities import unique_everseen
from obtainFilesText import findFileNames
from patientsClass import Patient
from patientsClass import IndividualFile
from patientsClass import mmFile
from getTracts import getTracts # Start, End, allFiles
from getData import getDataForPatient #patient, resultFile, dataPath

print('Adding Paths....')
eng = matlab.engine.start_matlab()
eng.loadPath(nargout = 0)
print(', Ignore the Warnings.')
print('\n' * 2)
dataPath = '/Users/talhakhalil/Desktop/Research/Data'
print('This is your data path, ' + dataPath)

doNotRun = findFileNames(dataPath + '/TossData.txt')#Removing bad Data from analysis
doNotRun += findFileNames(dataPath + '/FilesWithTests.txt')#Removing tests from analysis
tracts = findFileNames(dataPath + '/Trajectories.txt')#Used to find the starting and end point of trajectories
doNotRun.sort()

fileDirectory = []
for root, dirs, files in os.walk(dataPath):
    for file in files:
        if file.endswith('_fooof_results.mat'):
            fileDirectory.append(os.path.join(root, file)) #stored the directory with the name.

fileNameResult = re.compile(r'(\d\d\d\d-\d\d\d\d)([ABCDEF])?(auto)?(\d)?(\d)?');
fileName = re.compile(r'(\d\d\d\d-\d\d\d\d)([ABCDEF])?');

allFiles = []
for x in fileDirectory:
    name = fileName.search(x)
    if name!= None and name not in allFiles:
        allFiles.append(name[0])
allFiles = list(unique_everseen(duplicates(allFiles)))
allFiles.sort()

allResultFiles = []
for x in fileDirectory:
    name = fileNameResult.search(x)
    if name!= None and name not in allResultFiles:
        allResultFiles.append(name[0])
allResultFiles.sort()

for x in doNotRun:
    name = fileNameResult.search(x)
    if name[3] == None:
        for y in allResultFiles:
            remove = fileName.search(y)
            if x == remove[0]:
                allResultFiles.remove(y)
    else:
        try:
            allResultFiles.remove(x)
        except:
            continue

print('Do not run files have been removed from analysis!')

startTract = []
endTract = []
endOfTrajectory = False #used to filp flop between start and end points as the text file is written in this way
for x in tracts:
    if endOfTrajectory == True:
        endTract.append(x)
        endOfTrajectory = False
    else:
        startTract.append(x)
        endOfTrajectory = True

#Finding all the patient numbers using Tracts, done in case we need to create figures per patient, or any other method of sorting
patientArray = []
oldPatient = 0
findPatientNumber = re.compile(r'(\d\d\d\d)(-)')

for x in startTract:
    patientNumber = findPatientNumber.search(x)
    patientNumber = int(patientNumber.group(1))
    if patientNumber != oldPatient:
        y = Patient(patientNumber)
        patientArray.append(y)
        oldPatient = patientNumber

for x in startTract:
    patientNumber = findPatientNumber.search(x)
    patientNumber = int(patientNumber.group(1))
    for y in patientArray:
        if y.getName() == patientNumber:
            y.appendStartTract(x)

for x in endTract:
    patientNumber = findPatientNumber.search(x)
    patientNumber = int(patientNumber.group(1))
    for y in patientArray:
        if y.getName() == patientNumber:
            y.appendEndTract(x)

for x in patientArray:
    len = x.getTractLen()
    i = 0
    while i < len:
        x.storeTract(i, getTracts(x.getStartTract(i), x.getEndTract(i), allFiles))
        i = i + 1

for x in patientArray:
    getDataForPatient(x, allResultFiles, dataPath)
    print('Trajectories for ' + str(x.getName()) + ' have been stored!')

print('All trajectories have been stored!')
#plt.scatter(0,error)
#plt.savefig('/Users/talhakhalil/Desktop/my_new_figure.png', transparent = False, bbox_inches = 'tight')
#plt.show()

#Saving a figure
#print (val['background_params'])
#print (val['peak_params'])

