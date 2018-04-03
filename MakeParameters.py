import numpy as np
from collections import OrderedDict

def CreateFiles(fileName):
    fileParam = open("parameters/"+ fileName + "_param" + ".csv", "w+")
    fileSet = open("parameters/"+ fileName + "_set" + ".csv", "w+")
    return fileParam, fileSet

# Saves the keys onto a header for the given file. 
def CreateHeader(file, aDict):
    for key in aDict:
        file.write(key + ",") 
    file.write("\n")
    return

def InsertValues(file, aDict):
    npArray = MakeNPArrayFromDict(aDict)
    print(npArray)
    for i in range(len(npArray)):
        for j in range(len(aDict)):
            file.write(str(npArray[i][j]) + ",")
        file.write("\n")
    #np.savetxt(file, npArray, delimiter=",")
    return

def MakeNPArrayFromDict(aDict):

    class ProductOfDictCreator():

        def __init__(self, aDict):
            self.lengthOfDict = len(aDict)
            self.values = [None] * len(aDict)
            self.keys = MakeListOfKeys(aDict)
            self.dataArray = MakeEmptyListFromDict(aDict)
            self.aDict = aDict
            self.y = 0

        def LoopOverThis(self, i):
            for self.values[i] in self.aDict[self.keys[i]]:
                if i < self.lengthOfDict - 1:
                    i = self.LoopOverThis(i + 1)
                else:
                    for j in range(self.lengthOfDict):
                        self.dataArray[self.y][j] = self.values[j]
                    self.y += 1
            return i - 1

    q = ProductOfDictCreator(aDict)
    i = 0
    q.LoopOverThis(i)

    return q.dataArray



def MakeListOfKeys(aDict):
    keys = []
    for key in aDict:
        keys.append(key)
    return keys

def MakeEmptyListFromDict(aDict):
    length = 1
    for key, value in aDict.items():
        length = length * len(value)
    EmptyList = []
    for i in range(length):
        EmptyList.append([None] * len(aDict))
    print(EmptyList)
    return EmptyList


folder = "parameters/"
Name = "simplest_infectionRate"

length = 2
width = 1

parameters = OrderedDict()
parameters["NHosts"] = np.array([10000])
parameters["InfectionSpeed"] = np.array([0.99 + float(i)/float(length) for i in range(length)])
#parameters["ImmunitySpeed"] = np.array([1.0])
#parameters["MutationSpeed"] = np.array([0.0])
#parameters["DeathSpeed"] = np.array([0.0])

parameters['NAntigens'] = np.array([1])
parameters['MaxAntigenValue'] = np.array([1])
 
settings = {"SingleFiles": ["false"], "Time": [0], "Runs": [25000000], "BurnIn": [0]}

##

fileParam, fileSet = CreateFiles(Name)
CreateHeader(fileParam, parameters)
CreateHeader(fileSet, settings) 
InsertValues(fileParam, parameters)
InsertValues(fileSet, settings)

fileParam.close()
fileSet.close()