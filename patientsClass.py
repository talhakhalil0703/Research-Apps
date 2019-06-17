class Patient:
    def __init__(self, name):
        self.__name = name
        self.__startTract = []
        self.__endTract = []
    

    def setName(self, name):
        self.__name = name
    def getName(self):
        return self.__name
    def appendStartTract(self, tract):
        self.__startTract.append(tract)
    def getStartTract(self):
        return self.__startTract
    def appendEndTract(self, tract):
        self.__endTract.append(tract)
    def getEndTract(self):
        return self.__endTract

class mmFile:
    
    __exponent = None
    __r2 = None
    __error = None
    __peakFreq = [] #Peak frequencies
    __freqArea = [] #Take two values and multiply and store here
    
    def appendFreq(self, frequency):
        self.__peakFreq.append(frequency)
    def appendFreqArea(self, area):
        self.__freqArea.append(area)
    def setExponent(self, exp):
        self.__exponent = exp
    def setR2(self, rsq):
        self.__r2 = rsq
    def setError(self, err):
        self.__error = err
    def getFreq(self):
        return self.__peakFreq
    def getFreqArea(self):
        return self.__freqArea
    def getExponent(self):
        return self.__exponent
    def getR2(self):
        return self.__r2
    def getError(self):
        return self.__error

