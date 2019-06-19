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

def getDataForPatient(Patient, resultFiles, dataPath):
    x = 0
    while x < Patient.getTractLen():
        tract = Patient.getAllTrajectory(x)
        tract = tract.getTract()
        for mmFile in tract:
            for individualFile in resultFiles:
                if mmFile.getName() == fileName.search(individualFile)[0]:
                    mmFile.appendResultsFiles(getDataFromIndividualFile(Patient, individualFile, dataPath))
        
        x = x + 1


