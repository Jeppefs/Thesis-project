import numpy as np
import os
from collections import OrderedDict

def CreateParametersAndSettings(func, name, notes):

    if notes == "" and name == "":
        folder, name, parameters, settings, notes = func()
    elif notes == "":
        folder, name, parameters, settings, notes = func(name = name)
    elif name == "":
        folder, name, parameters, settings, notes = func(notes = notes) 
    else:
        folder, name, parameters, settings, notes = func(name = name, notes = notes) 

    fileParam, fileSet, fileNotes = CreateFiles(name)
    CreateNotes(fileNotes, notes)
    fileNotes.close()
    CreateHeader(fileParam, parameters)
    CreateHeader(fileSet, settings) 
    InsertValues(fileParam, parameters)
    InsertValues(fileSet, settings)

    CreateDataAndPlotFolders(name)

    fileParam.close()
    fileSet.close()
    

def CreateFiles(folderName):
    if not os.path.exists("data/" + folderName + "/"):
        os.makedirs("data/" + folderName + "/")

    fileParam = open("data/" + folderName + "/" + "parameters" + ".csv", "w+")
    fileSet = open("data/" + folderName + "/" +  "settings" + ".csv", "w+")
    fileNotes = open("data/" + folderName + "/" +  "notes" + ".txt", "w+")

    return fileParam, fileSet, fileNotes

def CreateNotes(file, notes):
    file.write(notes)
    return


""" Saves the keys onto a header for the given file. """
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
    q.LoopOverThis(i = 0)

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

def CreateDataAndPlotFolders(folderName):
    if not os.path.exists("data/" + folderName + "/plots"):
        os.makedirs("data/" + folderName + "/plots")
    if not os.path.exists("data/" + folderName + "/timeline"):
        os.makedirs("data/" + folderName + "/timeline")
    return

