import malaria_statistics as MS 

import numpy as np
import matplotlib.pyplot as plt
import pandas as pandas
import scipy.optimize as op

def simple():
    q = MS.MalariaStatistics("simple")

    q.PlotExtinctionTime("InfectionSpeed", xlabel = r"$\alpha$")
    plt.figure()
    plt.plot(np.arange(1.0, 1.05, 0.0001), 10000*(np.arange(1.0, 1.05, 0.0001)-1), color="r")
    q.PlotMeanInfection("InfectionSpeed", xlabel = r"$\alpha$", newFigure=False)
    

    q.timelineIndex = [1, 1]
    print("InfectionSpeed", q.parameters["InfectionSpeed"][q.timelineIndex[0]])
    q.ImportTimeline()
    q.PlotTimeline()

    q.timelineIndex = [40, 5]
    print("InfectionSpeed", q.parameters["InfectionSpeed"][q.timelineIndex[0]])
    q.ImportTimeline()
    q.PlotTimeline()
    return

def replacement(): 
    q = MS.MalariaStatistics("replacement")

    q.PlotExtinctionTime("ReplacementSpeed", xlabel = r"$\gamma$")
    q.PlotMeanInfection("ReplacementSpeed", xlabel = r"$\gamma$")

    q.timelineIndex = [10, 1]
    print("ReplacementSpeed", q.parameters["ReplacementSpeed"][q.timelineIndex[0]])
    q.ImportTimeline()
    q.PlotTimeline()

    q.timelineIndex = [40, 1]
    print("ReplacementSpeed", q.parameters["ReplacementSpeed"][q.timelineIndex[0]])
    q.ImportTimeline()
    q.PlotTimeline()
   
    #q2 = MS.MalariaStatistics("replacement2")
    #q2.PlotExtinctionTime("ReplacementSpeed", xlabel = r"$\gamma$")
    #q2.PlotMeanInfection("ReplacementSpeed", xlabel = r"$\gamma$")

    return

def complexFun():
    q = MS.MalariaStatistics("complexFun", timelineIndex = [4,1])
    
    plt.figure()
    q.PlotExtinctionTime(vary = "MaxAntigenValue", newFigure=False)
    linearFitResults = MS.LinearFit(q.parameters["MaxAntigenValue"], q.dataEnd["run"])
    plt.plot(np.arange(2,21), linearFitResults["slope"]*np.arange(2,21)+linearFitResults["intersect"])

    q.PlotMeanInfection(vary = "MaxAntigenValue")
    
    q.PlotTimeline()
    q.ImportStrainCounter
    q.PlotStrainCounter(newFigure=False)
    
    #for i in np.arange(19)+1:
    #    q.timelineIndex = [i,1]
    #    q.ImportTimeline()
    #    q.ImportStrainCounter()
    #    q.PlotTimeline(newFigure = True)
    #    q.PlotStrainCounter(newFigure=False)
    
    return

def complexFunReplacement():
    q = MS.MalariaStatistics("complexFunReplacement", timelineIndex = [4,1])
    
    plt.figure()
    q.PlotExtinctionTime(vary = "MaxAntigenValue", newFigure=False)
    #linearFitResults = MS.LinearFit(q.parameters["MaxAntigenValue"], q.dataEnd["run"])
    #plt.plot(np.arange(2,21), linearFitResults["slope"]*np.arange(2,21)+linearFitResults["intersect"])

    q.PlotMeanInfection(vary = "MaxAntigenValue")

    q.PlotTimeline()
    q.ImportStrainCounter()
    q.PlotStrainCounter(newFigure=False)
   
    

replacement()
plt.show()
