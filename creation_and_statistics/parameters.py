import numpy as np 
from collections import OrderedDict
import make_parameters as mp 

func = "standard"
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
    settings["Repeat"] = [1]
    settings["ShouldSaveData"] = ["true"]
    settings["ShouldSaveDataWhileRunning"] = ["true"]
    settings["ShouldCreateNewDataFile"] = ["true"]
    settings["DataFileName"] = ["dataEnd.csv"]

    return folder, name, parameters, settings, notes


##-------------------------------------------------------------------------------##
mp.CreateParametersAndSettings(eval(func), name, notes)


