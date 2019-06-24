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
import openpyxl

from obtainFilesText import findFileNames
from patientsClass import Patient
from patientsClass import IndividualFile
from patientsClass import mmFile
from patientsClass import FullTract
from getTracts import getTracts # Start, End, allFiles
from getData import getDataForPatient #patient, resultFile, dataPath
from createFigures import createFigure# name to save as, datapath, dorsal/ventral, bin for peak, bin for area, alpha for point, and boolean to determine if you want to use the average values for the mm or to use each file
from extractData import extractData #Patient Array, Dorsal, Ventral, mmToTest
from extractData import extractDataFromMiddle
from extractData import getDataGreatestLength
from brainSectionClass import brainSection

def getAverage(list):
    return sum(list)/len(list)

print('Adding Paths....')
eng = matlab.engine.start_matlab()
eng.loadPath(nargout = 0)
print(', Ignore the Warnings.')
print('\n' * 2)
dataPath = '/Users/talhakhalil/Desktop/Research/Data'
print('This is your data path, ' + dataPath)

#mmToTest = int(input('How many mm do you want to test? (0, would mean to test all!)\n'))
mmToTest = 0
if mmToTest == 0 :
    print('Going to test: All mm')
else:
    print('Going to test: ' + str(mmToTest) + 'mm')

binPeak = [0,10,20,30,40,50,60] #These are the bin edges for the peak frequencies figures, you can change these to change how the histogram looks
binArea = [0,1,2,3,4,5,6,7,8,9,10] #Same as above but for the frequency areas
pointAlpha = 0.2 # This is the tranparency of the points on the scatter plots

#These are all the lists that will end up holding the data for the use of figure creation, they are not really organized in a good manner. You can get specific data points by using the class Patient
dorsal = brainSection('Dorsal')
ventral = brainSection('Ventral')

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


#The bin edges and the alpha for the scatter plots can be changed at the top of the file called, binPeak, binArea, and pointAlpha

wb = openpyxl.Workbook()
sheet = wb.create_sheet('Patients Average Data')
if mmToTest == 0:
    greatestLength = getDataGreatestLength(patientArray, dorsal, ventral)
    print(greatestLength)
    q = 1
    while q <= greatestLength:
        dorsal = brainSection('Dorsal')
        ventral = brainSection('Ventral')
        extractDataFromMiddle(patientArray, dorsal, ventral, q)
        sheet['A' + str(q)] = 'Points in: ' + str(len(dorsal.getAverageError()))
        sheet['B' + str(q)] = 'Dorsal Slope Average For : ' + str(q) + ' mm'
        sheet['C' + str(q)] = getAverage(dorsal.getAverageExponents())
        sheet['D' + str(q)] = 'Dorsal Offset Average For : ' + str(q) + ' mm'
        sheet['E' + str(q)] = getAverage(dorsal.getAverageOffset())
        sheet['F' + str(q)] = 'Ventral Slope Average For : ' + str(q) + ' mm'
        sheet['G' + str(q)] = getAverage(ventral.getAverageExponents())
        sheet['H' + str(q)] = 'Ventral Offset Average For : ' + str(q) + ' mm'
        sheet['I' + str(q)] = getAverage(ventral.getAverageOffset())
        createFigure('Dorsal ' + str(q) + ' mm',dataPath, dorsal, binPeak, binArea, pointAlpha, True)
        createFigure('Ventral ' + str(q) + ' mm',dataPath, ventral, binPeak, binArea, pointAlpha, True)
        q += 1
else:
    extractDataFromMiddle(patientArray, dorsal, ventral, mmToTest)
    createFigure('Dorsal ' + str(mmToTest) + ' mm',dataPath, dorsal, binPeak, binArea, pointAlpha, True)
    createFigure('Ventral ' + str(mmToTest) + ' mm',dataPath, ventral, binPeak, binArea, pointAlpha, True)

print('Creating Figures!')
print('Creating Excel Files')
wb.save(dataPath + '/Average Patient Data.xlsx')
print('\n'*2 + 'Saved figures in ' + dataPath + '!')
#plt.show()
print('Done!')
