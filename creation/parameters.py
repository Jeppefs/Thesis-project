import numpy as np 
import pandas as pandas
from collections import OrderedDict
import make_parameters as mp 

func = "crossNonCrossInjectionFast"
name = ""
notes = ""
SameyGamma = True
b = 2/3
factor = 1.0

def OptimalGamma(a, b = 1.0):
    return (2.0*a*b**2.0)**(1.0/3.0) - b

##--------------------------------------------- ----------------------------------##
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
    parameters["ReplacementSpeed"] = np.array([0]) # This should only be for the corresponding infection.
    parameters["MaxAntigenValue"] = np.arange(1, 20+0.1, 1, dtype=int)
    settings["Repeat"] = [10]

    return folder, name, parameters, settings, notes

def features2D(name = "features2D", notes = "Adjusts number of surface features and infection rate, to see at what limit it becomes extinct"):
    folder, name, parameters, settings, notes = standard(name = name, notes = notes)

    parameters["InfectionSpeed"] = np.arange(0.5,0.8+0.01,0.01)
    parameters["ReplacementSpeed"] = np.array([0]) # Optimal Gamma
    parameters["MaxAntigenValue"] = np.arange(1, 20+0.1, 1, dtype=int)

    settings["Repeat"] = [1]
    settings["SkipSaving"] = [2000]
    settings["ShouldSaveDataWhileRunning"] = ["false"] 

    return folder, name, parameters, settings, notes

def mutation(name = "mutation", notes = "Over the same parameters as features, except mutation exist"):
    folder, name, parameters, settings, notes = features(name = name, notes = notes)
    
    parameters["InfectionSpeed"] = np.array([0.6])
    parameters["ReplacementSpeed"] = np.array([ OptimalGamma(parameters["InfectionSpeed"][0])/4,
     OptimalGamma(parameters["InfectionSpeed"][0])/2, OptimalGamma(parameters["InfectionSpeed"][0]) ])
    parameters["MutationSpeed"] = np.array([0.0, 0.00001, 0.0001, 0.001])

    settings["Repeat"] = [10]

    return folder, name, parameters, settings, notes

def mutationTimeSeries(name="mutationTimeSeries", notes = "Time series of the parameters I wish to look at for mutations"):
    folder, name, parameters, settings, notes = features(name = name, notes = notes)
    
    parameters["InfectionSpeed"] = np.array([0.55])
    parameters["ReplacementSpeed"] = np.array([OptimalGamma(parameters["InfectionSpeed"][0])/8, 
    OptimalGamma(parameters["InfectionSpeed"][0])/4, OptimalGamma(parameters["InfectionSpeed"][0])/2, OptimalGamma(parameters["InfectionSpeed"][0]), OptimalGamma(parameters["InfectionSpeed"][0])*2])
    parameters["MutationSpeed"] = np.array([0.0, 0.00001, 0.0001, 0.001])
    parameters["MaxAntigenValue"] = np.arange(1, 11)

    return folder, name, parameters, settings, notes

def mutation2D(name = "mutation2D", notes = "Over the same parameters as features2D, except mutation exist"):
    folder, name, parameters, settings, notes = features2D(name = name, notes = notes)
    
    parameters["MutationSpeed"] = np.array([0.0, 0.00001, 0.0001, 0.001])
    parameters["MaxAntigenValue"] = np.arange(1, 20+1, 1, dtype=int)

    return folder, name, parameters, settings, notes

def mutation2DLowReplacement(name = "mutation2DLowReplacement", notes = "Over the same parameters as mutation2D, but with half the replacementspeed"):
    folder, name, parameters, settings, notes = features2D(name = name, notes = notes)
    
    parameters["MutationSpeed"] = np.array([0.0, 0.00001, 0.0001, 0.001])
    parameters["MaxAntigenValue"] = np.arange(1, 20+1, 1, dtype=int)

    return folder, name, parameters, settings, notes


def crossNonCross(name = "crossNonCross", notes = "Simulation with and without cross immunity."):
    folder, name, parameters, settings, notes = simple(name = name, notes = notes)

    parameters["InfectionSpeed"] = np.arange(0.35, 0.6+0.000001, 0.01)
    parameters["MutationSpeed"] = np.array([10**-4])
    parameters["SpecificStrains"] = ["nonCross", "cross"]

    settings["ShouldSaveDataWhileRunning"] = ["True"] 

    return folder, name, parameters, settings, notes

def crossBig(name = "crossBig", notes = "Same as with crossNonCross, but instead have two additional strains."):
    folder, name, parameters, settings, notes = simple(name = name, notes = notes)

    parameters["InfectionSpeed"] = np.arange(0.35, 0.6+0.000001, 0.01)
    parameters["MutationSpeed"] = np.array([10**-4])
    parameters["SpecificStrains"] = ["nonCrossBig", "crossBig"]

    settings["ShouldSaveDataWhileRunning"] = ["True"] 

    return folder, name, parameters, settings, notes

def crossOdd(name = "crossOdd", notes = "Try with five strain"):
    folder, name, parameters, settings, notes = simple(name = name, notes = notes)

    parameters["InfectionSpeed"] = np.arange(0.35, 0.6+0.000001, 0.01)
    parameters["MutationSpeed"] = np.array([10**-4])
    parameters["SpecificStrains"] = ["odd"]

    settings["ShouldSaveDataWhileRunning"] = ["True"] 

    return folder, name, parameters, settings, notes

