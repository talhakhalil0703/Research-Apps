import re
import scipy.io as sio
from patientsClass import IndividualFile

fileName = re.compile(r'(\d\d\d\d-\d\d\d\d)([ABCDEF])?');

def getDataFromIndividualFile(patient, file, dataPath):
    content = sio.loadmat(dataPath + '/' + str(patient.getName()) + '/' + file + '_fooof_results.mat')
    struct = content['fooof_results']
    tempFile = IndividualFile(file)
    val = struct[0,0]
    tempFile.setExponent(val['background_params'][0][1])
    tempFile.setOffset(val['background_params'][0][0])
    tempFile.setError(val['error'][0][0])
    tempFile.setR2(val['r_squared'][0][0])
    peak = val['peak_params']
    for x in peak:
        tempFile.appendFreq(x[0])
        tempFile.appendFreqArea(x[1]*x[2])
    return tempFile

def getDataForPatient(Patient, resultFiles, dataPath, tolerance):
    x = 0
    while x < Patient.getTractLen():
        tract = Patient.getAllTrajectory(x)
        tractLen = tract.getTractLen()
        y = 0
        while y < tractLen: #mmFile in tract
            for individualFile in resultFiles:
                if tract.getTract()[y].getName() == fileName.search(individualFile)[0]:
                    file = getDataFromIndividualFile(Patient, individualFile, dataPath)
                    if file.getR2() >= tolerance:
                        tract.getTract()[y].appendResultsFiles(file)
            y += 1

        tractLen = tract.getTractLen()
        y = 0
        while y < tractLen:
            if tract.getTract()[y].getResultsFilesLen() == 0:
                tract.removeTract(tract.getTract()[y])
                tractLen -= 1
            else:    
                y += 1
        x = x + 1


