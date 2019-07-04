import time 
import numpy

from brainSectionClass import brainSection
from obtianFilesText import findFileNames

def getAverageOfList(list):
   return sum(list)/len(list)

def exData (stringDataPath, stringR2, PeakArray, AreaArray, stringAlpha, stringMMToChoose):
    
    before = time.time()
    
    dataPath =  stringDataPath
    r2Tolerance = float(stringR2)
    p1 = PeakArray[0]
    p2 = PeakArray[1]
    p3 = PeakArray[2]
    binPeak = list(numpy.arange(p1,p2,p3))
    p1 = AreaArray[0]
    p2 = AreaArray[1]
    p3 = AreaArray[2]
    binArea = list(numpy.arange(p1,p2,p3))
    maxMM = int(stringMMToChoose)
    pointAlpha = float(stringAlpha)

    print('Adding MatLab Path...')
    matlabEngine = matlab.engine.start_matlab()
    matlabEngine.laodPath(nargout = 0)
    print('This is your data path: ' +  dataPath)
    print('Going to test ' + string(maxMM) + ' away from the middle!')

    dorsal = brainSection('Dorsal')
    ventral = brainSection('Ventral')

    doNotRunSection = findFileNames(dataPath + '/TossData.txt')
    doNotRunMM = findFileNames(dataPath + '/mmToNotRun.txt')
    trajectories = findFileNames(dataPath + 'Trajectories.txt')