def crossSimple(name = "crossSimple", notes = "Two strain with no crossovers"):
    folder, name, parameters, settings, notes = simple(name = name, notes = notes)

    parameters["InfectionSpeed"] = np.arange(0.35, 0.6+0.000001, 0.01)
    parameters["MutationSpeed"] = np.array([10**-4])
    parameters["SpecificStrains"] = ["simple"]

    settings["ShouldSaveDataWhileRunning"] = ["True"] 

    return folder, name, parameters, settings, notes

def crossSwitchingTime(name = "crossSwitchingTime", notes = "cross and cross big with a long run to be able to calculate consistent switching times. "):
    folder, name, parameters, settings, notes = simple(name = name, notes = notes)
    
    parameters["InfectionSpeed"] = np.arange(0.4, 0.5+0.000001, 0.01)
    parameters["MutationSpeed"] = np.array([10**-4])
    settings["Runs"] = [500000000] 
    settings["Repeat"] = [10]
    parameters["SpecificStrains"] = ["cross", "crossBig"]

    return folder, name, parameters, settings, notes

def crossThree(name = "crossThree", notes = "The system with all the combinations. "):
    folder, name, parameters, settings, notes = simple(name = name, notes = notes)
    
    parameters["InfectionSpeed"] = np.arange(0.3, 0.5+0.000001, 0.01)
    parameters["MutationSpeed"] = np.array([10**-4])
    parameters["NAntigens"] = np.array([3])
    parameters["MaxAntigenValue"] = np.array([5])

    settings["Runs"] = [50000000] 
    settings["Repeat"] = [5]
    

    parameters["SpecificStrains"] = ["all"]

    return folder, name, parameters, settings, notes

def crossNonCrossLowReplacement(name = "crossNonCrossLowReplacement", notes = "Simulation with and without cross immunity but with 1/4 of optimal replacement"):
    folder, name, parameters, settings, notes = simple(name = name, notes = notes)

    parameters["InfectionSpeed"] = np.arange(0.35, 0.6+0.000001, 0.01)
    parameters["MutationSpeed"] = np.array([10**-4])
    parameters["SpecificStrains"] = ["cross"]

    settings["ShouldSaveDataWhileRunning"] = ["True"] 

    return folder, name, parameters, settings, notes

def crossNonCrossInjection(name = "crossNonCrossInjection", notes = "Simulation with and without cross immunity but with injections every hundred generation"):
    folder, name, parameters, settings, notes = simple(name = name, notes = notes)

    #parameters["InfectionSpeed"] = np.array([0.42, 0.43, 0.44, 0.45])
    parameters["InfectionSpeed"] = np.arange(0.35, 0.6+0.000001, 0.01)
    parameters["MutationSpeed"] = np.array([10**-4])
    parameters["SpecificStrains"] = ["nonCross", "cross", "simple"]

    settings["Repeat"] = [5]
    settings["ShouldSaveDataWhileRunning"] = ["True"] 

    return folder, name, parameters, settings, notes

def crossNonCrossInjectionLow(name = "crossNonCrossInjectionLow", notes = "Simulation with and without cross immunity but with injections every hundred generation with 1/4 replacement"):
    folder, name, parameters, settings, notes = simple(name = name, notes = notes)

    #parameters["InfectionSpeed"] = np.array([0.42, 0.43, 0.44, 0.45])
    parameters["InfectionSpeed"] = np.arange(0.35, 0.6+0.000001, 0.01)
    parameters["MutationSpeed"] = np.array([10**-4])
    parameters["SpecificStrains"] = ["nonCross", "cross", "simple"]

    settings["Repeat"] = [5]
    settings["ShouldSaveDataWhileRunning"] = ["True"] 

    return folder, name, parameters, settings, notes

def crossNonCrossLow(name = "crossNonCrossLow", notes = "Simulation with and without cross immunity with 1/4 replacement"):
    folder, name, parameters, settings, notes = simple(name = name, notes = notes)

    #parameters["InfectionSpeed"] = np.array([0.42, 0.43, 0.44, 0.45])
    parameters["InfectionSpeed"] = np.arange(0.35, 0.6+0.000001, 0.01)
    parameters["MutationSpeed"] = np.array([10**-4])
    parameters["SpecificStrains"] = ["nonCross", "cross", "simple"]

    settings["Repeat"] = [5]
    settings["ShouldSaveDataWhileRunning"] = ["True"] 

    return folder, name, parameters, settings, notes

def crossNonCrossInjectionFast(name = "crossNonCrossInjectionFast", notes = "Simulation with and without cross immunity with vaccine injections at every 10'th generation."):
    folder, name, parameters, settings, notes = simple(name = name, notes = notes)

    #parameters["InfectionSpeed"] = np.array([0.42, 0.43, 0.44, 0.45])
    parameters["InfectionSpeed"] = np.arange(0.35, 0.6+0.000001, 0.01)
    parameters["MutationSpeed"] = np.array([10**-4])
    parameters["SpecificStrains"] = ["nonCross", "cross", "simple"]

    settings["Repeat"] = [5]
    settings["ShouldSaveDataWhileRunning"] = ["True"] 

    return folder, name, parameters, settings, notes


##-------------------------------------------------------------------------------##
mp.CreateParametersAndSettings(eval(func), name, notes)

if SameyGamma == True:
    q = pandas.pandas.read_csv("data/" + func + "/parameters.csv")
    alphas = q["InfectionSpeed"].unique()
    gammas = OptimalGamma(a = alphas, b = b) * factor

    q.loc[:, ("ReplacementSpeed")] = OptimalGamma(q.loc[:, ("InfectionSpeed")], b = b) * factor

    q.to_csv("data/" + func + "/parameters.csv", index=False)

