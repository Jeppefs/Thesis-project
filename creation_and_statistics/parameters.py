import numpy as np 
from collections import OrderedDict
import make_parameters as mp 

func = "replacement"
name = ""
notes = ""

def OptimalGamma(a):
    return (2*a)**(1/3) - 1

##-------------------------------------------------------------------------------##
def standard(name = "standard", notes = "Standard data for non-systematic tests"):
    
    folder = "data"
    
    parameters = OrderedDict()
    parameters["NHosts"] = np.array([10000], dtype=int)
    parameters["InfectionSpeed"] = np.array([1.0]) 
    parameters["ImmunitySpeed"] = np.array([1.0])
    parameters["ReplacementSpeed"] = np.array([0.0])
    parameters["MutationSpeed"] = np.array([0.0])
    parameters["NAntigens"] = np.array([1])
    parameters["MaxAntigenValue"] = np.array([1])
    parameters["MaxSuperInfections"] = np.array([5])
    parameters["InitialInfected"] = np.array([500])
    parameters["SpecificStrains"] = ["all"]

    settings = OrderedDict()
    settings["Runs"] = [20000000] 
    settings["BurnIn"] = [0]
    settings["SkipSaving"] =  np.array([int(parameters["NHosts"][0] / 10)])
    settings["Repeat"] = [1]
    settings["ShouldSaveData"] = ["true"]
    settings["ShouldSaveDataWhileRunning"] = ["true"]
    settings["ShouldCreateNewDataFile"] = ["true"]
    
    settings["DataFileName"] = ["dataEnd.csv"]

    return folder, name, parameters, settings, notes

def simple(name = "simple", notes = "Infections speed adjusted with resistance at 1 and anything else at zero"):

    folder, name, parameters, settings, notes = standard(name = name, notes = notes)

    parameters["InfectionSpeed"] = np.arange(1.0, 1.05+0.0000001, 0.001) # skip with 0.001
    settings["Repeat"] = [10] 


    return folder, name, parameters, settings, notes 

def simpleBigN(name = "simpleBigN", notes="Same as simple, but with N=100000"):

    folder, name, parameters, settings, notes = simple(name = name, notes = notes)

    parameters["NHosts"] = np.array([100000], dtype=int)
    settings["Runs"] = [200000000] 

    return folder, name, parameters, settings, notes

def replacement(name = "replacement", notes = "Replacement increases"):
    
    folder, name, parameters, settings, notes = standard(name = name, notes = notes)

    parameters["InfectionSpeed"] = np.array([0.6, 0.8, 0.95, 1.05]) 
    parameters["ReplacementSpeed"] = np.arange(0, 1.0+0.0001, 0.01)
    settings["Repeat"] = [10]

    return folder, name, parameters, settings, notes 

def replacement2D(name = "replacement2D", notes = "Loops over infection speed and replacement"):
    folder, name, parameters, settings, notes = standard(name = name, notes = notes)

    parameters["InfectionSpeed"] = np.arange(0.5, 1.10+0.000001, 0.05)
    parameters["ReplacementSpeed"] = np.arange(0, 0.6+0.000001, 0.002)
    
    settings["Repeat"] = [1]
    settings["ShouldSaveDataWhileRunning"] = ["false"]
    
    return folder, name, parameters, settings, notes

def features(name = "features", notes = "Adjusts number of surface features"):
    folder, name, parameters, settings, notes = standard(name = name, notes = notes)
    
    parameters["InfectionSpeed"] = np.array([0.6, 0.8, 0.95, 1.05])
    parameters["ReplacementSpeed"] = np.array([0]) # This should only be for the corresponding infection. How do we make that???
    parameters["MaxAntigenValue"] = np.arange(1, 25+1, 1, dtype=int)
    settings["Repeat"] = [1]

    return folder, name, parameters, settings, notes

