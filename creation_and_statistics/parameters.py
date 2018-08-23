import numpy as np 
from collections import OrderedDict
import make_parameters as mp 

func = "complexDifference"
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
    settings["SpecificStrains"] = ["All"]
    settings["DataFileName"] = ["dataEnd.csv"]

    return folder, name, parameters, settings, notes

def simple(name = "simple", notes = "Infections speed adjusted with resistance at 1 and anything else at zero"):

    folder, name, parameters, settings, notes = standard(name = name, notes = notes)

    parameters["InfectionSpeed"] = np.arange(1.0, 1.05+0.0000001, 0.001)
    settings["Repeat"] = [10] 


    return folder, name, parameters, settings, notes 

def replacement(name = "replacement", notes = "Replacement increases"):
    
    folder, name, parameters, settings, notes = standard(name = name, notes = notes)

    parameters["InfectionSpeed"] = np.array([0.95]) 
    parameters["ReplacementSpeed"] = np.arange(0, 0.005, 0.0001)
    settings["Repeat"] = [10]

    return folder, name, parameters, settings, notes 

def replacement2(name = "replacement2", notes = "Replacement increases large"):
    folder, name, parameters, settings, notes = standard(name = name, notes = notes)

    parameters["InfectionSpeed"] = np.array([0.95]) 
    parameters["ReplacementSpeed"] = np.arange(0, 1.0, 0.005)
    settings["Repeat"] = [10]

    return folder, name, parameters, settings, notes 

def replacement2D(name = "replacement2D", notes = "Loops over infection speed and replacement"):
    folder, name, parameters, settings, notes = standard(name = name, notes = notes)

    parameters["InfectionSpeed"] = np.arange(0.5, 1.10+0.000001, 0.05)
    parameters["ReplacementSpeed"] = np.arange(0, 0.6+0.000001, 0.002)
    
    settings["Repeat"] = [10]
    settings["SkipSaving"] = [2000]
    settings["ShouldSaveDataWhileRunning"] = ["false"]
    
    return folder, name, parameters, settings, notes

def features(name = "features", notes = "Adjusts number of surface features"):
    folder, name, parameters, settings, notes = standard(name = name, notes = notes)
    
    parameters["InfectionSpeed"] = np.array([0.6, 0.8, 0.95])
    parameters["ReplacementSpeed"] = np.array([0.0, 0.005, 0.01, 0.02])
    parameters["MaxAntigenValue"] = np.arange(1, 25+1, 1, dtype=int)
    settings["Repeat"] = [1]
    settings["SkipSaving"] = [2000]

    return folder, name, parameters, settings, notes

def complexFeatures(name = "complexFeatures", notes = "Over the same parameters as features, except antigen size is 2"):
    folder, name, parameters, settings, notes = features(name = name, notes = notes)
    
    parameters["MaxAntigenValue"] = np.arange(2, 25+1, 1, dtype=int)
    parameters["NAntigens"] = np.array([2])
    settings["SkipSaving"] = [2000]

    return folder, name, parameters, settings, notes

def complexFeatures2(name = "complexFeatures2", notes = "Over the same parameters as features, except antigen size is 3"):
    folder, name, parameters, settings, notes = features(name = name, notes = notes)
    
    parameters["MaxAntigenValue"] = np.arange(3, 25+1, 1, dtype=int)
    parameters["NAntigens"] = np.array([3])
    settings["SkipSaving"] = [2000]

    return folder, name, parameters, settings, notes

def complexDifference(name = "complexDifference", notes = "Over the same parameters as features, except antigen size is 3"):
    folder, name, parameters, settings, notes = features(name = name, notes=notes)

    parameters["InfectionSpeed"] = np.array([0.6])
    parameters["ReplacementSpeed"] = np.array([0.01])
    parameters["MaxAntigenValue"] = np.arange([8])
    parameters["NAntigens"] = np.array([2]) 

    settings["SpecificStrains"] = ["other"]
    settings["SkipSaving"] = np.array([2000], dtype=int)
    
    return folder, name, parameters, settings, notes

def featuresMutation(name = "featuresMutation", notes = "Over the same parameters as features, except mutation exist"):
    folder, name, parameters, settings, notes = features(name = name, notes = notes)
    
    parameters["NAntigens"] = np.array([1])
    parameters["InfectionSpeed"] = np.array([0.6])
    parameters["ReplacementSpeed"] = np.array([0.005])
    parameters["MutationSpeed"] = np.array([0.005])


    return folder, name, parameters, settings, notes

##-------------------------------------------------------------------------------##
mp.CreateParametersAndSettings(eval(func), name, notes)
