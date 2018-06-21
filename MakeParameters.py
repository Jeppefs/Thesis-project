import numpy as np
import os
from collections import OrderedDict

def CreateFiles(folderName):
    if not os.path.exists("data/" + folderName + "/"):
        os.makedirs("data/" + folderName + "/")

    fileParam = open("data/" + folderName + "/" + "parameters" + ".csv", "w+")
    fileSet = open("data/" + folderName + "/" +  "settings" + ".csv", "w+")
    return fileParam, fileSet

# Saves the keys onto a header for the given file. 
def CreateHeader(file, aDict):
    i = 0
    for key in aDict:
        if i < len(aDict) - 1:
            file.write(key + ",") 
        else:
            file.write(key)
        i += 1
    file.write("\n")
    return

def InsertValues(file, aDict):
    npArray = MakeNPArrayFromDict(aDict)
    print(npArray)
    for i in range(len(npArray)):
        for j in range(len(aDict)):
            if j < len(aDict) - 1:
                file.write(str(npArray[i][j]) + ",")
            else:
                file.write(str(npArray[i][j]))
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
    for _, value in aDict.items():
        length = length * len(value)
    EmptyList = []
    for _ in range(length):
        EmptyList.append([None] * len(aDict))
    return EmptyList

def MakeParametersAndSettings():

    folder = "data"
    name = "test_other"

    length = 1
    width = 1
    parameters = OrderedDict()
    
    parameters["NHosts"] = np.array([10000])
    parameters["InfectionSpeed"] = np.array([1.0])
    parameters["ImmunitySpeed"] = np.array([1.0])
    parameters["MutationSpeed"] = np.array([0.0])
    parameters["DeathSpeed"] = np.array([0.00])

    parameters['NAntigens'] = np.array([i+1 for i in range(3)])
    parameters['MaxAntigenValue'] = np.array([1])
    parameters['InitialInfected'] = np.array([100])

    parameters['IsMultipleInfectionsPossible'] = np.array(["true"])

    settings = OrderedDict()
    settings["Runs"] = [2500000] 
    settings["BurnIn"] = [0]
    settings["Repeat"] = [1]
    settings["ShouldSaveData"] = ["true"]
    settings["ShouldSaveDataWhileRunning"] = ["true"] 
    settings["ShouldCreateNewDataFile"] = ["true"]
    settings["DataFileName"] = ["data/" + "endData"]

    return folder, name, parameters, settings

folder, name, parameters, settings = MakeParametersAndSettings()

##

fileParam, fileSet = CreateFiles(name)
CreateHeader(fileParam, parameters)
CreateHeader(fileSet, settings) 
InsertValues(fileParam, parameters)
InsertValues(fileSet, settings)

fileParam.close()
fileSet.close()