def features2D(name = "features2D", notes = "Adjusts number of surface features and infection rate, to see at what limit it becomes extinct"):
    folder, name, parameters, settings, notes = standard(name = name, notes = notes)

    parameters["InfectionSpeed"] = np.arange(0.5,0.8+0.01,0.01)
    parameters["ReplacementSpeed"] = np.array([0]) # Optimal Gamma
    parameters["MaxAntigenValue"] = np.arange(1, 25+1, 1, dtype=int)

    settings["Repeat"] = [1]
    settings["SkipSaving"] = [2000]
    settings["ShouldSaveDataWhileRunning"] = ["false"] 

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

def complexDifference(name = "complexDifference", notes = "Trying with cross immunity and not"):
    folder, name, parameters, settings, notes = standard(name = name, notes=notes)

    parameters["InfectionSpeed"] = np.array([0.6])
    parameters["ReplacementSpeed"] = np.array([0.005])
    parameters["SpecificStrains"] = ["nonCross", "cross"] 
    
    settings["Repeat"] = [10]
    settings["SkipSaving"] = np.array([2000], dtype=int)
    
    return folder, name, parameters, settings, notes

def complexDifference2D(name = "complexDifference2D", notes = "Trying with cross immunity and not for different alphas and replacement"):
    folder, name, parameters, settings, notes = standard(name = name, notes=notes)

    parameters["InfectionSpeed"] = np.arange(0.5,0.8+0.01,0.01)
    parameters["ReplacementSpeed"] = np.arange(0.0,0.02+0.001, 0.001)
    parameters["SpecificStrains"] = ["nonCross", "cross"] 
    
    settings["Repeat"] = [1]
    settings["ShouldSaveDataWhileRunning"] = ["false"] 
    settings["SkipSaving"] = np.array([2000], dtype=int)
    
    return folder, name, parameters, settings, notes

def mutation2D(name = "mutation2D", notes = "Search over muation and infection speed"):
    folder, name, parameters, settings, notes = standard(name = name, notes = notes)

    parameters["InfectionSpeed"] = parameters["InfectionSpeed"] = np.arange(0.5,0.8+0.01,0.01)
    parameters["ReplacementSpeed"] = np.array([0.005])
    parameters["MutationSpeed"] = np.arange(0.0,0.01+0.0001, 0.0002)
    parameters["NAntigens"] = np.array([2])
    parameters["MaxAntigenValue"] = np.array([4])

    settings["Repeat"] = [1]
    settings["ShouldSaveDataWhileRunning"] = ["false"] 
    settings["SkipSaving"] = np.array([2000], dtype=int)

    return folder, name, parameters, settings, notes

def featuresMutation(name = "featuresMutation", notes = "Over the same parameters as features, except mutation exist"):
    folder, name, parameters, settings, notes = features(name = name, notes = notes)
    
    parameters["MutationSpeed"] = np.array([0.005])

    return folder, name, parameters, settings, notes

def featuresMutationLow(name = "featuresMutationLow", notes = "Over the same parameters as features, except mutation exist with 0.0005"):
    folder, name, parameters, settings, notes = features(name = name, notes = notes)
    
    parameters["MutationSpeed"] = np.array([0.0005])

    return folder, name, parameters, settings, notes

def featuresMutationVeryLow(name = "featuresMutationVeryLow", notes = "Over the same parameters as features, except mutation exist with 0.0005"):
    folder, name, parameters, settings, notes = features(name = name, notes = notes)
    
    parameters["MutationSpeed"] = np.array([0.0001])

    return folder, name, parameters, settings, notes

def complexDifferenceMutation2D(name = "complexDifferenceMutation2D", notes = "Same as complexDifference2D but with mutation."):
    folder, name, parameters, settings, notes = complexDifference2D(name = name, notes = notes)

    parameters["MutationSpeed"] = np.array([0.0005])

    return folder, name, parameters, settings, notes



##-------------------------------------------------------------------------------##
mp.CreateParametersAndSettings(eval(func), name, notes)
