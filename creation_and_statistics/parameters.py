import numpy as np 
from collections import OrderedDict
import make_parameters as mp 

func = "simple"
name = ""
notes = ""

##-------------------------------------------------------------------------------##
def standard(name = "standard", notes = "Standard data for non-systematic tests"):
    
    folder = "data"
    
    parameters = OrderedDict()
    parameters["NHosts"] = np.array([10000])
    parameters["InfectionSpeed"] = np.array([1.0]) 
    parameters["ImmunitySpeed"] = np.array([1.0])
    parameters["ReplacementSpeed"] = np.array([0.0])
    parameters["MutationSpeed"] = np.array([0.0])
    parameters["NAntigens"] = np.array([1])
    parameters["MaxAntigenValue"] = np.array([1])
    parameters["MaxSuperInfections"] = np.array([5])
    parameters["InitialInfected"] = np.array([500])

    settings = OrderedDict()
    settings["Runs"] = [20000000] 
    settings["BurnIn"] = [0]
    settings["SkipSaving"] = [500]
    settings["Repeat"] = [1]
    settings["ShouldSaveData"] = ["true"]
    settings["ShouldSaveDataWhileRunning"] = ["true"]
    settings["ShouldCreateNewDataFile"] = ["true"]
    settings["DataFileName"] = ["dataEnd.csv"]

    return folder, name, parameters, settings, notes

def simple(name = "simple", notes = "Infections speed adjusted with resistance at 1 and anything else at zero"):

    folder, name, parameters, settings, notes = standard(name = name, notes = notes)

    parameters["InfectionSpeed"] = np.arange(1.0, 1.05+0.0000001, 0.001)
    settings["Repeat"] = [10] 


    return folder, name, parameters, settings, notes 

def replacement(name = "replacement", notes = "Replacement increases"):
    
    folder, name, parameters, settings, notes = standard(name = name, notes = notes)

    parameters["InfectionSpeed"] = np.array([0.99]) 
    parameters["ReplacementSpeed"] = np.arange(0, 0.01, 0.0001)

    return folder, name, parameters, settings, notes 

def complexFun(name = "complexFun", notes = "Adjusts number of possible antigens, with strain length of 2."):
    
    folder = "data"
    
    parameters = OrderedDict()
    parameters["NHosts"] = np.array([10000])
    parameters["InfectionSpeed"] = np.array([0.98]) 
    parameters["ImmunitySpeed"] = np.array([1.0])
    parameters["ReplacementSpeed"] = np.array([0.0])
    parameters["MutationSpeed"] = np.array([0.0])
    parameters["NAntigens"] = np.array([2])
    parameters["MaxAntigenValue"] = np.array([2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
    parameters["MaxSuperInfections"] = np.array([5])
    parameters["InitialInfected"] = np.array([500])

    settings = OrderedDict()
    settings["Runs"] = [20000000]
    settings["BurnIn"] = [0]
    settings["SkipSaving"] = [500]
    settings["Repeat"] = [1]
    settings["ShouldSaveData"] = ["true"]
    settings["ShouldSaveDataWhileRunning"] = ["true"]
    settings["ShouldCreateNewDataFile"] = ["true"]
    settings["DataFileName"] = ["dataEnd.csv"]

    return folder, name, parameters, settings, notes

def complexFunReplacement(name = "complexFunReplacement", notes = "Adjusts number of possible antigens, with strain length of 2. and with replacement existing."):
    
    folder = "data"
    
    folder, name, parameters, settings, notes = simple(name, notes)

    parameters["NHosts"] = np.array([10000])
    parameters["InfectionSpeed"] = np.array([0.95]) 
    parameters["ImmunitySpeed"] = np.array([1.0])
    parameters["ReplacementSpeed"] = np.array([0.001])
    parameters["NAntigens"] = np.array([2])
    parameters["MaxAntigenValue"] = np.array([2,3,4,5,6,7,8,9,10])

    return folder, name, parameters, settings, notes


##-------------------------------------------------------------------------------##
mp.CreateParametersAndSettings(eval(func), name, notes)
