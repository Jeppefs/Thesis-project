import malaria_statistics as MS 

import numpy as np
import matplotlib.pyplot as plt
import pandas as pandas
import scipy.optimize as op

def simple():
    q = MS.MalariaStatistics("simple")

    #linearFitResults = MS.LinearFit(q.parameters["InfectionSpeed"], q.dataEnd["run"])
    #q.PlotExtinctionTime("InfectionSpeed")
    #plt.plot(np.arange())
    #q.PlotMeanInfection("InfectionSpeed")

    return

def deathRate():
    q = MS.MalariaStatistics("DeathRate", timelineIndex = [10,1])

    #q.PlotExtinctionTime("DeathSpeed")
    plt.figure()
    q.PlotMeanInfection("DeathSpeed", newFigure = False)
    #op.minimize( MS.Loglike2D, method="Powell", x0 = tuple([0.5, 1, 400]), 
    #args=tuple([q.parameters["deathRate"][2:-1], q.dataEndRepeat["mean"][2:-1], np.sqrt( dataEndRepeat["variance"][2:-1]/len(dataEndRepeat["variance"][2:-1]) ), FitFunc_Power]) )
    #q.PlotTimeLinePlot()
    
    return

def complexFun():
    q = MS.MalariaStatistics("complexFun", timelineIndex = [5,1])
    
    plt.figure()
    q.PlotExtinctionTime(vary = "MaxAntigenValue", newFigure=False)
    linearFitResults = MS.LinearFit(q.parameters["MaxAntigenValue"], q.dataEnd["run"])
    plt.plot(np.arange(2,21), linearFitResults["slope"]*np.arange(2,21)+linearFitResults["intersect"])

    q.PlotMeanInfection(vary = "MaxAntigenValue")
    
    
    
    #for i in np.arange(19)+1:
    #    q.timelineIndex = [i,1]
    #    q.ImportTimeline()
    #    q.ImportStrainCounter()
    #    q.PlotTimeline(newFigure = True)
    #    q.PlotStrainCounter(newFigure=False)
    
    return

def complexFunReplacement():
    q = MS.MalariaStatistics("complexFunReplacement", timelineIndex = [8,1])
    
    plt.figure()
    q.PlotExtinctionTime(vary = "MaxAntigenValue", newFigure=False)
    linearFitResults = MS.LinearFit(q.parameters["MaxAntigenValue"], q.dataEnd["run"])
    plt.plot(np.arange(2,21), linearFitResults["slope"]*np.arange(2,21)+linearFitResults["intersect"])

    q.PlotMeanInfection(vary = "MaxAntigenValue")

    q.PlotTimeline()
    q.ImportStrainCounter()
    q.PlotStrainCounter(newFigure=False)
    

complexFunReplacement()
plt.show()
