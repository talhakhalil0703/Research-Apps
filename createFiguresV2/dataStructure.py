class Patient:
    def __init__(self, name):
        self.__name = name
        self.__startTrajectory = []
        self.__endTrajectory = []
        self.__Trajectories = []  # contains all the mm files from which to extract data

    def setName(self, name):
        self.__name = name

    def getName(self):
        return self.__name

    def appendStartTrajectory(self, tract):
        self.__startTrajectory.append(tract)

    def getStartTrajectory(self, i):
        return self.__startTrajectory[i]

    def appendEndTrajectory(self, tract):
        self.__endTrajectory.append(tract)

    def getEndTrajectory(self, i):
        return self.__endTrajectory[i]

    def getTrajectoryLen(self):
        return len(self.__startTrajectory)

    def appendAllTrajectory(self, tract):
        self.__Trajectories.append(tract)

    def getAllTrajectory(self, int):
        return self.__Trajectories[int]


class FullTrajectory:
    def __init__(self):
        self.__Trajectory = []

    def storeTrajectory(self, tract):
        self.__Trajectory = tract.copy()

    def getTrajectory(self):
        return self.__Trajectory

    def removeTrajectory(self, i):
        self.__Trajectory.remove(i)

    def getTrajectoryLen(self):
        return len(self.__Trajectory)


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
        self.__peakFreq = []  # Peak frequencies
        self.__freqArea = []  # Take two values and multiply and store here

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
    return sum(list) / len(list)
