import scipy.io as sio
import os
import re
import matplotlib.pyplot as plt
import matlab.engine
eng = matlab.engine.start_matlab()
from obtainFilesText import findFileNames
from patientsClass import Patient

print('Adding Paths....')
eng.loadPath(nargout = 0)
print(' Ignore the Warnings.')
print('\n' * 2)
dataPath = '/Users/talhakhalil/Desktop/Research/Data'

doNotRun = findFileNames(dataPath + '/TossData.rtf')#Removing bad Data from analysis
doNotRun += findFileNames(dataPath + '/FilesWithTests.rtf')#Removing tests from analysis
tracts = findFileNames(dataPath + '/Trajectories.rtf')#Used to find the starting and end point of trajectories

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

#Sorting out Tracts
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
        #y.setName(patientNumber)
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

print(allFiles)


#content = sio.loadmat('/Users/talhakhalil/Desktop/Research/Data/2120/2120-1218auto1_fooof_results.mat')
#struct = content['fooof_results']
#val = struct[0,0]
#exponential = val['background_params'][0][1]
#error = val['error'][0][0]
#r2 = val['r_squared'][0][0]
#peak = val['peak_params']
#peakvalues = []
#for x in peak:
#    peakvalues.append(x[0])

#plt.scatter(0,error)
#plt.savefig('/Users/talhakhalil/Desktop/my_new_figure.png', transparent = False, bbox_inches = 'tight')
#plt.show()

#Saving a figure
#print (val['background_params'])
#print (val['peak_params'])

