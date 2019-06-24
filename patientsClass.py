class Patient:
    def __init__(self, name):
        self.__name = name
        self.__startTract = []
        self.__endTract = []
        self.__Tracts = [] #contains all the mm files from which to extract data

    def setName(self, name):
        self.__name = name
    def getName(self):
        return self.__name
    def appendStartTract(self, tract):
        self.__startTract.append(tract)
    def getStartTract(self, i):
        return self.__startTract[i]
    def appendEndTract(self, tract):
        self.__endTract.append(tract)
    def getEndTract(self, i):
        return self.__endTract[i]
    def getTractLen(self):
        return len(self.__startTract)
    def appendAllTrajectory(self, tract):
        self.__Tracts.append(tract)
    def getAllTrajectory (self, int):
        return self.__Tracts[int]

class FullTract:
    def __init__(self):
        self.__Tract = []

    def storeTract(self, tract):
        self.__Tract = tract.copy()
    def getTract (self):
        return self.__Tract
    def removeTract(self, i):
        del(self.__Tract[i])
    def getTractLen(self):
        return len(self.__Tract)

class mmFile:
    def __init__(self, name):
        self.__name = name
        self.__resultsFiles = []

    def appendResultsFiles(self, file):
        self.__resultsFiles.append(file)
    def getResultsSingleFile(self, fileName):
        i = self.__resultsFiles.index(fileName)
        return self.__resultsFiles(i)
    def getResultsFile(self):
        return self.__resultsFiles
    def getName(self):
        return self.__name
    def getResultsFilesLen(self):
        return len(self.__resultsFiles)
    def getAverageExponent(self):
        sum = []
        for x in self.__resultsFiles:
            sum.append(x.getExponent())
        return average(sum)
    def getAverageOffset(self):
        sum = []
        for x in self.__resultsFiles:
            sum.append(x.getOffset())
        return average(sum)
    def getAverageR2(self):
        sum = []
        for x in self.__resultsFiles:
            sum.append(x.getR2())
        return average(sum)
    def getAverageError(self):
        sum = []
        for x in self.__resultsFiles:
            sum.append(x.getError())
        return average(sum)

class IndividualFile:
    def __init__(self, name):
        self.__name = name
        self.__exponent = None
        self.__offset = None
        self.__r2 = None
        self.__error = None
        self.__peakFreq = [] #Peak frequencies
        self.__freqArea = [] #Take two values and multiply and store here
    
    def appendFreq(self, frequency):
        self.__peakFreq.append(frequency)
    def appendFreqArea(self, area):
        self.__freqArea.append(area)
    def setExponent(self, exp):
        self.__exponent = exp
    def setOffset(self, off):
        self.__offset = off
    def setR2(self, rsq):
        self.__r2 = rsq
    def setError(self, err):
        self.__error = err
    def getFreq(self):
        return self.__peakFreq
    def getFreqLen(self):
        return len(self.__peakFreq)
    def getFreqArea(self):
        return self.__freqArea
    def getExponent(self):
        return self.__exponent
    def getOffset(self):
        return self.__offset
    def getR2(self):
        return self.__r2
    def getError(self):
        return self.__error
    def getName(self):
        return self.__name

def average(list):
    return sum(list)/len(list)

