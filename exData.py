import time
import os
import re
import matlab.engine
from iteration_utilities import duplicates
from iteration_utilities import unique_everseen
import openpyxl
import numpy

from obtainFilesText import findFileNames
from patientsClass import Patient
from patientsClass import FullTract
from getTracts import getTracts  # Start, End, allFiles
from getData import getDataForPatient  # patient, resultFile, dataPath
# name to save as, datapath, dorsal/ventral, bin for peak, bin for area, alpha
# for point, and boolean to determine if you want to use the average values for
# the mm or to use each file
from createFigures import createFigure
from extractData import extractDataFromMiddle
from extractData import getDataGreatestLength
from storeExcelData import storeExcelData
from brainSectionClass import brainSection
from createFigures import createSlopeMM

def exData(stringDataPath, stringR2, PeakArray, AreaArray, stringAlpha, stringMMToChoose):
    before = time.time()

    # Modules needed, scipy, matplotlib, iteration_utilities, you also need the
    # loadPath matlab inside it you can see what modules in matlab you need
    # Talha Khalil June 2019


    def getAverage(list):
        return sum(list) / len(list)


    print('Adding Matlab Paths....')
    eng = matlab.engine.start_matlab()
    eng.loadPath(nargout=0)
    dataPath = stringDataPath
    print('This is your data path, ' + dataPath)

    # mmToTest = int(input('How many mm do you want to test?
    # (0, would mean to test all!)\n'))
    R2tolerance = float(stringR2)

    mmToTest = 0
    if mmToTest == 0:
        print('Going to test: All mm')
    else:
        print('Going to test: ' + str(mmToTest) + 'mm')

    # These are the bin edges for the peak frequencies figures, you can change
    # these to change how the histogram looks
    p1 = PeakArray[0]
    p2 = PeakArray[1]
    p3 = PeakArray[2]
    binPeak = list(numpy.arange(p1,p2,p3))
    # Same as above but for the frequency areas
    p1 = AreaArray[0]
    p2 = AreaArray[1]
    p3 = AreaArray[2]
    binArea = list(numpy.arange(p1,p2,p3))
    pointAlpha = float(stringAlpha)  # This is the tranparency of the points on the scatter plots

    maxMM = int(stringMMToChoose)
    # These are all the lists that will end up holding the data for the use of
    # figure creation, they are not really organized in a good manner. You can
    # get specific data points by using the class Patient
    dorsal = brainSection('Dorsal')
    ventral = brainSection('Ventral')

    # Removing bad Data from analysis
    doNotRun = findFileNames(dataPath + '/TossData.txt')
    # Removing tests from analysis
    doNotRun += findFileNames(dataPath + '/FilesWithTests.txt')
    # Used to find the starting and end point of trajectories
    tracts = findFileNames(dataPath + '/Trajectories.txt')
    doNotRun.sort()

    fileDirectory = []
    for root, dirs, files in os.walk(dataPath):
        for file in files:
            if file.endswith('_fooof_results.mat'):
                # stored the directory with the name.
                fileDirectory.append(os.path.join(root, file))

    fileNameResult = re.compile(r'(\d\d\d\d-\d\d\d\d)([ABCDEF])?(auto)?(\d)?(\d)?')
    fileName = re.compile(r'(\d\d\d\d-\d\d\d\d)([ABCDEF])?')

    allFiles = []
    for x in fileDirectory:
        name = fileName.search(x)
        if name is not None and name not in allFiles:
            allFiles.append(name[0])
    allFiles = list(unique_everseen(duplicates(allFiles)))
    allFiles.sort()

    allResultFiles = []
    for x in fileDirectory:
        name = fileNameResult.search(x)
        if name is not None and name not in allResultFiles:
            allResultFiles.append(name[0])
    allResultFiles.sort()

    for x in doNotRun:
        name = fileNameResult.search(x)
        if name[3] is None:
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
    # used to filp flop between start and end points as the text file is written
    # in this way
    endOfTrajectory = False
    for x in tracts:
        if endOfTrajectory is True:
            endTract.append(x)
            endOfTrajectory = False
        else:
            startTract.append(x)
            endOfTrajectory = True

    # Finding all the patient numbers using Tracts, done in case we need to
    # create figures per patient, or any other method of sorting
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
            tract.storeTract(getTracts(x.getStartTract(i),
                                       x.getEndTract(i), allFiles))
            x.appendAllTrajectory(tract)
            i = i + 1

    wb = openpyxl.Workbook()
    for x in patientArray:
        getDataForPatient(x, allResultFiles, dataPath, R2tolerance)
        storeExcelData(x, wb)
    print('Trajectories have been stored!')

    # The bin edges and the alpha for the scatter plots can be changed at the top
    # of the file called, binPeak, binArea, and pointAlpha

    slopeMM = [None] * maxMM * 2
    sheet = wb.create_sheet('Patients Average Data')
    if mmToTest == 0:
        greatestLength = getDataGreatestLength(patientArray, dorsal, ventral)
        print('Cutout a mm from ventral to make length even for tracts!')
        print('Creating Figures!')
        q = 1
        while q <= maxMM:
            dorsal = brainSection('Dorsal')
            ventral = brainSection('Ventral')
            extractDataFromMiddle(patientArray, dorsal, ventral, q)
            slopeMM[maxMM -q] = dorsal.getExponents()
            slopeMM[maxMM - 1 + q] = ventral.getExponents()
            sheet['A' + str(q)] = 'Points in: ' + \
                str(len(dorsal.getAverageError()))
            sheet['B' + str(q)] = 'Dorsal Slope Average For : ' + str(q) + ' mm'
            sheet['C' + str(q)] = getAverage(dorsal.getAverageExponents())
            sheet['D' + str(q)] = 'Dorsal Offset Average For : ' + str(q) + ' mm'
            sheet['E' + str(q)] = getAverage(dorsal.getAverageOffset())
            sheet['F' + str(q)] = 'Ventral Slope Average For : ' + str(q) + ' mm'
            sheet['G' + str(q)] = getAverage(ventral.getAverageExponents())
            sheet['H' + str(q)] = 'Ventral Offset Average For : ' + str(q) + ' mm'
            sheet['I' + str(q)] = getAverage(ventral.getAverageOffset())
            createFigure('Dorsal ' + str(q) + ' mm', dataPath,
                         dorsal, binPeak, binArea, pointAlpha, True)
            createFigure('Ventral ' + str(q) + ' mm', dataPath,
                         ventral, binPeak, binArea, pointAlpha, True)
            q += 1
    else:
        extractDataFromMiddle(patientArray, dorsal, ventral, mmToTest)
        createFigure('Dorsal ' + str(mmToTest) + ' mm', dataPath,
                     dorsal, binPeak, binArea, pointAlpha, True)
        createFigure('Ventral ' + str(mmToTest) + ' mm', dataPath,
                     ventral, binPeak, binArea, pointAlpha, True)
    print('Loading Figures!')
    print('Saving Excel Files')
    wb.save(dataPath + '/Patients Data.xlsx')
    print('Saved figures in ' + dataPath + '!')
    createSlopeMM('SlopesMM', dataPath, slopeMM)
    after = time.time()
    print('Done! Time taken: ' + str(int(after - before)) + ' seconds')
