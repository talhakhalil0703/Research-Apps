class brainSection:
    def __init__(self, name):
        self.__name = name
        self.__exponents = []
        self.__offset = []
        self.__r2 = []
        self.__error = []
        self.__averageExponents = []
        self.__averageOffset = []
        self.__averageR2 = []
        self.__averageError = []
        self.__peakFreq = []
        self.__freqArea = []

    def getExponents(self):
        return self.__exponents
    def getOffset(self):
        return self.__offset
    def getR2(self):
        return self.__r2
    def getError(self):
        return self.__error
    def getAverageExponents(self):
        return self.__averageExponents
    def getAverageOffset(self):
        return self.__averageOffset
    def getAverageR2(self):
        return self.__averageR2
    def getAverageError(self):
        return self.__averageError
    def getPeakFreq(self):
        return self.__peakFreq
    def getFreqArea(self):
        return self.__freqArea
    def appendExponents(self, i):
        return self.__exponents.append(i)
    def appendOffset(self, i):
        return self.__offset.append(i)
    def appendR2(self, i):
        return self.__r2.append(i)
    def appendError(self, i):
        return self.__error.append(i)
    def appendAverageExponents(self, i):
        return self.__averageExponents.append(i)
    def appendAverageOffset(self, i):
        return self.__averageOffset.append(i)
    def appendAverageR2(self, i):
        return self.__averageR2.append(i)
    def appendAverageError(self, i):
        return self.__averageError.append(i)
    def appendPeakFreq(self, i):
        return self.__peakFreq.append(i)
    def appendFreqArea(self, i):
        return self.__freqArea.append(i)
