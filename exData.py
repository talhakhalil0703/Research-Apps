#Modules needed, scipy, matplotlib, iteration_utilities, you also need the loadPath matlab inside it you can see what modules in matlab you need
#Talha Khalil June 2019

import scipy.io as sio
import os
import re
import matplotlib.pyplot as plt
import matlab.engine
from iteration_utilities import duplicates
from iteration_utilities import unique_everseen
from random import uniform

from obtainFilesText import findFileNames
from patientsClass import Patient
from patientsClass import IndividualFile
from patientsClass import mmFile
from patientsClass import FullTract
from getTracts import getTracts # Start, End, allFiles
from getData import getDataForPatient #patient, resultFile, dataPath
from createFigures import createFigure

print('Adding Paths....')
eng = matlab.engine.start_matlab()
eng.loadPath(nargout = 0)
print(', Ignore the Warnings.')
print('\n' * 2)
dataPath = '/Users/talhakhalil/Desktop/Research/Data'
print('This is your data path, ' + dataPath)

mmToTest = int(input('How many mm do you want to test? (0, would mean to test all!)\n'))
print('Going to test: ' + str(mmToTest) + 'mm')

binPeak = [0,10,20,30,40,50,60] #These are the bin edges for the peak frequencies figures, you can change these to change how the histogram looks
binArea = [0,1,2,3,4,5,6,7,8,9,10] #Same as above but for the frequency areas
pointAlpha = 0.2 # This is the tranparency of the points on the scatter plots

#These are all the lists that will end up holding the data for the use of figure creation, they are not really organized in a good manner. You can get specific data points by using the class Patient
dorsalExponents = []
dorsalOffset = []
dorsalR2 = []
dorsalError = []
dorsalAverageExponents = []
dorsalAverageOffset = []
dorsalAverageR2 = []
dorsalAverageError = []
dorsalPeakFreq = []
dorsalFreqArea = []

ventralExponents = []
ventralR2 = []
ventralOffset = []
ventralError = []
ventralAverageExponents = []
ventralAverageR2 = []
ventralAverageOffset = []
ventralAverageError = []
ventralPeakFreq = []
ventralFreqArea = []

jitterAveragePlotDorsal = []
jitterAveragePlotVentral = []

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

for x in patientArray:
    y = 0
    while y < x.getTractLen():
        dorsalIndex = x.getAllTrajectory(y).getTractLen() // 2
        z = 0
        avgExponent = []
        avgOffset = []
        while z < dorsalIndex:
            if z == 0: #ignoring the first mm
                z += 1
                continue
            if mmToTest != 0:
                if z > (mmToTest):
                    z += 1
                    continue
            fileIndex = x.getAllTrajectory(y).getTract()[z].getResultsFilesLen()
            dorsalAverageExponents.append(x.getAllTrajectory(y).getTract()[z].getAverageExponent())
            dorsalAverageOffset.append(x.getAllTrajectory(y).getTract()[z].getAverageOffset())
            dorsalAverageR2.append(x.getAllTrajectory(y).getTract()[z].getAverageR2())
            dorsalAverageError.append(x.getAllTrajectory(y).getTract()[z].getAverageError())
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
            z += 1

        while z < x.getAllTrajectory(y).getTractLen():
            if z == (x.getAllTrajectory(y).getTractLen() - 1): #ignoring the last mm
                z += 1
                continue
            if mmToTest != 0:
                if z < (x.getAllTrajectory(y).getTractLen() - (mmToTest + 1)):
                    z += 1
                    continue
            fileIndex = x.getAllTrajectory(y).getTract()[z].getResultsFilesLen()
            ventralAverageExponents.append(x.getAllTrajectory(y).getTract()[z].getAverageExponent())
            ventralAverageOffset.append(x.getAllTrajectory(y).getTract()[z].getAverageOffset())
            ventralAverageR2.append(x.getAllTrajectory(y).getTract()[z].getAverageR2())
            ventralAverageError.append(x.getAllTrajectory(y).getTract()[z].getAverageError())
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
            z += 1
        y += 1

print('\n'*2 + 'Ignored the first and last mm!')
print('Done seperating into Ventral and Dorsal groups!')
print('Creating Figures!' + '\n'*2)

num = 0

while num < len(dorsalAverageExponents):
    jitterAveragePlotDorsal.append(uniform(-0.1, 0.1))
    num += 1

num = 0

while num < len(ventralAverageExponents):
    jitterAveragePlotVentral.append(uniform(-0.1, 0.1))
    num += 1

print('Points in Dorsal: ' + str(len(jitterAveragePlotDorsal)))
print('Points in Ventral: ' + str(len(jitterAveragePlotVentral)) + '\n'*2)

#The bin edges and the alpha for the scatter plots can be changed at the top of the file called, binPeak, binArea, and pointAlpha

createFigure('Dorsal' + str(mmToTest) + 'mm',dataPath, jitterAveragePlotDorsal, dorsalAverageError, dorsalAverageExponents,dorsalAverageOffset, dorsalAverageR2, dorsalPeakFreq, dorsalFreqArea, binPeak, binArea, pointAlpha)
createFigure('Ventral' + str(mmToTest) + 'mm',dataPath, jitterAveragePlotVentral, ventralAverageError, ventralAverageExponents,ventralAverageOffset, ventralAverageR2, ventralPeakFreq, ventralFreqArea, binPeak, binArea, pointAlpha)

print('\n'*2 + 'Saved figures in ' + dataPath + '!')
plt.show()
print('Done!')
