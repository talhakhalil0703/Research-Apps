import re
from obtianFilesText import findFileNames
from dataStructure import Patient

findPatientNumber = re.compile(r'(\d\d\d\d)(-)')

def findStartEndTrajectories(dataPath):

    trajectories = findFileNames(dataPath + 'Trajectories.txt')
    startTract = []
    endTract = []
    endOfTrajectory = False

    for x in tracts:
        if endOfTrajectory is True:
            endTrajectories.append(x)
            endOfTrajectory = False
        else:
           startTrajectories.append(x)
           endOfTrajectory = True

    return startTrajectories, endTrajectories

def createPatientArrayWithTrajectories(dataPath):

    startTrajectories, endTrajectories = findStartEndTrajectories(dataPath)
    patientArray = []
    oldPatient = 0
    patientNumber = None

    for startTrajectory, endTrajectory in zip(startTrajectories, endTrajectories):
        patientNumber = findPatientNumber.search(startTrajectory)
        patientNumber = int(patientNumber.group(1))

        if patientNumber != oldPatient:
            y = Patient(patientNumber)
            y.appendStartTrajectory(startTrajectory)
            y.appendEndTrajectory(endTrajectory)
            patientArray.append(y)
            oldPatient = patientNumber

    for x in patientArray:
        length = x.getTractLen()
        i = 0
        while i < length:
            tract = FullTract()
            tract.storeTract(getTracts(x.getStartTract(i),
                                       x.getEndTract(i), allFiles))
            x.appendAllTrajectory(tract)
            i = i + 1
