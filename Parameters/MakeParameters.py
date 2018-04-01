import numpy as np

def CreateFiles(fileName):
    fileParam = open("parameters/"+"fileName" + "_param" + ".csv", "w+")
    fileSet = open("parameters/"+"fileName" + "_set" + ".csv", "w+")
    return fileParam, fileSet

# Saves the keys onto a header for the given file. 
def CreateHeader(file, aDict):
    for key in aDict:
        file.write(key + ",") 
    return

def InsertValues(file, aDict):
    for key, value in aDict.items():
        for i in range(len(value)):
            
def CrateNPArrayFromDict(aDict):
    xLines = len(aDict)
    yLines = 0
    for key, value in aDict.items():
        yline = yLine * len(value)
    
    array = np.zeros(xLines,yLines)

    for key in aDict:
        x = 0
        for y in yLines:
            array[x, y] = 
            x += 1 

    return array
    


    [key, len]

Name = "simplest_infectionRate"

parameters = {} 
parameters["NHosts"] = np.array([10000])
parameters["InfectionSpeed"] = np.array([0.99 + float(i)/float(length) for i in range(100)])
parameters["ImmunitySpeed"] = np.array([1.0])
parameters["MutationSpeed"] = np.array([0.0])
parameters["DeathSpeed"] = np.array([0.0])

parameters['NAntigens'] = np.array([1])
parameters['MaxAntigenValue'] = np.array([1])
 
settings = {"SingleFiles": "false", "Time": 0, "Runs": 25000000, "BurnIn": 0}

##

fileParam, fileSet = CreateFiles(Name)
CreateHeader(fileParam, parameters)
CreateHeader(fileSet, settings) 
InsertValues(fileParam, parameters, length, width)
InsertValues(fileSet, settings)