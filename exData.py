import scipy.io as sio
import os
import re
import matplotlib.pyplot as plt
import numpy as np
import matlab.engine
from iteration_utilities import duplicates
from iteration_utilities import unique_everseen
from obtainFilesText import findFileNames
from patientsClass import Patient
from patientsClass import IndividualFile
from patientsClass import mmFile
from patientsClass import FullTract
from getTracts import getTracts # Start, End, allFiles
from getData import getDataForPatient #patient, resultFile, dataPath
from random import uniform
from createFigures import createFigure

print('Adding Paths....')
eng = matlab.engine.start_matlab()
eng.loadPath(nargout = 0)
print(', Ignore the Warnings.')
print('\n' * 2)
dataPath = '/Users/talhakhalil/Desktop/Research/Data'
print('This is your data path, ')


mmToTest = 2 # Value of 0 tests all files

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

print('Do not run files have been removed from analysis!' + '\n'*2)

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
    length = x.getTractLen()
    i = 0
    while i < length:
        tract = FullTract()
        tract.storeTract(getTracts(x.getStartTract(i), x.getEndTract(i), allFiles))
        x.appendAllTrajectory(tract)
        i = i + 1

for x in patientArray:
    getDataForPatient(x, allResultFiles, dataPath)
    print('Trajectories for ' + str(x.getName()) + ' have been stored!')

print('\n'*2 + 'All trajectories have been stored!')

#print(patientArray[0].getAllTrajectory(0).getTract()[0].getResultsFile()[0].getExponent())

dorsalExponents = []
dorsalOffset = []
dorsalR2 = []
dorsalError = []
dorsalPeakFreq = []
dorsalFreqArea = []

ventralExponents = []
ventralR2 = []
ventralOffset = []
ventralError = []
ventralPeakFreq = []
ventralFreqArea = []

for x in patientArray:
    y = 0
    while y < x.getTractLen():
        dorsalIndex = x.getAllTrajectory(y).getTractLen() // 2
        z = 0
        #print('Tract final mm: ' +  str(x.getAllTrajectory(y).getTractLen() - 1))
        while z < dorsalIndex:
            if z == 0:
                z += 1
                continue
            if mmToTest != 0:
                if z > (mmToTest):
                    z += 1
                    continue
            fileIndex = x.getAllTrajectory(y).getTract()[z].getResultsFilesLen()
            q = 0
            while q < fileIndex:
                dorsalExponents.append(x.getAllTrajectory(y).getTract()[z].getResultsFile()[q].getExponent())
                dorsalOffset.append(x.getAllTrajectory(y).getTract()[z].getResultsFile()[q].getOffset())
                dorsalR2.append(x.getAllTrajectory(y).getTract()[z].getResultsFile()[q].getError())
                dorsalError.append(x.getAllTrajectory(y).getTract()[z].getResultsFile()[q].getR2())
                freqIndex = x.getAllTrajectory(y).getTract()[z].getResultsFile()[q].getFreqLen()
                o = 0
                while o < freqIndex:
                    dorsalPeakFreq.append(x.getAllTrajectory(y).getTract()[z].getResultsFile()[q].getFreq()[o])
                    dorsalFreqArea.append(x.getAllTrajectory(y).getTract()[z].getResultsFile()[q].getFreqArea()[o])
                    o += 1
                q += 1
            #print('Used: ' + str(z))
            z += 1

        while z < x.getAllTrajectory(y).getTractLen():
            if z == (x.getAllTrajectory(y).getTractLen() - 1):
                z += 1
                continue
            if mmToTest != 0:
                if z < (x.getAllTrajectory(y).getTractLen() - (mmToTest + 1)):
                    z += 1
                    continue
            fileIndex = x.getAllTrajectory(y).getTract()[z].getResultsFilesLen()
            q = 0
            while q < fileIndex:
                ventralExponents.append(x.getAllTrajectory(y).getTract()[z].getResultsFile()[q].getExponent())
                ventralOffset.append(x.getAllTrajectory(y).getTract()[z].getResultsFile()[q].getOffset())
                ventralR2.append(x.getAllTrajectory(y).getTract()[z].getResultsFile()[q].getError())
                ventralError.append(x.getAllTrajectory(y).getTract()[z].getResultsFile()[q].getR2())
                freqIndex = x.getAllTrajectory(y).getTract()[z].getResultsFile()[q].getFreqLen()
                o = 0
                while o < freqIndex:
                    ventralPeakFreq.append(x.getAllTrajectory(y).getTract()[z].getResultsFile()[q].getFreq()[o])
                    ventralFreqArea.append(x.getAllTrajectory(y).getTract()[z].getResultsFile()[q].getFreqArea()[o])
                    o += 1
                q += 1
            #print('Used: ' + str(z))
            z += 1
        y += 1
    #print('\n')

print('\n'*2 + 'Ignored the first and last mm!')
print('Done seperating into Ventral and Dorsal groups!')
print('Creating Figures!' + '\n'*2)
jitterPlotDorsal = []
jitterPlotVentral = []

num = 0

while num < len(dorsalExponents):
    jitterPlotDorsal.append(uniform(-0.1, 0.1))
    num += 1

num = 0

while num < len(ventralExponents):
    jitterPlotVentral.append(uniform(-0.1, 0.1))
    num += 1


binPeak = [0,10,20,30,40,50,60]
binArea = [0,1,2,3,4,5,6,7,8,9,10]
pointAlpha = 0.2

print('Points in Dorsal: ' + str(len(jitterPlotDorsal)))
print('Points in Ventral: ' + str(len(jitterPlotVentral)) + '\n'*2)

createFigure('Dorsal',dataPath, jitterPlotDorsal, dorsalError, dorsalExponents,dorsalOffset, dorsalR2, dorsalPeakFreq, dorsalFreqArea, binPeak, binArea, pointAlpha)
createFigure('Ventral',dataPath, jitterPlotVentral, ventralError, ventralExponents,ventralOffset, ventralR2, ventralPeakFreq, ventralFreqArea, binPeak, binArea, pointAlpha)


print('\n'*2 + 'Saved figures in ' + dataPath + '!')
plt.show()
print('Done!')

#plt.savefig('/Users/talhakhalil/Desktop/my_new_figure.png', transparent = False, bbox_inches = 'tight')
#plt.show()

#Saving a figure
#print (val['background_params'])
#print (val['peak_params'])

